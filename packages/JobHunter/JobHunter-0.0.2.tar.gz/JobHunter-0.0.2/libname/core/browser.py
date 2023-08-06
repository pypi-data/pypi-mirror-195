import os
import random
import tempfile
import time
import traceback
import uuid

import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_profiles_path():
    return tempfile.gettempdir() if os.getenv('CHROME_PROFILE_DIRECTORY', '') == '' else os.getenv(
        'CHROME_PROFILE_DIRECTORY')


def get_profile_directory(email):
    return os.path.join(get_profiles_path(), email)


class Browser:

    def __init__(self, email=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('test-type')
        chrome_options.add_argument('start-maximized')  # open Browser in maximized mode
        chrome_options.add_argument('disable-infobars')  # disabling infobars
        chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
        chrome_options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        # chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
        if email:
            chrome_options.add_argument("--user-data-dir={}".format(get_profile_directory(email)))
        chrome_options.add_argument("-homepage \"about:blank\"")

        chromedriver_autoinstaller.install()
        try:
            self.driver: WebDriver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            traceback.print_exc()
            if 'This version of ChromeDriver only supports Chrome version' in e.msg:
                raise Exception('Update Chromedriver Version')
            else:
                raise Exception("Failed to Launch Browser")

        self.wait_driver = WebDriverWait(self.driver, 60)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                                    dict(
                                        source="console.log('Setting Webdriver Property to undefined');Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"))

    def open_url(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def wait_and_click(self, locator):
        web_element = self.wait_driver.until(
            EC.visibility_of_element_located(
                locator)
        )
        web_element.click()

    def wait_and_click(self, locator):
        web_element = self.wait_driver.until(
            EC.visibility_of_element_located(
                locator)
        )
        web_element.click()

    def wait_and_js_click(self, locator):
        web_element = self.wait_driver.until(
            EC.visibility_of_element_located(
                locator)
        )

        self.js_click(web_element)

    def js_click(self, web_element):
        self.driver.execute_script("arguments[0].click();", web_element)

    def slow_type(self, web_element, value):
        web_element.clear()
        for c in str(value):
            web_element.send_keys(c)
            time.sleep(float(random.randint(0, 10) / 10))

    def wait_and_slow_type(self, locator, value):

        web_element = self.wait_driver.until(
            EC.visibility_of_element_located(
                locator)
        )
        ActionChains(self.driver).move_to_element(web_element).click(web_element).perform()
        self.slow_type(web_element, value)

    def wait_and_type(self, locator, value):
        web_element = self.wait_driver.until(
            EC.visibility_of_element_located(
                locator)
        )
        web_element.clear()
        web_element.send_keys(value)

    def wait_for_invisibility(self, locator):
        self.wait_driver.until(EC.invisibility_of_element_located(locator))

    def wait_for_visibility(self, locator):
        return self.wait_driver.until(EC.visibility_of_element_located(locator))

    def wait_and_switch_to_frame(self, locator):
        self.wait_driver.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def get_bs4_page(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.page_source, 'html.parser')


    def reload_page(self):
        self.driver.refresh()

    def take_screen_shot(self):
        # try:
        #     self.driver.execute_script("document.querySelector('#vf-root > div >div').style.background = 'black';")
        # except JavascriptException:
        #     print('Failed to set the background color.')

        screen_shot_path = os.path.join(tempfile.gettempdir(), f'{str(uuid.uuid4())}.png')
        self.driver.save_screenshot(screen_shot_path)
        return screen_shot_path

    def get_field_value(self, locator) -> str:
        web_element = self.wait_driver.until(
            EC.visibility_of_element_located(
                locator)
        )
        return web_element.get_attribute('value')


    def get_screen_shot_url(self):
        try:
            screen_shot_path = self.take_screen_shot()
            screenshot_url = upload_to_aws(screen_shot_path)
            if screenshot_url:
                os.remove(screen_shot_path)
            return screenshot_url
        except Exception as e:
            print('Failed to take the screenshot')

    def send_keys(self, keys: Keys):
        ActionChains(self.driver).send_keys(keys).perform()

    def clear_cache_and_cookies(self):
        self.driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
