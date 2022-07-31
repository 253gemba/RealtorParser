from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from parsers.Parser import Parser

from ..models import RentOffer, SellOffer


class DomclickParser(Parser):
    @property
    def name(self) -> str:
        return 'Domclick'

    @property
    def sell_url(self) -> str:
        return 'https://spb.domclick.ru/search?deal_type=sale&category=living&sort=published&sort_dir=desc&offset={page}0'
    
    @property
    def rent_url(self) -> str:
        return 'https://spb.domclick.ru/search?deal_type=rent&category=living&sort=published&sort_dir=desc&offset={page}0'
    
    def get_cards(self) -> list[WebElement]:
        self.scroll_down()
        return self.driver.find_elements(By.XPATH, ".//div[@data-test='product-snippet']")
    
    def parse_sell_card(self, card: WebElement) -> SellOffer:
        return super().parse_sell_card(card)
    
    def parse_rent_card(self, card: WebElement) -> RentOffer:
        return super().parse_rent_card(card)
