from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TMDB_USERNAME = 'your_username'
TMDB_PASSWORD = 'your_password'
EPISODE_URL = 'https://www.themoviedb.org/tv/201900/season/1/episode/1/edit?active_nav_item=primary_facts'
DATA_FILE = '/path/to/episodes.txt'
LANGUAGE_CODE = 'zh_CN'

try:
    driver = webdriver.Chrome()
    driver.get('https://www.themoviedb.org/login')

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))

    driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)

    driver.find_element(By.XPATH, '//*[@id="login_button"]').click()

    # Check if there is a cookie acceptance page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
        accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        accept_button.click()
    except:
        pass

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = file.readlines()

    success_count = 0
    failure_count = 0

    remaining_data = data.copy()

    for line in data:
        episode_number, date, duration, topic, description = line.strip().split(';', maxsplit=4)
        episode_url = EPISODE_URL.replace('/episode/1/', f'/episode/{episode_number}/')
        driver.get(episode_url)

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{LANGUAGE_CODE}_name"]')))

            name_field = driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_name"]')
            name_field.clear()
            name_field.send_keys(topic)

            overview_field = driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_overview"]')
            overview_field.clear()
            overview_field.send_keys(description)

            runtime_field = driver.find_element(By.ID, 'runtime')
            runtime_field.clear()
            runtime_field.send_keys(duration)

            save_button = driver.find_element(By.ID, 'submit')
            save_button.click()

            time.sleep(2)

            success_count += 1

            # Remove the line from the remaining data and update the file
            remaining_data.remove(line)
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                for line in remaining_data:
                    file.write(line)

            print(f'Successfully updated episode: {episode_number}')
        except Exception as e:
            failure_count += 1
            print(f'Failed to update episode: {episode_number} - {e}')

    print()
    print(f'Total updated: {success_count}')
    print(f'Total failed: {failure_count}')

except Exception as e:
    print(f'Error: {e}')

driver.quit()
