from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from parsers.ItemInfo import ItemInfo
from parsers.Parser import Parser


class OzonParser(Parser):
    @property
    def name(self) -> str:
        return 'Ozon'

    def parse(self) -> list[ItemInfo]:
        info: list[ItemInfo] = []
        
        for page in range(1, 2):
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
            driver.implicitly_wait(30)
            driver.get(f'https://www.ozon.ru/category/smartfony-15502/?page={page}')
            
            # Scrolling
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
            
            # Parsing
            cards = OzonParser._get_cards(driver)
            for card in cards:
                info.append(OzonParser._parse_card(card))

            driver.quit()
        
        return info
    
    @staticmethod
    def _get_cards(driver: WebDriver) -> list[WebElement]:
        '''
        Returns card container
        '''
        container = driver.find_element(By.CLASS_NAME, 'widget-search-result-container').find_element(By.XPATH, './*')
        cards = container.find_elements(By.XPATH, './*')
        return list(filter(lambda c: c.get_attribute('class') == cards[0].get_attribute('class'), cards)) # Removing an empty div

    @staticmethod
    def _parse_card(card: WebElement) -> ItemInfo:
        divs = card.find_elements(By.XPATH, './*')
        
        card_link = divs[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
        image_link = divs[0].find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'img').get_attribute('src')
        name = divs[1].find_element(By.TAG_NAME, 'a').text
        price = divs[2].find_element(By.TAG_NAME, 'span').text
        return ItemInfo(card_link, image_link, name, price)
