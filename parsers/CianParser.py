from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from parsers.ItemInfo import ItemInfo
from parsers.Parser import Parser


class CianParser(Parser):
    def parse(self) -> list[ItemInfo]:
        info: list[ItemInfo] = []

        for page in range(1, 2):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            driver.implicitly_wait(30)
            driver.get(f'https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={page}&region=2&sort=creation_date_desc')

            # Scrolling
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)

            # Parsing
            cards = CianParser._get_cards(driver)
            for card in cards:
                info.append(CianParser._parse_card(card))
            
            driver.close()

        return info

    @property
    def name(self):
        return 'Cian'
    
    @staticmethod
    def _get_cards(driver: WebDriver) -> list[WebElement]:
        return driver.find_elements(By.XPATH, ".//article[@data-name='CardComponent']")
    
    @staticmethod
    def _parse_card(card: WebElement) -> ItemInfo:
        # Show phone number
        card.find_element(By.XPATH, ".//button[@data-mark='PhoneButton']").click()
        card_link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

        try:
            image_link = card.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_link = ''
            
        name = card.find_element(By.XPATH, ".//span[@data-mark='OfferTitle']").text
        price = card.find_element(By.XPATH, ".//span[@data-mark='MainPrice']").text
        location = ', '.join([geo.text for geo in card.find_elements(By.XPATH, ".//a[@data-name='GeoLabel']")]) + '; '+ \
            card.find_element(By.XPATH, ".//div[@data-name='SpecialGeo']").text
        phone = card.find_element(By.XPATH, ".//span[@data-mark='PhoneValue']").text

        return ItemInfo(card_link, image_link, name, price, location, phone)
