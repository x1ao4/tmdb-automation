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
    """处理 Cookie 弹窗"""
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
    """添加剧集"""
    driver.get(EPISODES_URL)
    time.sleep(3)

    # 获取已存在的剧集编号，避免重复添加
    existing_episodes = [
        int(e.text.strip()) for e in driver.find_elements(By.XPATH, "//table/tbody/tr/td[1]")
    ]

    if int(episode_number) in existing_episodes:
        print(f"Episode {episode_number} already exists, skipping.")
        return True

    try:
        # 点击 "新增新集数" 按钮
        add_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.k-grid-add"))
        )
        ActionChains(driver).move_to_element(add_button).click().perform()

        # 填写集数信息
        episode_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".k-numerictextbox input"))
        )
        episode_input.clear()
        episode_input.send_keys(episode_number)

        topic_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, f"{LANGUAGE_CODE}_name_text_input_field"))
        )
        topic_input.send_keys(topic)

        description_input = driver.find_element(By.ID, f"{LANGUAGE_CODE}_overview_text_box_field")
        description_input.send_keys(description)

        date_input = driver.find_element(By.ID, "air_date_date_picker_field")
        date_input.clear()
        date_input.send_keys(date)

        duration_input = driver.find_element(By.ID, f"{LANGUAGE_CODE}_runtime_text_input_field")
        duration_input.send_keys(duration)

        save_button = driver.find_element(By.XPATH, "/html/body/div[16]/div[3]/button[1]")
        driver.execute_script("arguments[0].click();", save_button)

        print(f"Successfully added episode: {episode_number}")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Failed to add episode {episode_number}: {str(e)}")
        return False


def main():
    """主流程"""
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
        # 确保每行数据被正确分割
        episode_number, date, duration, topic, description = line.strip().split(';', maxsplit=4)

        # 调用 add_episode 方法，逐条填写剧集信息
        if add_episode(episode_number, date, duration, topic, description):
            success_count += 1
            remaining_data.remove(line)

            # 更新文件，防止重复添加
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                file.writelines(remaining_data)

    print(f'\nTotal episodes added: {success_count}')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()
