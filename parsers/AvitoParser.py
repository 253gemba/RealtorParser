from base64 import b64decode
from io import BytesIO
from time import sleep

import pytesseract
from config import config
from models.RentOffer import RentOffer
from models.SellOffer import SellOffer
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

from parsers.Parser import Parser

pytesseract.pytesseract.tesseract_cmd = config['APP']['tesseract_path']


class AvitoParser(Parser):
    def parse_sell_offers(self) -> list[SellOffer]:
        info: list[SellOffer] = []

        for page in range(1, 2):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            driver.get(f'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?p={page}&s=104')     

            # Parsing
            cards = AvitoParser._get_cards(driver)
            for card in cards:
                ActionChains(driver).move_to_element(card).perform()
                info.append(AvitoParser._parse_sell_card(card))
                sleep(3)

            driver.quit()

        return info
    
    def parse_rent_offers(self) -> list[RentOffer]:
        info: list[RentOffer] = []

        for page in range(1, 2):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            driver.get(f'https://www.avito.ru/sankt-peterburg/kvartiry/sdam-ASgBAgICAUSSA8gQ?p={page}&s=104')     

            # Parsing
            cards = AvitoParser._get_cards(driver)
            for card in cards:
                ActionChains(driver).move_to_element(card).perform()
                info.append(AvitoParser._parse_rent_card(card))
                sleep(3)

            driver.quit()

        return info
    
    @property
    def name(self):
        return 'Avito'

    @staticmethod
    def _get_cards(driver: WebDriver) -> list[WebElement]:
        return driver\
            .find_element(By.XPATH, ".//div[@elementtiming='bx.catalog.container']")\
            .find_element(By.TAG_NAME, 'div')\
            .find_elements(By.XPATH, "./div[@itemtype='http://schema.org/Product']")

    @staticmethod
    def _parse_sell_card(card: WebElement) -> SellOffer:
        # Show phone number
        has_phone = AvitoParser._show_number(card)

        divs = card.find_element(By.TAG_NAME, 'div').find_elements(By.XPATH, './*')

        card_link = divs[0].find_element(By.TAG_NAME, 'a').get_attribute('href')

        try:
            image_link = divs[0].find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_link = None

        title = divs[1].find_element(By.TAG_NAME, 'a').text
        name = title.split(', ')[0]
        area = float(title[len(name) + 2:].split(' м²')[0].replace(',', '.'))
        floor = int(title.split(', ')[-1].split('/')[0])
        floor_max = int(title.split(',')[-1].split('/')[-1].removesuffix(' эт.'))
        price = int(divs[1].find_element(By.XPATH, ".//span[@itemtype='http://schema.org/Offer']").text.replace('₽', '').replace(' ', ''))
        
        location = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").find_element(By.TAG_NAME, 'span').text
        
        try:
            metro = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').text
        except NoSuchElementException:
            metro = None
        
        phone = AvitoParser._phone_number(card) if has_phone else None
        description = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']/following-sibling::div").text

        return SellOffer(
            card_link=card_link,
            image_link=image_link,
            name=name,
            description=description,
            price=price,
            location=location,
            metro=metro,
            phone=phone,
            area=area,
            floor=floor,
            floor_max=floor_max) 

    @staticmethod
    def _parse_rent_card(card: WebElement) -> RentOffer:
        # Show phone number
        has_phone = AvitoParser._show_number(card)

        divs = card.find_element(By.TAG_NAME, 'div').find_elements(By.XPATH, './*')

        card_link = divs[0].find_element(By.TAG_NAME, 'a').get_attribute('href')

        try:
            image_link = divs[0].find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_link = None

        title = divs[1].find_element(By.TAG_NAME, 'a').text
        name = title.split(', ')[0]
        area = float(title[len(name) + 2:].split(' м²')[0].replace(',', '.'))
        floor = int(title.split(', ')[-1].split('/')[0])
        floor_max = int(title.split(',')[-1].split('/')[-1].removesuffix(' эт.'))
        price = divs[1].find_element(By.XPATH, ".//span[@itemtype='http://schema.org/Offer']").text
        location = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").find_element(By.TAG_NAME, 'span').text
        
        try:
            metro = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').text
        except NoSuchElementException:
            metro = None
        
        phone = AvitoParser._phone_number(card) if has_phone else None
        description = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']/following-sibling::div").text

        return RentOffer(
            card_link=card_link,
            image_link=image_link,
            name=name,
            description=description,
            price=price,
            location=location,
            metro=metro,
            phone=phone,
            area=area,
            floor=floor,
            floor_max=floor_max) 
    
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
