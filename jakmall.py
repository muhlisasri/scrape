from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = Options()
options.add_argument('-headless')
web    = 'https://www.jakmall.com/gudanggrosir'
driver = webdriver.Firefox(options=options)
product_links = set()
product_name  = []
product_price = []
description   = []
img1 = []
img2 = []
img3 = []

for i in range(1,2) :
    page  = web + f'?page={i}'
    driver.get(page)
    links = driver.find_elements (by='xpath', value='//a[@class="pi__name link link--normal"]')
    
    for link in links :
        url = link.get_attribute('href')
        print(url)
        product_links.add(url)

for link in product_links :
    url = link
    result = driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dp__thumb')]"))
        )
        name = driver.find_element(by='xpath', value="//h1[contains(@class,'dp__name')]").text
        product_name.append(name)
        print(name)
        product_price.append(driver.find_element(by='xpath', value="//div[contains(@class,'format__money')]").text)
        description.append(driver.find_element(by='xpath', value="//div[contains(@class, 'dp__info__wrapper')]").text)
        img_div = driver.find_element(by='xpath', value="//div[contains(@class,'dp__thumb')]")
        imgs_tag = img_div.find_elements(By. TAG_NAME, 'img')
        img_links = []
        for img in imgs_tag :
            src = img.get_attribute('src')
            img_links.append(src)
        img1.append(img_links[0])
        img2.append(img_links[1])
        img3.append(img_links[2])
    except Exception as e:
        print("An error occurred:", str(e))
driver.quit()

data = {'Nama Produk':product_name, 'Harga': product_price, 'img1' :img1, 'img2': img2,'img3': img3, 'Deskripsi' : description}
print(data)
df = pd.DataFrame(data)
df.to_csv('jakmall.csv', index=False)
