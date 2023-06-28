from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TMDB_USERNAME = 'your_username'
TMDB_PASSWORD = 'your_password'
DATA_FILE_PATH = '/path/to/episodes.txt'
ADD_EPISODES_URL = 'https://www.themoviedb.org/tv/201900/season/1/edit?active_nav_item=episodes'

driver = webdriver.Chrome()
driver.get('https://www.themoviedb.org/login')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))

driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)

driver.find_element(By.XPATH, '//*[@id="login_button"]').click()

with open(DATA_FILE_PATH, 'r') as file:
    data = file.readlines()

driver.get(ADD_EPISODES_URL)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="grid"]/div[1]/a')))

successful_lines = []
for index, line in enumerate(data):
    try:
        episode_number, date, duration, topic, description = line.strip().split(',')

        driver.find_element(By.XPATH, '//*[@id="grid"]/div[1]/a').click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.k-formatted-value')))

        current_episode_number = int(driver.find_element(By.CSS_SELECTOR, '.k-formatted-value').get_attribute('aria-valuenow'))
        clicks_needed = int(episode_number) - current_episode_number
        if clicks_needed > 0:
            for _ in range(clicks_needed):
                increase_button = driver.find_element(By.CSS_SELECTOR, '.k-link-increase')
                increase_button.click()
        else:
            for _ in range(abs(clicks_needed)):
                decrease_button = driver.find_element(By.CSS_SELECTOR, '.k-link-decrease')
                decrease_button.click()

        driver.find_element(By.XPATH, '//*[@id="zh-CN_name_text_input_field"]').send_keys(topic)

        driver.find_element(By.XPATH, '//*[@id="zh-CN_overview_text_box_field"]').send_keys(description)

        air_date_field = driver.find_element(By.XPATH, '//*[@id="air_date_date_picker_field"]')
        air_date_field.clear()
        air_date_field.send_keys(date)

        driver.find_element(By.XPATH, '//*[@id="zh-CN_runtime_text_input_field"]').send_keys(duration)

        save_button = driver.find_element(By.CLASS_NAME, 'k-grid-update')
        save_button.click()

        time.sleep(2)

        successful_lines.append(index)
        
        if index != 0:
            print(f'Successfully added episode: {episode_number}')
    except Exception as e:
        error_message = str(e).split('\n')[0]
        if index != 0:
            print(f'Error: {error_message}')
            print(f'Failed to add episode: {episode_number}')

with open(DATA_FILE_PATH, 'w') as file:
    for index, line in enumerate(data):
        if index not in successful_lines:
            file.write(line)

driver.quit()
