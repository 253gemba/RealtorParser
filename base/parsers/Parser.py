from abc import ABC, abstractmethod
from time import sleep
from typing import Callable, Type

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from ..models import RentOffer, SellOffer

Offer = SellOffer | RentOffer


class Parser(ABC):
    driver: WebDriver
    
    @property
    @abstractmethod
    def base_url(self) -> str:
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
        raise NotImplementedError

    @abstractmethod
    def parse_sell_card(self, card: WebElement) -> SellOffer:
        raise NotImplementedError
    
    @abstractmethod
    def parse_rent_card(self, card: WebElement) -> RentOffer:
        raise NotImplementedError
    
    def run(self):
        self._run(SellOffer, self.sell_url, self.get_cards, self.parse_sell_card)
        self._run(RentOffer, self.rent_url, self.get_cards, self.parse_rent_card)
    
    def scroll_down(self):
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

    def _run(self, model: Type[Offer], url: str, get_cards: Callable[[], list[WebElement]], parse_card: Callable[[WebElement], Offer]):
        offers: list[Offer] = []
        
        last_offer: Offer | None = model.objects.filter(card_link__startswith=self.base_url).first()

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get(self.base_url + url.format(page=1))

        cards = get_cards()
        for card in cards:
            offer = parse_card(card)

            if last_offer is not None and offer.card_link == last_offer.card_link:
                break

            offers.insert(0, offer)

        self.driver.close()
        
        for offer in offers:
            offer.save()
