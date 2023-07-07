from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re

TMDB_USERNAME = 'your_username'
TMDB_PASSWORD = 'your_password'
EPISODE_URL = 'https://www.themoviedb.org/tv/229116-dust/season/0/episode/1/images/backdrops'
IMAGE_FOLDER = '/path/to/covers'
LANGUAGE = 'English'

match = re.search(r'(https://www.themoviedb.org/tv/[\w-]+/season/\d+/episode/)\d+', EPISODE_URL)
TV_SHOW_URL = match.group(1) + '{episode_number}/images/backdrops'

try:
    driver = webdriver.Chrome()
    driver.get('https://www.themoviedb.org/login')

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))

    driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)

    driver.find_element(By.XPATH, '//*[@id="login_button"]').click()

    success_count = 0
    failure_count = 0

    image_files = sorted(os.listdir(IMAGE_FOLDER), key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))
    
    for image_file in image_files:
        if not image_file.split('.')[0].isdigit():
            continue
        
        episode_number = int(image_file.split('.')[0])
        
        episode_url = TV_SHOW_URL.format(episode_number=episode_number)
        driver.get(episode_url)

        add_background_button = driver.find_element(By.XPATH, '//*[@id="media_v4"]/div[3]/div/div[1]/div[1]/h3/div/a[2]/span')
        add_background_button.click()

        select_file_button = driver.find_element(By.XPATH, '//*[@id="upload_window"]/section/div/div/div/div')
        select_file_button.click()

        image_path = f'{IMAGE_FOLDER}/{episode_number}.jpg'
        
        if not os.path.exists(image_path):
            continue
        
        script = f'''
        tell application "Google Chrome"
            activate
            tell application "System Events"
                keystroke "g" using {{command down, shift down}}
                delay 1
                keystroke "{image_path}"
                delay 1
                keystroke return
                delay 1
                keystroke return
            end tell
        end tell
        '''
        os.system(f"osascript -e '{script}'")
        
        time.sleep(3)
        
        try:
            error_message = driver.find_element(By.CSS_SELECTOR, '.error_message')
            failure_count += 1
            
            print(f'Failed to upload cover for episode {episode_number}: {error_message.text}')
            
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
            
            print(f'Successfully uploaded cover for episode {episode_number}')

        driver.refresh()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-owns^="image_language"] .k-select')))

        language_dropdown_button = driver.find_element(By.CSS_SELECTOR, '[aria-owns^="image_language"] .k-select')

        language_dropdown_button.click()

        language_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-owns^="image_language"]')
        language_input.send_keys(LANGUAGE)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//li[contains(text(), "{LANGUAGE}")]')))
        language_option = driver.find_element(By.XPATH, f'//li[contains(text(), "{LANGUAGE}")]')
        language_option.click()
        
        time.sleep(1)
    
    print(f'Total success: {success_count}')
    print(f'Total failure: {failure_count}')

except Exception as e:
    print(f'Error: {e}')

driver.quit()
