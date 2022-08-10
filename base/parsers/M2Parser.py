from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..models import RentOffer, SellOffer
from .Parser import Parser


class M2Parser(Parser):
    @property
    def base_url(self) -> str:
        return 'https://m2.ru'
    
    @property
    def sell_url(self) -> str:
        return '/moskva/nedvizhimost/kupit-kvartiru/?sort=date'
    
    @property
    def rent_url(self) -> str:
        return '/moskva/nedvizhimost/snyat-kvartiru/?sort=date'
    
    def get_cards(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, 'OffersSearchList__item')
    
    def parse_sell_card(self, card: WebElement) -> SellOffer | None:
        ActionChains(self.driver).move_to_element(card).perform()

        try:
            title = card.find_element(By.CLASS_NAME, 'LayoutSnippet__title').find_element(By.CLASS_NAME, 'LinkSnippet')
        except NoSuchElementException:
            return None
        
        name = title.text.split(',')[-2].strip()
        area = float(title.text.split('м²')[0].replace(',', '.').replace(' ', ''))
        card_link = title.get_attribute('href')
        
        floor_text = title.text.split(',')[-1].replace('этаж', '').replace(' ', '').split('/')
        floor = int(floor_text[0])
        floor_max = int(floor_text[1])

        address = card.find_element(By.CLASS_NAME, 'LayoutSnippet__address').text.replace('\n', ' ').replace('  • ', ';')
        metro = card.find_element(By.CLASS_NAME, 'OfferRouteCard').text.replace('\n', ' ')
        image_link = card.find_element(By.CLASS_NAME, 'ImageLazySeo__img').get_attribute('src')
        price = int(card.find_element(By.CLASS_NAME, 'Price').text.replace('₽', '').replace(' ', ''))
        description = None

        button = card.find_element(By.XPATH, ".//button[@data-test='phone-button']")
        button.click()
        close_button = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//button[@aria-label='Закрыть']")))
        
        number = close_button.find_element(By.XPATH, "..").find_element(By.TAG_NAME, 'a').text

        close_button.click()
        return SellOffer(
            card_link=card_link,
            image_link=image_link,
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
        ActionChains(self.driver).move_to_element(card).perform()

        try:
            title = card.find_element(By.CLASS_NAME, 'LayoutSnippet__title').find_element(By.CLASS_NAME, 'LinkSnippet')
        except NoSuchElementException:
            return None
        
        name = title.text.split(',')[-2].strip()
        area = float(title.text.split('м²')[0].replace(',', '.').replace(' ', ''))
        card_link = title.get_attribute('href')
        
        floor_text = title.text.split(',')[-1].replace('этаж', '').replace(' ', '').split('/')
        floor = int(floor_text[0])
        floor_max = int(floor_text[1])

        address = card.find_element(By.CLASS_NAME, 'LayoutSnippet__address').text.replace('\n', ' ').replace('  • ', ';')
        metro = card.find_element(By.CLASS_NAME, 'OfferRouteCard').text.replace('\n', ' ')
        image_link = card.find_element(By.CLASS_NAME, 'ImageLazySeo__img').get_attribute('src')
        description = None

        price_text = card.find_element(By.CLASS_NAME, 'Price').text.replace('₽', '').replace(' ', '').split('/')
        price = int(price_text[0])
        price_per = RentOffer.price_month if price_text[1] == 'мес.' else RentOffer.price_day

        button = card.find_element(By.XPATH, ".//button[@data-test='phone-button']")
        button.click()
        close_button = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//button[@aria-label='Закрыть']")))
        
        number = close_button.find_element(By.XPATH, "..").find_element(By.TAG_NAME, 'a').text
        
        close_button.click()
        return RentOffer(
            card_link=card_link,
            image_link=image_link,
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
