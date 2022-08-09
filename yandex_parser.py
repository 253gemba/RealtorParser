from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def record_data(data):
    list_data = []
    list_data.append(data)
    print(data)
    return list_data


def get_data():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://realty.yandex.ru/moskva_i_moskovskaya_oblast/kupit/kvartira/vtorichniy-rynok-i-bez-posrednikov/')

    cards = driver.find_elements(By.XPATH, ".//button[@data-test='ItemShowPhone']")

    i = 0
    for card in cards:
        i += 1
        try:
            button = card.find_element(By.CLASS_NAME, 'Button__text')
        except NoSuchElementException:
            continue

        button.click()

        number = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@data-test='PhoneModalContactsPhoneShown']"))).text

        name = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located(
            (By.XPATH, ".//div[@class='AuthorName__wrapper--2BsYR PhoneModalPerson__name--2d1CW']"))).text

        adress = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@class='PhoneModalOffer__address']"))).text

        price = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@class='Price PhoneModalOffer__price']"))).text\
            .replace(' ', '').replace('₽', '')
        price = int(price)

        description = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@class='PhoneModalOffer__info']"))).text

        area = description.split('м²')[0]
        if ',' in area:
            area = float(area.replace(',', '.'))
        else:
            area = int(area)

        floor = description.split(',')[-1].split(' этаж из ')[0].replace('студия', '')
        if 'комнатная' in floor:
            floor = int(floor.split('комнатная')[-1])
        else:
            floor = int(floor)

        floor_max = int(description.split(',')[-1].split(' этаж из ')[1])

        card_link = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@class='PhoneModalOffer']/a"))).get_attribute('href')

        link_image = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.XPATH, ".//div[@class='PhoneModalOffer']/a/div"))) \
            .get_attribute('style').replace('background-image: url("', 'https:').replace('");', '')

        close_button = driver.find_element(By.CLASS_NAME, 'PhoneModal__closeIcon')
        close_button.click()

        record_data([name, number, price, adress, area, floor, floor_max, card_link, link_image])

    driver.close()



if __name__ == '__main__':
    get_data()
