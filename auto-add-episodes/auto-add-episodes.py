from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TMDB_USERNAME = 'your_username'
TMDB_PASSWORD = 'your_password'
DATA_FILE_PATH = '/path/to/episodes.txt'
ADD_EPISODES_URL = 'https://www.themoviedb.org/tv/229116-dust/season/6/edit?active_nav_item=episodes'
LANGUAGE_CODE = 'en-US'

try:
    driver = webdriver.Chrome()
    driver.get('https://www.themoviedb.org/login')

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))

    driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)

    driver.find_element(By.XPATH, '//*[@id="login_button"]').click()

    with open(DATA_FILE_PATH, 'r') as file:
        data = file.readlines()

    driver.get(ADD_EPISODES_URL)

    time.sleep(3)

    existing_episode_numbers = []
    for i in range(1, 1000):
        xpath = f'//*[@id="grid"]/div[3]/table/tbody/tr[{i}]/td[1]'
        episode_elements = driver.find_elements(By.XPATH, xpath)
        if not episode_elements:
            break
        existing_episode_numbers.append(int(episode_elements[0].text))
    
    if not existing_episode_numbers:
        filtered_data = data
    else:
        existing_episodes_in_file = [int(line.strip().split(';')[0]) for line in data]
        common_episodes = list(set(existing_episode_numbers) & set(existing_episodes_in_file))
        print(f'Episodes already exist: {common_episodes}')
        print()

        filtered_data = []
        for line in data:
            episode_number = int(line.strip().split(';')[0])
            if episode_number not in existing_episode_numbers:
                filtered_data.append(line)

    successful_lines = []
    failed_lines = []
    
    for index, line in enumerate(filtered_data):
        try:
            episode_number, date, duration, topic, description = line.strip().split(';', maxsplit=4)

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

            driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_name_text_input_field"]').send_keys(topic)
            
            time.sleep(1)
            
            driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_overview_text_box_field"]').send_keys(description)

            air_date_field = driver.find_element(By.XPATH, '//*[@id="air_date_date_picker_field"]')
            air_date_field.clear()
            air_date_field.send_keys(date)

            driver.find_element(By.XPATH, f'//*[@id="{LANGUAGE_CODE}_runtime_text_input_field"]').send_keys(duration)

            save_button = driver.find_element(By.CLASS_NAME, 'k-grid-update')
            save_button.click()

            time.sleep(2)

            successful_lines.append(index)
            
            if index != 0:
                print(f'Successfully added episode: {episode_number}')
                data.remove(line)
                with open(DATA_FILE_PATH, 'w') as file:
                    for line in data:
                        file.write(line)

        except Exception as e:
            error_message = str(e).split('\n')[0]
            failed_lines.append(index)
            
            if index != 0:
                print(f'Failed to add episode: {episode_number}')

            
    with open(DATA_FILE_PATH, 'w') as file:
        for line in data:
            file.write(line)
    
    print()
    
    print(f'Total added: {len(successful_lines)}')
    print(f'Total failed: {len(failed_lines)}')
    
    if failed_lines:
        failed_episodes_str = 'Failed episodes:'
        for index in failed_lines:
            line = filtered_data[index]
            episode_number = line.strip().split(';')[0]
            failed_episodes_str += f' {episode_number}'
        print()
        print(failed_episodes_str)

except Exception as e:
    print(f'Unknown error')

driver.quit()
