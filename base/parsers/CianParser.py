from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..models import RentOffer, SellOffer
from .Parser import Parser


class CianParser(Parser):
    @property
    def base_url(self) -> str:
        return 'https://spb.cian.ru'

    @property
    def sell_url(self) -> str:
        return '/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={page}&region=2&sort=creation_date_desc'
    
    @property
    def rent_url(self) -> str:
        return '/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={page}&region=2&sort=creation_date_desc&type=4'

    def get_cards(self) -> list[WebElement]:
        return self.driver.find_elements(By.XPATH, ".//article[@data-name='CardComponent']")

    def parse_sell_card(self, card: WebElement) -> SellOffer:
        # Show phone number
        card.find_element(By.XPATH, ".//button[@data-mark='PhoneButton']").click()
        card_link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

        try:
            image_link = card.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_link = None
        
        try:
            title = card.find_element(By.XPATH, ".//span[@data-mark='OfferSubtitle']").text
            if not title.endswith('этаж'):
                raise NoSuchElementException
        except NoSuchElementException:
            title = card.find_element(By.XPATH, ".//span[@data-mark='OfferTitle']").text

        name = title.split(', ')[0]
        area = float(title[len(name) + 2:].split(' м²')[0].replace(',', '.'))
        floor = int(title.split(', ')[-1].split('/')[0])
        floor_max = int(title.split(',')[-1].split('/')[-1].removesuffix(' этаж'))
        try:
            description = card.find_element(By.XPATH, ".//div[@data-name='Description']").text
        except NoSuchElementException:
            description = None
        price = int(card.find_element(By.XPATH, ".//span[@data-mark='MainPrice']").text.replace('₽', '').replace(' ', ''))
        location = ', '.join([geo.text for geo in card.find_elements(By.XPATH, ".//a[@data-name='GeoLabel']")])
        metro = card.find_element(By.XPATH, ".//div[@data-name='SpecialGeo']").text.replace('\n', ' ')
        sleep(2)
        phone = card.find_element(By.XPATH, ".//span[@data-mark='PhoneValue']").text
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

    def parse_rent_card(self, card: WebElement) -> RentOffer:
        # Show phone number
        try:
            card.find_element(By.XPATH, ".//button[@data-mark='PhoneButton']").click()
            has_phone = True
        except NoSuchElementException:
            has_phone = False
        
        card_link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

        try:
            image_link = card.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except NoSuchElementException:
            image_link = None
        
        try:
            title = card.find_element(By.XPATH, ".//span[@data-mark='OfferSubtitle']").text
            if not title.endswith('этаж'):
                raise NoSuchElementException
        except NoSuchElementException:
            title = card.find_element(By.XPATH, ".//span[@data-mark='OfferTitle']").text

        name = title.split(', ')[0]
        area = float(title[len(name) + 2:].split(' м²')[0].replace(',', '.'))
        floor = int(title.split(', ')[-1].split('/')[0])
        floor_max = int(title.split(',')[-1].split('/')[-1].removesuffix(' этаж'))
        try:
            description = card.find_element(By.XPATH, ".//div[@data-name='Description']").text
        except NoSuchElementException:
            description = None
        price = int(card.find_element(By.XPATH, ".//span[@data-mark='MainPrice']").text.replace('₽', '').replace(' ', '').split('/')[0])
        price_per = RentOffer.price_month if card.find_element(By.XPATH, ".//span[@data-mark='MainPrice']").text.replace('₽', '').replace(' ', '').split('/')[1].endswith('мес.') else RentOffer.price_day
        location = ', '.join([geo.text for geo in card.find_elements(By.XPATH, ".//a[@data-name='GeoLabel']")])
        metro = card.find_element(By.XPATH, ".//div[@data-name='SpecialGeo']").text.replace('\n', ' ')

        phone = None
        if has_phone:
            sleep(2)
            phone = card.find_element(By.XPATH, ".//span[@data-mark='PhoneValue']").text
        
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
