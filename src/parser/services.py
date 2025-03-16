import logging

from lxml import html
from selenium.common import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from db.connection import DatabaseConnection
from db.dals import SitesDAL
from parser.utils import clean_price, get_avg_price
from settings.utils import get_selenium_driver

logger = logging.getLogger(__name__)


async def get_prices_by_site():
    # url_prices_map структура:
    # {
    #   'https://website.domain/zyuzyublicates/': [399.0, 322.0],
    #   'https://best-zyuzublics.domain/prices/': [869.0, 1205.0, 892,0],
    # }
    url_prices_map: dict[str, list] = {}
    async with DatabaseConnection() as db:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        with get_selenium_driver() as driver:
            async for site in SitesDAL(db=db).select():
                logger.info("Парсинг записи: %s", site)
                try:
                    price = await get_price(driver=driver, url=str(site.url), xpath=site.xpath)
                except TimeoutException as e:
                    logger.debug("TimeoutException. Запись: %s", site)
                    continue
                url_prices_map.setdefault(str(site.url), []).append(price)
    return url_prices_map


async def get_avg_prices_by_site() -> dict[str, float]:
    url_prices_map = await get_prices_by_site()
    avg_prices: dict[str, float] = {}
    for url, prices in url_prices_map.items():
        avg_prices[url] = get_avg_price(prices=prices)

    return avg_prices


async def get_price(driver: WebDriver, url: str, xpath: str) -> float:
    driver.get(url)

    try:
        # Ждем пока не появится на странице нужный XPATH (10 сек)
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        page_content = driver.page_source
    except TimeoutException as e:
        logger.warning('Превышен лимит ожидания элемента (xpath=%s) на странице (url=%s)', xpath, url)
        raise e from None

    price = html.fromstring(page_content).xpath(xpath)
    price = price[0].text_content().strip()
    cleaned_price = clean_price(price=price)

    return cleaned_price
