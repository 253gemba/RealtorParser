from abc import ABC, abstractmethod
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from ..models import RentOffer, SellOffer


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
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            self.driver.get(self.sell_url.format(page=page))

            cards = self.get_cards()
            for card in cards:
                sells.append(self.parse_sell_card(card))

            self.driver.close()
        
        for sell in sells:
            sell.save()

        # Rents parsing
        rents: list[RentOffer] = []
        for page in range(1, 2):
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            self.driver.get(self.rent_url.format(page=page))

            cards = self.get_cards()
            for card in cards:
                rents.append(self.parse_rent_card(card))

            self.driver.close()
        
        for rent in rents:
            rent.save()
    
    def scroll_down(self) -> None:
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
