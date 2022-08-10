from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..models import RentOffer, SellOffer
from .Parser import Parser


class YandexParser(Parser):
    @property
    def base_url(self) -> str:
        return 'https://realty.yandex.ru'
    
    @property
    def sell_url(self) -> str:
        return '/moskva_i_moskovskaya_oblast/kupit/kvartira/?sort=DATE_DESC'
    
    @property
    def rent_url(self) -> str:
        return '/moskva_i_moskovskaya_oblast/snyat/kvartira/?sort=DATE_DESC'
    
    def get_cards(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, 'OffersSerpItem')
    
    def parse_sell_card(self, card: WebElement) -> SellOffer | None:
        try:
            button = card.find_element(By.CLASS_NAME, 'Button__text')
        except NoSuchElementException:
            return None
        
        title = card.find_element(By.CLASS_NAME, 'OffersSerpItem__title').text 
        name = title.split(',')[-1].strip()
        area = float(title.split('м²')[0].replace(',', '.').replace(' ', ''))

        address = card.find_element(By.CLASS_NAME, 'OffersSerpItem__address').text

        try:
            metro = card.find_element(By.CLASS_NAME, 'MetroWithTime__body').text.replace('\n', '')
        except NoSuchElementException:
            metro = None
        
        price = int(card.find_element(By.CLASS_NAME, 'OffersSerpItem__price').text.replace(' ', '').replace('₽', ''))
        description = card.find_element(By.CLASS_NAME, 'OffersSerpItem__description').text

        floor_text = card.find_element(By.CLASS_NAME, 'OffersSerpItem__building').text.split(',')[-1].replace(' ', '').split('этажиз')
        floor = int(floor_text[0])
        floor_max = int(floor_text[1])

        card_link = card.find_element(By.CLASS_NAME, 'OffersSerpItem__link').get_attribute('href')
        link_image = card.find_element(By.CLASS_NAME, 'Gallery__activeImg').get_attribute('src')

        button.click()
        number = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@data-test='PhoneModalContactsPhoneShown']"))).text

        close_button = self.driver.find_element(By.CLASS_NAME, 'PhoneModal__closeIcon')
        close_button.click()

        return SellOffer(
            card_link=card_link,
            image_link=link_image,
            name=name,
            description=description,
            price=price,
            location=address,
            metro=metro,
            phone=number,
            area=area,
            floor=floor,
            floor_max=floor_max)
    
    def parse_rent_card(self, card: WebElement) -> RentOffer | None:
        try:
            button = card.find_element(By.CLASS_NAME, 'Button__text')
        except NoSuchElementException:
            return None
        
        title = card.find_element(By.CLASS_NAME, 'OffersSerpItem__title').text 
        name = title.split(',')[-1].strip()
        area = float(title.split('м²')[0].replace(',', '.').replace(' ', ''))

        address = card.find_element(By.CLASS_NAME, 'OffersSerpItem__address').text
        
        try:
            metro = card.find_element(By.CLASS_NAME, 'MetroWithTime__body').text.replace('\n', '')
        except NoSuchElementException:
            metro = None

        price_text = card.find_element(By.CLASS_NAME, 'OffersSerpItem__price').text.replace(' ', '').replace('₽', '').split('/')
        price = int(price_text[0])
        price_per = RentOffer.price_month if price_text[1] == 'мес.' else RentOffer.price_day

        description = card.find_element(By.CLASS_NAME, 'OffersSerpItem__description').text

        floor_text = card.find_element(By.CLASS_NAME, 'OffersSerpItem__building').text.split(',')[-1].replace(' ', '').split('этажиз')
        floor = int(floor_text[0])
        floor_max = int(floor_text[1])

        card_link = card.find_element(By.CLASS_NAME, 'OffersSerpItem__link').get_attribute('href')
        link_image = card.find_element(By.CLASS_NAME, 'Gallery__activeImg').get_attribute('src')

        button.click()
        number = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@data-test='PhoneModalContactsPhoneShown']"))).text

        close_button = self.driver.find_element(By.CLASS_NAME, 'PhoneModal__closeIcon')
        close_button.click()

        return RentOffer(
            card_link=card_link,
            image_link=link_image,
            name=name,
            description=description,
            price=price,
            price_per=price_per,
            location=address,
            metro=metro,
            phone=number,
            area=area,
            floor=floor,
            floor_max=floor_max)
