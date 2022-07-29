from abc import ABC, abstractmethod
from models.RentOffer import RentOffer

from models.SellOffer import SellOffer
from xlsxwriter import Workbook


class Parser(ABC):
    @abstractmethod
    def parse_sell_offers(self) -> list[SellOffer]:
        raise NotImplementedError
    
    @abstractmethod
    def parse_rent_offers(self) -> list[RentOffer]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def run(self) -> None:
        sells = self.parse_sell_offers()
        rents = self.parse_rent_offers()
        self.save(sells, 'sells')
        self.save(rents, 'rents')
    
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
