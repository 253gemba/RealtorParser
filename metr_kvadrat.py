import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def record_data(data):
    list_data = []
    list_data.append(data)
    print(data)
    return list_data


def get_links_one_page():
    url_msk = 'https://m2.ru/moskva/nedvizhimost/kupit-kvartiru/?sort=date'
    driver = webdriver.Chrome()
    driver.get(url_msk)
    time.sleep(3)
    links = []
    containers = driver.find_elements(By.CLASS_NAME, 'LayoutSnippet__title')
    for container in containers:
        link = container.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links.append(link)
    driver.quit()
    return links


def get_data():
    list_links = get_links_one_page()
    for card_link in list_links:
        driver = webdriver.Chrome()
        driver.get(card_link)
        time.sleep(3)

        adress = driver.find_element(By.CLASS_NAME, 'ClClickableAddress__links').text.replace('\n', ' ')

        link_page = driver.find_element(By.CLASS_NAME, 'CarouselGallery__img-container').find_element(By.TAG_NAME, 'img')\
            .get_attribute('src')

        price = driver.find_element(By.CLASS_NAME, 'Price').find_element(By.TAG_NAME, 'span').text.replace(' ', '')
        price = int(price)

        description = driver.find_element(By.CLASS_NAME, 'fonts-module__h1___2QWY_').text

        area = ''
        if 'студии' in description:
            area = description.split('студии ')[-1].split('м²')[0]
        elif 'квартиры' in description:
            area = description.split('квартиры ')[-1].split('м²')[0]
        if ',' in area:
            area = float(area.replace(',', '.'))
        else:
            area = int(area)

        floor = int(description.split('м²,')[-1].split('/')[0])

        max_floor = int(description.split('м²,')[-1].split('/')[1].replace('этаж', ''))

        try:
            name = driver.find_element(By.CLASS_NAME, 'CardAuthorBadge__name').find_element(By.TAG_NAME, 'div').text
        except:
            name = 'имени на сайте нет'
        driver.find_element(By.CLASS_NAME, 'OfferCard__actions').find_element(By.TAG_NAME, 'button').click()
        ph = driver.find_element(By.CLASS_NAME, 'modal-module__root___2NNKU')\
            .find_elements(By.CLASS_NAME, 'OfferPhoneModal2__phone')
        if len(ph) > 0:
            phone = driver.find_element(By.CLASS_NAME, 'modal-module__root___2NNKU')\
                .find_element(By.CLASS_NAME, 'OfferPhoneModal2__phone').find_element(By.TAG_NAME, 'a')\
                .get_attribute('href').replace('tel:', '')
        else:
            phon = driver.find_element(By.CLASS_NAME, 'modal-module__root___2NNKU')
            time.sleep(2)
            phone = phon.find_element(By.CLASS_NAME, 'OfferPhoneModalDesktop__list').find_element(By.TAG_NAME, 'a')\
                .text.replace(' ', '')

        time.sleep(3)
        record_data([name, phone, price, adress, area, floor, max_floor, card_link, link_page])

        driver.quit()


if __name__ == '__main__':
    get_data()
