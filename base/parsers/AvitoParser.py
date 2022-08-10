from base64 import b64decode
from io import BytesIO
from time import sleep

import pytesseract
from PIL import Image
from RealtorParser.config import config
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..models import RentOffer, SellOffer
from .Parser import Parser

pytesseract.pytesseract.tesseract_cmd = config['APP']['tesseract_path']


class AvitoParser(Parser):
    @property
    def base_url(self):
        return 'https://www.avito.ru'
    
    @property
    def sell_url(self) -> str:
        return '/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?p={page}&s=104'
    
    @property
    def rent_url(self) -> str:
        return '/sankt-peterburg/kvartiry/sdam-ASgBAgICAUSSA8gQ?p={page}&s=104'
    
    def get_cards(self) -> list[WebElement]:
        return self.driver\
            .find_element(By.XPATH, ".//div[@elementtiming='bx.catalog.container']")\
            .find_element(By.TAG_NAME, 'div')\
            .find_elements(By.XPATH, "./div[@itemtype='http://schema.org/Product']")
    
    def parse_sell_card(self, card: WebElement) -> SellOffer | None:
        ActionChains(self.driver).move_to_element(card).perform()

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
        description = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']/following-sibling::div").text
        
        try:
            metro = divs[1]\
                .find_element(By.XPATH, ".//div[@data-marker='item-address']")\
                .find_element(By.TAG_NAME, 'div')\
                .find_element(By.TAG_NAME, 'div').text\
                .replace('\n', ' ')
        except NoSuchElementException:
            metro = None

        phone = self._get_number(card)
        sleep(1)
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
    
    def parse_rent_card(self, card: WebElement) -> RentOffer | None:
        ActionChains(self.driver).move_to_element(card).perform()

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

        price_text = divs[1].find_element(By.XPATH, ".//span[@itemtype='http://schema.org/Offer']").text
        price = int(price_text.split('₽')[0].replace(' ', ''))
        price_per = RentOffer.price_day if price_text.split('₽')[1].strip().endswith('сутки') else RentOffer.price_month

        location = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").find_element(By.TAG_NAME, 'span').text
        description = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']/following-sibling::div").text
        
        try:
            metro = divs[1].find_element(By.XPATH, ".//div[@data-marker='item-address']").find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').text
        except NoSuchElementException:
            metro = None
        
        phone = self._get_number(card)
        sleep(1)
        return RentOffer(
            card_link=card_link,
            image_link=image_link,
            name=name,
            description=description,
            price=price,
            price_per=price_per,
            location=location,
            metro=metro,
            phone=phone,
            area=area,
            floor=floor,
            floor_max=floor_max) 
    
    def _get_number(self, card: WebElement) -> str | None:
        try:
            button = card.find_element(By.XPATH, ".//div[@data-marker='item-contact']").find_element(By.TAG_NAME, 'button')
        except NoSuchElementException:
            return None
        
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button))
        button.click()

        phone_img = WebDriverWait(self.driver, 5).until(
            lambda _: card \
                .find_element(By.XPATH, ".//div[@data-marker='item-contact']") \
                .find_element(By.TAG_NAME, 'img') \
                .get_attribute('src')) \
            .replace('data:image/png;base64,', '')
        return pytesseract.image_to_string(Image.open(BytesIO(b64decode(phone_img))))
