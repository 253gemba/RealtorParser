import time
from selenium import webdriver
from selenium.webdriver.common.by import By

print()
print('НАЧАЛО')
print()

def record_data(data):
    list_data = []
    list_data.append(data)
    print(data)
    return list_data


def get_links():
    links = []
    url = 'https://youla.ru/moskva/nedvijimost/prodaja-kvartiri?attributes[realty_building_type][0]=166228&attributes[term_of_placement][from]=-1%20day&attributes[term_of_placement][to]=now'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    i = 0
    for scroll in range(1, 22, 4):
        driver.execute_script(f"window.scrollTo(5, {scroll}000);")
        time.sleep(1)
        containers = driver.find_elements(By.CLASS_NAME, 'sc-gqplIC')
        time.sleep(3)

        for container in containers:
            i += 1
            link = container.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if link not in links:
                links.append(link)

    driver.quit()

    return links


def get_data():
    new_links = get_links()
    print(len(new_links))
    for card_link in new_links:
        driver = webdriver.Chrome()
        driver.get(card_link)
        time.sleep(1)
        name = driver.find_element(By.CLASS_NAME, 'sc-mlOqW').find_element(By.TAG_NAME, 'a').text.split('(')[0]

        adress = driver.find_element(By.CLASS_NAME, 'sc-eWuggI').find_element(By.TAG_NAME, 'span').text

        floors = driver.find_elements(By.CLASS_NAME, 'dyaAgt')[1].find_elements(By.CLASS_NAME, 'sc-cOajty')
        floor, max_floor = None, None

        for i in range(len(floors)):
            if 'Этаж' in floors[i].text:
                floor = int(floors[i + 1].text)
                break

        for i in range(len(floors)):
            if 'Этажность дома' in floors[i].text:
                max_floor = int(floors[i + 1].text.split('\n')[0])
                break

        price = driver.find_element(By.CLASS_NAME, 'sc-dbGQSH').find_element(By.TAG_NAME, 'span').text\
            .replace('\u205f', '')

        link_img = driver.find_element(By.CLASS_NAME, 'sc-cKFVac').find_element(By.TAG_NAME, 'img').get_attribute('src')

        area = driver.find_element(By.CLASS_NAME, 'sc-CARIn').find_element(By.TAG_NAME, 'h2').text.split(',')[-1]
        area = area.replace(' м²', '').replace(' ', '')
        if '.' in area:
            area = float(area)
        else:
            area = int(area)

        driver.quit()

        record_data([name, 0, price, adress, area, floor, max_floor, card_link, link_img])
    return len(new_links)


if __name__ == '__main__':
    get_data()
