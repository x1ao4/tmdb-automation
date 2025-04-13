import os
import re
import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCRIPT_DIR = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(SCRIPT_DIR, 'config.ini'), encoding='utf-8')

TMDB_USERNAME = config.get('TMDB', 'USERNAME')
TMDB_PASSWORD = config.get('TMDB', 'PASSWORD')
EPISODE_URL = config.get('SHOW', 'EPISODE_URL')
LANGUAGE = config.get('SHOW', 'LANGUAGE')
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, 'backdrops')

match = re.search(r'(https://www.themoviedb.org/tv/[\w-]+/season/\d+/episode/)\d+', EPISODE_URL)
TV_SHOW_URL = match.group(1) + '{episode_number}/images/backdrops'

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
        pass  # 如果没有弹窗，直接继续执行

try:
    driver = webdriver.Chrome()
    driver.get('https://www.themoviedb.org/login')

    # **登录 TMDB**
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="login_button"]').click()

    # **等待登录成功（检测头像出现）**
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//span[@class="avatar"]/a/img[@class="avatar"]'))
    )

    # **处理 Cookie 弹窗（登录成功后自动跳转主页时处理）**
    handle_cookie_popup()

    success_count = 0
    failure_count = 0

    image_files = sorted(os.listdir(IMAGE_FOLDER), key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

    for image_file in image_files:
        if not image_file.split('.')[0].isdigit():
            continue
        
        episode_number = int(image_file.split('.')[0])
        episode_url = TV_SHOW_URL.format(episode_number=episode_number)
        driver.get(episode_url)

        add_background_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "add_image") and contains(@class, "upload")]'))
        )
        add_background_button.click()

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )

        image_path = os.path.join(IMAGE_FOLDER, f'{episode_number}.jpg')
        
        if not os.path.exists(image_path):
            continue

        file_input.send_keys(image_path)
        time.sleep(3)
        
        try:
            error_message = driver.find_element(By.CSS_SELECTOR, '.error_message')
            failure_count += 1
            print(f'Failed to upload backdrop for episode {episode_number}: {error_message.text}')
            
            close_button = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
            close_button.click()
            time.sleep(2)
            
            cancel_button = driver.find_element(By.XPATH, '//button[@aria-label="Cancel"]')
            cancel_button.click()
            time.sleep(1)
            
            continue
            
        except:
            success_count += 1
            os.remove(image_path)
            print(f'Successfully uploaded backdrop for episode {episode_number}')
        
        driver.refresh()

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'k-input-button')))
        dropdown_button = driver.find_element(By.CLASS_NAME, 'k-input-button')
        dropdown_button.click()

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.k-searchbox input.k-input-inner'))
        )
        search_box.send_keys(LANGUAGE)
        
        language_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[.//span[contains(text(), "{LANGUAGE}")]]'))
        )
        language_option.click()

        time.sleep(1)

    print(f'\nTotal uploaded: {success_count}')
    print(f'Total failed: {failure_count}')

except Exception as e:
    print(f'Error: {e}')

finally:
    driver.quit()
