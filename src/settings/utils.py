from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from settings import config


def get_selenium_driver():
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    driver = Chrome(service=Service(config.CHROME_DRIVER_PATH), options=options)
    return driver
