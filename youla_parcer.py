import time
from selenium import webdriver
from selenium.webdriver.common.by import By

print()
print('НАЧАЛО')
print()

# def record_data(data):
#     list_data = [data]
#     print(list_data)
#     return list_data


def get_links():
    links = []
    url = 'https://youla.ru/moskva/nedvijimost?attributes[sort_field]=date_published'
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
    for lin in new_links:
        driver = webdriver.Chrome()
        driver.get(lin)
        time.sleep(1)
        adress = driver.find_element(By.CLASS_NAME, 'sc-eWuggI').find_element(By.TAG_NAME, 'span').text
        price = driver.find_element(By.CLASS_NAME, 'sc-dbGQSH').find_element(By.TAG_NAME, 'span').text

    return len(new_links)


get_data()

