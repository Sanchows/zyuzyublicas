from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from settings import config


def get_selenium_driver():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    if config.PROD:
        driver = Remote(f"http://{config.SELENIUM_HOST}:{config.SELENIUM_PORT}/wd/hub", options=options)
    else:
        driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
