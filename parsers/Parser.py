from abc import ABC, abstractmethod

from xlsxwriter import Workbook

from parsers.ItemInfo import ItemInfo


class Parser(ABC):
    @abstractmethod
    def parse(self) -> list[ItemInfo]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def run(self) -> None:
        data = self.parse()
        self.save(data)
    
    def save(self, data: list[ItemInfo]):
        file = Workbook(f'data/{self.name}.xlsx')
        page = file.add_worksheet(self.name)

        for row, item in enumerate(data):
            page.write(row, 0, item.name)
            page.write(row, 1, item.price)
            page.write(row, 2, item.location)
            page.write(row, 3, item.phone)
            page.write(row, 4, item.card_link)
            page.write(row, 5, item.image_link)
        
        file.close()
