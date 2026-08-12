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

# 新版 TMDB 上传弹窗选择器
UPLOAD_MODAL_SELECTOR = '#image_upload_modal'
FILE_INPUT_SELECTOR = '#image_upload_modal #upload_files'
FILE_ITEM_SELECTOR = '#file_list .cropper_file_item'
IMAGE_CONTROLS_SELECTOR = '#image_controls'
UPLOAD_BUTTON_SELECTOR = '#btn_crop_upload'
MODAL_CLOSE_SELECTOR = '#image_upload_modal .modal_close'


def handle_cookie_popup():
    """处理 Cookie 弹窗"""
    try:
        cookie_banner = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "onetrust-banner-sdk"))
        )
        if cookie_banner.is_displayed():
            driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler").click()
            time.sleep(1)
    except Exception:
        pass


def is_upload_modal_visible():
    """检查上传弹窗是否可见"""
    try:
        modal = driver.find_element(By.CSS_SELECTOR, UPLOAD_MODAL_SELECTOR)
        return 'hidden' not in (modal.get_attribute('class') or '')
    except Exception:
        return False


def close_upload_modal():
    """关闭上传弹窗（上传成功后会自动刷新页面）"""
    if not is_upload_modal_visible():
        return

    # 上传成功后 imageUploadModalDirty=true，关闭时会触发 location.reload()
    upload_succeeded = driver.execute_script(
        'return typeof imageUploadModalDirty !== "undefined" && imageUploadModalDirty'
    )

    # 调用页面原生关闭函数，确保正确触发 reload 逻辑
    driver.execute_script("""
        if (typeof closeImageUploadModal === 'function') {
            closeImageUploadModal();
        } else {
            document.querySelector('#image_upload_modal .modal_close')?.click();
        }
    """)

    if upload_succeeded:
        # 等待页面刷新完成
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'k-input-button'))
        )
    else:
        # 未上传时仅隐藏弹窗，元素仍留在 DOM 中
        WebDriverWait(driver, 10).until(lambda d: not is_upload_modal_visible())


def wait_for_file_ready(timeout=20):
    """等待文件校验完成且无错误"""
    def file_ready(d):
        items = d.find_elements(By.CSS_SELECTOR, FILE_ITEM_SELECTOR)
        if not items:
            return False
        status = items[0].find_element(By.CSS_SELECTOR, '.file_status')
        status_class = status.get_attribute('class') or ''
        return 'error' not in status_class

    WebDriverWait(driver, timeout).until(file_ready)


def get_file_error_message():
    """获取文件列表中的错误信息"""
    try:
        status = driver.find_element(By.CSS_SELECTOR, f'{FILE_ITEM_SELECTOR} .file_status')
        if 'error' in (status.get_attribute('class') or ''):
            return status.text.strip()
    except Exception:
        pass
    return None


def is_auto_upload_enabled():
    """检查是否启用了自动上传"""
    try:
        checkbox = driver.find_element(By.CSS_SELECTOR, '#auto_upload')
        return checkbox.is_selected()
    except Exception:
        return True


def wait_for_image_controls(timeout=15):
    """等待裁剪控件显示（手动上传模式），必要时点击文件项"""
    controls = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, IMAGE_CONTROLS_SELECTOR))
    )
    if 'hidden' in (controls.get_attribute('class') or ''):
        driver.find_element(By.CSS_SELECTOR, FILE_ITEM_SELECTOR).click()

    WebDriverWait(driver, timeout).until(
        lambda d: 'hidden' not in (
            d.find_element(By.CSS_SELECTOR, IMAGE_CONTROLS_SELECTOR).get_attribute('class') or ''
        )
    )


def wait_for_upload_complete(timeout=120):
    """等待单张图片上传完成（文件状态变为 Uploaded）"""
    def upload_done(d):
        statuses = d.find_elements(By.CSS_SELECTOR, '#file_list .file_status')
        if not statuses:
            return False

        for status in statuses:
            status_class = status.get_attribute('class') or ''
            status_text = status.text.strip()
            if 'error' in status_class:
                raise RuntimeError(status_text or 'Upload failed')
            if 'success' in status_class or status_text == 'Uploaded':
                return True
        return False

    WebDriverWait(driver, timeout).until(upload_done)


def upload_backdrop(image_path):
    """通过新版裁剪弹窗上传剧照"""
    add_background_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "add_image") and contains(@class, "upload")]'))
    )
    add_background_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, FILE_INPUT_SELECTOR))
    )

    file_input = driver.find_element(By.CSS_SELECTOR, FILE_INPUT_SELECTOR)
    file_input.send_keys(os.path.abspath(image_path))

    wait_for_file_ready()

    error_message = get_file_error_message()
    if error_message:
        raise RuntimeError(error_message)

    # 启用 Auto upload 时，选文件后会自动上传，无需手动点击裁剪按钮
    if is_auto_upload_enabled():
        wait_for_upload_complete()
    else:
        wait_for_image_controls()
        upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, UPLOAD_BUTTON_SELECTOR))
        )
        upload_button.click()
        wait_for_upload_complete()

    close_upload_modal()


def set_backdrop_language():
    """为上传的剧照设置语言"""
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


try:
    driver = webdriver.Chrome()
    driver.get('https://www.themoviedb.org/login')

    # 登录 TMDB
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'username').send_keys(TMDB_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(TMDB_PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="login_button"]').click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//span[@class="avatar"]/a/img[@class="avatar"]'))
    )

    handle_cookie_popup()

    success_count = 0
    failure_count = 0

    image_files = sorted(
        os.listdir(IMAGE_FOLDER),
        key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf')
    )

    for image_file in image_files:
        if not image_file.split('.')[0].isdigit():
            continue

        episode_number = int(image_file.split('.')[0])
        image_path = os.path.join(IMAGE_FOLDER, f'{episode_number}.jpg')

        if not os.path.exists(image_path):
            continue

        episode_url = TV_SHOW_URL.format(episode_number=episode_number)
        driver.get(episode_url)

        try:
            upload_backdrop(image_path)
            success_count += 1
            os.remove(image_path)
            print(f'Successfully uploaded backdrop for episode {episode_number}')

            # 关闭弹窗时已自动刷新页面，直接设置语言
            set_backdrop_language()

        except Exception as e:
            failure_count += 1
            print(f'Failed to upload backdrop for episode {episode_number}: {e}')
            close_upload_modal()

    print(f'\nTotal uploaded: {success_count}')
    print(f'Total failed: {failure_count}')

except Exception as e:
    print(f'Error: {e}')

finally:
    driver.quit()
