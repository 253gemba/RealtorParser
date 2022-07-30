from abc import ABC, abstractmethod
from time import sleep

from models.RentOffer import RentOffer
from models.SellOffer import SellOffer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from xlsxwriter import Workbook


class Parser(ABC):
    driver: WebDriver
    
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def sell_url(self) -> str:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def rent_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_cards(self) -> list[WebElement]:
        pass

    @abstractmethod
    def parse_sell_card(self, card: WebElement) -> SellOffer:
        raise NotImplementedError
    
    @abstractmethod
    def parse_rent_card(self, card: WebElement) -> RentOffer:
        raise NotImplementedError
    
    def run(self) -> None:
        # Sells parsing
        sells: list[SellOffer] = []
        for page in range(1, 2):
            # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Remote('http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME, options=options)
            self.driver.get(self.sell_url.format(page=page))

            cards = self.get_cards()
            for card in cards:
                sells.append(self.parse_sell_card(card))

            self.driver.close()
                
        # Rents parsing
        rents: list[RentOffer] = []
        for page in range(1, 2):
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            self.driver.get(self.rent_url.format(page=page))

            cards = self.get_cards()
            for card in cards:
                rents.append(self.parse_rent_card(card))

            self.driver.close()
        
        # Save
        self.save(sells, 'sells')
        self.save(rents, 'rents')
    
    def scroll_down(self) -> None:
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
    
    def save(self, data: list[SellOffer], name: str):
        file = Workbook(f'data/{self.name}_{name}.xlsx')
        page = file.add_worksheet(self.name)
        
        # Title
        page.write(0, 0, 'Card Link')
        page.write(0, 1, 'Image Link')
        page.write(0, 2, 'Name')
        page.write(0, 3, 'Description')
        page.write(0, 4, 'Price')
        page.write(0, 5, 'Location')
        page.write(0, 6, 'Metro')
        page.write(0, 7, 'Phone')
        page.write(0, 8, 'Area')
        page.write(0, 9, 'Floor')
        page.write(0, 10, 'Floor Max')

        # Data
        for row, item in enumerate(data, 1):
            page.write(row, 0, item.card_link)
            page.write(row, 1, item.image_link)
            page.write(row, 2, item.name)
            page.write(row, 3, item.description)
            page.write(row, 4, item.price)
            page.write(row, 5, item.location)
            page.write(row, 6, item.metro)
            page.write(row, 7, item.phone)
            page.write(row, 8, item.area)
            page.write(row, 9, item.floor)
            page.write(row, 10, item.floor_max)

        file.close()
