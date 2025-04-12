import os
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
LANGUAGE_CODE = config.get('SHOW', 'LANGUAGE_CODE')
DATA_FILE = os.path.join(SCRIPT_DIR, 'episodes.txt')

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

def update_episode(episode_number, topic, description, date, duration):
    episode_url = EPISODE_URL.replace('/episode/1/', f'/episode/{episode_number}/')
    driver.get(episode_url)
    
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{LANGUAGE_CODE}_name"]')))
        driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_name"]').clear()
        driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_name"]').send_keys(topic)
        driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_overview"]').clear()
        driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_overview"]').send_keys(description)
        driver.find_element(By.ID, 'air_date').clear()
        driver.find_element(By.ID, 'air_date').send_keys(date)
        driver.find_element(By.ID, 'runtime').clear()
        driver.find_element(By.ID, 'runtime').send_keys(duration)
        driver.find_element(By.ID, 'submit').click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f'Failed to update episode {episode_number}: {e}')
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
        if update_episode(episode_number, topic, description, date, duration):
            success_count += 1
            remaining_data.remove(line)
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                for entry in remaining_data:
                    file.write(entry)
            print(f'Successfully updated episode {episode_number}')
        else:
            failure_count += 1
    
    print(f'\nTotal updated: {success_count}')
    print(f'Total failed: {failure_count}')
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()
