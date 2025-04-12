import os
import time
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
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="login_button"]').click()
    
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
        int(e.text.strip()) for e in driver.find_elements(By.XPATH, "//table/tbody/tr/td[1]")
    ]

    if int(episode_number) in existing_episodes:
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
            
            ActionChains(driver)\
                .click(date_picker_input)\
                .key_down(webdriver.Keys.CONTROL)\
                .send_keys('a')\
                .key_up(webdriver.Keys.CONTROL)\
                .send_keys(webdriver.Keys.DELETE)\
                .send_keys(date)\
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
            numeric_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".k-numerictextbox"))
            )
            
            try:
                current_episode = driver.execute_script("""
                    var numericContainer = document.querySelector('.k-numerictextbox');
                    if (numericContainer) {
                        var input = numericContainer.querySelector('input');
                        if (input) {
                            return parseInt(input.value) || 0;
                        }
                    }
                    return 0;
                """)
                
                target_episode = int(episode_number)
                
                if current_episode > target_episode:
                    clicks_needed = current_episode - target_episode
                    button_selector = ".k-spinner-decrease"
                else:
                    clicks_needed = target_episode - current_episode
                    button_selector = ".k-spinner-increase"
                
                if clicks_needed > 0:
                    button = numeric_container.find_element(By.CSS_SELECTOR, button_selector)
                    for _ in range(clicks_needed):
                        button.click()
                        time.sleep(0.05)
            except Exception:
                try:
                    down_button = numeric_container.find_element(By.CSS_SELECTOR, ".k-spinner-decrease")
                    up_button = numeric_container.find_element(By.CSS_SELECTOR, ".k-spinner-increase")
                    
                    for _ in range(20):
                        down_button.click()
                        time.sleep(0.05)
                    
                    target_clicks = int(episode_number) - 1
                    for _ in range(target_clicks):
                        up_button.click()
                        time.sleep(0.05)
                except Exception:
                    pass
            
            driver.execute_script("""
                var numericContainer = document.querySelector('.k-numerictextbox');
                if (numericContainer) {
                    try {
                        if (window.kendo && window.jQuery) {
                            var kendoWidget = window.jQuery(numericContainer).data("kendoNumericTextBox");
                            if (kendoWidget) {
                                kendoWidget.value(arguments[0]);
                                kendoWidget.trigger("change");
                                return;
                            }
                        }
                    } catch(e) {}
                    
                    var allInputs = numericContainer.querySelectorAll('input');
                    for (var i = 0; i < allInputs.length; i++) {
                        allInputs[i].value = arguments[0];
                        allInputs[i].dispatchEvent(new Event('change', { bubbles: true }));
                        allInputs[i].dispatchEvent(new Event('blur', { bubbles: true }));
                    }
                }
            """, episode_number)
            
        except Exception:
            pass

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
                
                return False
            except Exception:
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
    remaining_data = data.copy()

    for line in data:
        episode_number, date, duration, topic, description = line.strip().split(';', maxsplit=4)

        if add_episode(episode_number, date, duration, topic, description):
            success_count += 1
            remaining_data.remove(line)

            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                file.writelines(remaining_data)

    print(f'\nTotal added: {success_count}')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()
