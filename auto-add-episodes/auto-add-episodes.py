import os
import time
import json
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

def add_episode(episode_number, date, duration, topic, description):
    driver.get(EPISODES_URL)
    time.sleep(3)

    existing_episodes = [
        int(e.text.strip().replace(',', '')) for e in driver.find_elements(By.XPATH, "//table/tbody/tr/td[1]")
    ]

    if int(episode_number) in existing_episodes:
        print(f"Episode {episode_number} already exists")
        return True

    try:
        add_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.k-grid-add"))
        )
        add_button.click()
        time.sleep(3)

        topic_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, f"{LANGUAGE_CODE}_name_text_input_field"))
        )
        topic_input.clear()
        topic_input.send_keys(topic)

        description_input = driver.find_element(By.ID, f"{LANGUAGE_CODE}_overview_text_box_field")
        description_input.clear()
        description_input.send_keys(description)

        try:
            date_picker_input = driver.find_element(By.ID, "air_date_date_picker_field")
            driver.execute_script("arguments[0].value = '';", date_picker_input)
            time.sleep(0.5)

            ActionChains(driver) \
               .click(date_picker_input) \
               .key_down(webdriver.Keys.CONTROL) \
               .send_keys('a') \
               .key_up(webdriver.Keys.CONTROL) \
               .send_keys(webdriver.Keys.DELETE) \
               .send_keys(date) \
               .perform()
            time.sleep(0.5)

            driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
                arguments[0].dispatchEvent(new Event('change', {bubbles:true}));
                arguments[0].dispatchEvent(new Event('blur', {bubbles:true}));
            """, date_picker_input, date)
            time.sleep(1)
        except Exception:
            pass

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

        try:
            save_button = driver.find_element(By.CSS_SELECTOR, "button[ref-update-button]")
            save_button.click()
            time.sleep(3)
            print(f"Successfully added episode {episode_number}")
            return True
        except Exception:
            try:
                # 不使用文本内容，改用通用的CSS选择器找到保存按钮
                # 尝试几种常见的保存按钮选择器
                save_selectors = [
                    ".k-grid-update",  # Kendo UI常用的保存按钮类
                    "button.k-button.k-primary",  # 主要按钮通常是保存
                    "form button[type='submit']",  # 表单提交按钮
                    ".edit-buttons button:last-child",  # 编辑按钮组中的最后一个按钮通常是保存
                    ".k-edit-buttons button:last-child",  # Kendo编辑按钮组
                    ".modal-footer button.k-primary",  # 模态框中的主要按钮
                ]

                for selector in save_selectors:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    if buttons:
                        buttons[0].click()
                        time.sleep(3)
                        print(f"Successfully added episode {episode_number}")
                        return True

                # 如果上述方法都失败，尝试查找form元素并提交
                forms = driver.find_elements(By.TAG_NAME, "form")
                if forms:
                    driver.execute_script("arguments[0].submit();", forms[0])
                    time.sleep(3)
                    print(f"Successfully added episode {episode_number}")
                    return True

                print(f"Failed to add episode {episode_number}")
                return False
            except Exception:
                print(f"Failed to add episode {episode_number}")
                return False
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
    