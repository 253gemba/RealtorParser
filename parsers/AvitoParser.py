from base64 import b64decode
from io import BytesIO
from time import sleep

import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from parsers.ItemInfo import ItemInfo
from parsers.Parser import Parser

pytesseract.pytesseract.tesseract_cmd = r'D:\Programs\Tesseract\tesseract.exe'


class AvitoParser(Parser):
    def parse(self) -> list[ItemInfo]:
        info: list[ItemInfo] = []

        for page in range(1, 2):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            driver.get(f'https://www.avito.ru/sankt-peterburg/kvartiry?&s=104&p={page}')

            # Parsing
            cards = AvitoParser._get_cards(driver)
            for card in cards:
                ActionChains(driver).move_to_element(card).perform()
                info.append(AvitoParser._parse_card(card))
                sleep(3)

            driver.quit()

        return info
    
    @property
    def name(self):
        return 'Avito'

    @staticmethod
    def _get_cards(driver: WebDriver) -> list[WebElement]:
        return driver.find_elements(By.XPATH, "//div[@itemtype='http://schema.org/Product']")

    @staticmethod
    def _parse_card(card: WebElement) -> ItemInfo:
        # Show phone number
        has_phone = AvitoParser._show_number(card)

        divs = card.find_element(By.TAG_NAME, 'div').find_elements(By.XPATH, './*')

        card_link = divs[0].find_element(By.TAG_NAME, 'a').get_attribute('href')

        try:
            image_link = divs[0].find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_link = ''

        name = divs[1].find_element(By.TAG_NAME, 'a').text
        price = divs[1].find_element(By.XPATH, ".//span[@itemtype='http://schema.org/Offer']").text
        location = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").text.replace('\n', '; ')
        phone = AvitoParser._phone_number(card) if has_phone else ''

        return ItemInfo(card_link, image_link, name, price, location, phone)
    
    @staticmethod
    def _show_number(card: WebElement) -> bool:
        for _ in range(5):
            try:
                card.find_element(By.XPATH, ".//div[@data-marker='item-contact']").find_element(By.TAG_NAME, 'button').click()
                return True
            except NoSuchElementException:
                return False
            except ElementNotInteractableException:
                sleep(1)
        
        return False
    
    @staticmethod
    def _phone_number(card: WebElement) -> str:
        for _ in range(5):
            try:
                data = card.find_element(By.XPATH, ".//div[@data-marker='item-contact']").find_element(By.TAG_NAME, 'img').get_attribute('src')
                break
            except NoSuchElementException:
                sleep(1)
        else:
            return ''

        return pytesseract.image_to_string(Image.open(BytesIO(b64decode(data.replace('data:image/png;base64,', '')))))
