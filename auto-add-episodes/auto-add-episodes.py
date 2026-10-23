import os
import time
import json
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 读取配置文件
SCRIPT_DIR = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(SCRIPT_DIR, 'config.ini'), encoding='utf-8')

TMDB_USERNAME = config.get('TMDB', 'USERNAME')
TMDB_PASSWORD = config.get('TMDB', 'PASSWORD')
EPISODES_URL = config.get('SHOW', 'EPISODES_URL')
LANGUAGE_CODE = config.get('SHOW', 'LANGUAGE_CODE')
DATA_FILE = os.path.join(SCRIPT_DIR, 'episodes.txt')

# 启动 WebDriver
driver = webdriver.Chrome()

def login():
    driver.get('https://www.themoviedb.org/login')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'auth_username')))
    driver.find_element(By.ID, 'auth_username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'auth_password').send_keys(TMDB_PASSWORD)
    driver.find_element(By.ID, 'auth_login_button').click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//span[@class="avatar"]/a/img[@class="avatar"]'))
    )

def handle_cookie_popup():
    try:
        cookie_banner = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "onetrust-banner-sdk"))
        )
        if cookie_banner.is_displayed():
            driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler").click()
            time.sleep(1)
    except:
        pass

def wait_for_grid_loaded(timeout=90, settle=0.8):
    """等待分集表格把数据取回并渲染完成，返回数据源里的集数（超时返回 None）。

    编辑页是 Kendo Grid：工具栏的「新增新集數」按钮在 HTML 里一早就存在，
    但表格数据是异步加载的。若在 dataBound 之前点它，弹窗会先打开、随后被表格
    重新渲染冲掉，表现出来就是「弹窗打开了却填不进内容」。所以必须先等表格稳定。
    """
    script = """
        var jq = (window.kendo && window.kendo.jQuery) ? window.kendo.jQuery : window.jQuery;
        var grid = null;
        if (jq) {
            grid = jq('#grid').data('kendoGrid') || jq('.k-grid').first().data('kendoGrid');
        }
        var domRows = document.querySelectorAll('table tbody tr').length;
        var active = window.jQuery ? window.jQuery.active : 0;
        if (!grid) { return [domRows, domRows, false, active]; }
        return [grid.dataSource.data().length, domRows, true, active];
    """
    deadline = time.time() + timeout
    last = None
    stable_since = time.time()
    while time.time() < deadline:
        state = driver.execute_script(script)
        # 表格实例已就绪，且数据行数稳定、没有还在跑的 jQuery 异步请求
        if state[2] and state[3] == 0:
            if state != last:
                last = state
                stable_since = time.time()
            elif time.time() - stable_since >= settle:
                return last[0]
        else:
            last = None
        time.sleep(0.2)
    # 超时仍没读到表格：返回 None，调用方应中止而不是当成「一集都没有」继续添加
    return None

def open_add_dialog(retries=3):
    """点击「新增新集數」并确认弹窗真的留住了，返回是否成功。"""
    for attempt in range(1, retries + 1):
        add_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.k-grid-add"))
        )
        add_button.click()
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, f"{LANGUAGE_CODE}_name_text_input_field"))
            )
            # 再等半秒：如果表格这时才 dataBound，弹窗会被冲掉，这里能发现
            time.sleep(0.5)
            if driver.find_elements(By.CSS_SELECTOR, ".k-edit-form-container"):
                return True
        except TimeoutException:
            pass
        print(f"Add dialog did not stay open (attempt {attempt}/{retries}), retrying")
        time.sleep(1)
    return False

def set_air_date(date):
    """用 Kendo DatePicker 组件 API 写入上映日期，并回读表单模型。

    直接改 input.value（或 dispatch input/change）只改页面显示：DatePicker 内部的
    值不变，表单模型里的 air_date 仍是页面预填的日期（一般是上一集 +7 天），
    保存时提交的就是那个预填值 —— 日期不对时会被静默写错。
    """
    iso_date = date.replace('/', '-')
    return json.loads(driver.execute_script("""
        var out = { widget: false, applied: false, model: '', input: '' };
        var jq = (window.kendo && window.kendo.jQuery) ? window.kendo.jQuery : window.jQuery;
        var el = document.getElementById('air_date_date_picker_field');
        if (!el) { return JSON.stringify(out); }

        // TMDB 的模型里 air_date 是字符串：预填是 yyyy-MM-dd，
        // 用户点日历选中后是 Date.toString() 的形式，两种都要能归一化成 yyyy-MM-dd
        function toIso(v) {
            if (!v) { return ''; }
            if (typeof v === 'string' && /^\\d{4}-\\d{2}-\\d{2}$/.test(v)) { return v; }
            var d = (v instanceof Date) ? v : new Date(v);
            if (isNaN(d.getTime())) { return ''; }
            var mm = ('0' + (d.getMonth() + 1)).slice(-2);
            var dd = ('0' + d.getDate()).slice(-2);
            return d.getFullYear() + '-' + mm + '-' + dd;
        }

        var picker = null;
        if (jq) {
            picker = jq(el).data('kendoDatePicker');
            if (!picker && el.parentNode) { picker = jq(el.parentNode).data('kendoDatePicker'); }
        }
        if (picker) {
            out.widget = true;
            var parsed = kendo.parseDate(arguments[0], 'yyyy-MM-dd');
            if (parsed) {
                picker.value(parsed);
                picker.trigger('change');
                out.applied = true;
            }
        }

        var formEl = document.querySelector('.k-edit-form-container');
        var form = (jq && formEl) ? jq(formEl).data('kendoForm') : null;
        if (form && form.options && form.options.formData) {
            out.model = toIso(form.options.formData.air_date);
        }
        out.input = el.value;
        return JSON.stringify(out);
    """, iso_date) or '{}')

def add_episode(episode_number, date, duration, topic, description):
    driver.get(EPISODES_URL)

    # 必须先等表格加载完：否则既读不到已存在的集数（重复检查失效），
    # 点新增也会被随后到来的 dataBound 冲掉
    if wait_for_grid_loaded() is None:
        print(f"Failed to add episode {episode_number}: the episode table never finished loading")
        return False

    # 从表格数据源一次读全部集数：逐格取 text 要一千多次 WebDriver 往返（实测 12s+）
    existing_episodes = driver.execute_script("""
        var jq = (window.kendo && window.kendo.jQuery) ? window.kendo.jQuery : window.jQuery;
        var grid = jq ? (jq('#grid').data('kendoGrid') || jq('.k-grid').first().data('kendoGrid')) : null;
        if (!grid) { return null; }
        return grid.dataSource.data().map(function (row) { return row.episode_number; });
    """)
    if existing_episodes is None:
        # 拿不到数据源时退回读单元格（慢，但能兜底）
        existing_episodes = []
        for cell in driver.find_elements(By.XPATH, "//table/tbody/tr/td[1]"):
            text = cell.text.strip().replace(',', '')
            if text.isdigit():
                existing_episodes.append(int(text))
    existing_episodes = [int(number) for number in existing_episodes if number is not None]

    if int(episode_number) in existing_episodes:
        print(f"Episode {episode_number} already exists")
        return True

    try:
        if not open_add_dialog():
            print(f"Failed to add episode {episode_number}: the add dialog never stayed open")
            return False

        topic_input = driver.find_element(By.ID, f"{LANGUAGE_CODE}_name_text_input_field")
        topic_input.clear()
        topic_input.send_keys(topic)

        description_input = driver.find_element(By.ID, f"{LANGUAGE_CODE}_overview_text_box_field")
        description_input.clear()
        description_input.send_keys(description)

        iso_date = date.replace('/', '-')
        date_result = set_air_date(date)
        if date_result.get('widget'):
            if date_result.get('model') and date_result['model'] != iso_date:
                print(f"Failed to set air date for episode {episode_number}: form model holds {date_result['model']}, expected {iso_date}, skipping save")
                return False
            if not date_result.get('applied'):
                print(f"Failed to set air date for episode {episode_number}: date picker rejected {iso_date}, skipping save")
                return False
        else:
            print(f"Warning: air date picker widget not found for episode {episode_number}, the air date may not be submitted")

        duration_input = driver.find_element(By.ID, f"{LANGUAGE_CODE}_runtime_text_input_field")
        duration_input.clear()
        duration_input.send_keys(duration)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".k-numerictextbox"))
            )
        except Exception:
            pass

        # 集数是 Kendo NumericTextBox：组件实例挂在带 data-role 的隐藏原始 input 上，
        # 且必须用 kendo 自带的 jQuery 获取（window.jQuery 与之不是同一实例）。
        # 直接改 input.value 只会更新页面显示，保存提交的仍是模型里自动生成的集数，
        # 因此必须走组件 API 设值，并在保存前回读模型校验。
        set_result = {}
        try:
            set_result = json.loads(driver.execute_script("""
                var target = arguments[0];
                var result = { widget_set: false, model_value: null };

                var container = document.querySelector('.k-numerictextbox');
                var boundInput = container ? container.querySelector('input[data-role="numerictextbox"]') : null;
                if (!boundInput) {
                    boundInput = document.getElementById('episode_number_numeric_text_box_field');
                }
                var kendojq = (window.kendo && window.kendo.jQuery) ? window.kendo.jQuery : null;

                var widget = null;
                if (kendojq && boundInput) {
                    widget = kendojq(boundInput).data('kendoNumericTextBox');
                }
                if (!widget && kendojq && container) {
                    widget = kendojq(container).data('kendoNumericTextBox');
                }
                if (!widget && window.jQuery && container) {
                    widget = window.jQuery(container).data('kendoNumericTextBox');
                }

                if (widget) {
                    widget.value(target);
                    widget.trigger('change');
                    result.widget_set = true;
                }

                try {
                    var formEl = document.querySelector('.k-edit-form-container');
                    if (formEl && kendojq) {
                        var form = kendojq(formEl).data('kendoForm');
                        if (form && form.options && form.options.formData) {
                            result.model_value = form.options.formData.episode_number;
                        }
                    }
                } catch (e) {}

                return JSON.stringify(result);
            """, episode_number) or '{}')
        except Exception:
            pass

        if not set_result.get('widget_set'):
            print(f"Failed to set episode number for episode {episode_number}: Kendo widget not found, skipping save to avoid a wrong episode number")
            return False

        model_value = set_result.get('model_value')
        if model_value is not None and int(model_value) != int(episode_number):
            print(f"Failed to set episode number for episode {episode_number}: form model still holds {model_value}, skipping save")
            return False
        if model_value is None:
            print(f"Warning: episode number {episode_number} was set via Kendo API, but the form model could not be verified")

        save_buttons = driver.find_elements(By.CSS_SELECTOR, "button[ref-update-button]")
        if not save_buttons:
            # 只在弹窗内找主要按钮，避免点到弹窗外的其它 primary 按钮或取消按钮
            save_buttons = driver.find_elements(By.CSS_SELECTOR, ".k-window button.k-button-primary")
        if not save_buttons:
            print(f"Failed to add episode {episode_number}: save button not found")
            return False

        save_buttons[-1].click()

        # 保存成功后弹窗会关闭；没关闭说明没存进去（校验不通过等），
        # 此时不能报成功，否则 episodes.txt 里这行会被删掉，数据就丢了
        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".k-edit-form-container"))
            )
        except TimeoutException:
            print(f"Failed to add episode {episode_number}: edit dialog is still open after saving, keeping the data for retry")
            return False

        print(f"Successfully added episode {episode_number}")
        return True
    except Exception as e:
        print(f"Failed to add episode {episode_number}: {str(e)}")
        return False

def main():
    login()
    handle_cookie_popup()

    if not os.path.exists(DATA_FILE):
        print("Data file not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = file.readlines()

    success_count = 0
    failure_count = 0
    remaining_data = data.copy()

    for line in data:
        episode_number, date, duration, topic, description = line.strip().split(';', maxsplit=4)

        if add_episode(episode_number, date, duration, topic, description):
            success_count += 1
            remaining_data.remove(line)

            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                file.writelines(remaining_data)
        else:
            failure_count += 1

    print(f'\nTotal added: {success_count}')
    print(f'Total failed: {failure_count}')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()
    