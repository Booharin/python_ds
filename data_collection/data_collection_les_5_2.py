from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time


# 2
class GoodsParser:
    # driver
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # mongo
    mongo_client = MongoClient("mongodb://admin:12345@18.197.155.243/my_db")
    my_db = mongo_client.my_db
    goods = my_db.goods
    print(goods)

    def get_goods_from_mvideo(self):
        self.driver.get('https://www.mvideo.ru/promo/vneplanovaya-chernaya-pyatnica-mark165903130?reff=menu_main')
        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'content-quote'))
        )
        self.driver.execute_script("window.scrollTo(0, 900);")
        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'gallery-list-item'))
        )
        goods = self.driver.find_elements_by_class_name('gallery-list-item')
        print(len(goods))

        self.save_to_mongo(goods)

    def save_to_mongo(self, goods_list):
        for good_item in goods_list:
            good_data = {
                'title': good_item.find_element_by_class_name('c-product-tile__description-wrapper').text,
                'price': good_item.find_element_by_class_name('c-pdp-price__current')
                    .text
                    .replace(' ', '')
                    .replace('¤', ''),
                'good_link': good_item.find_element_by_class_name('sel-product-tile-title')
                    .get_attribute('href')
            }

            self.goods.replace_one(good_data, good_data, upsert=True)


goods_parser = GoodsParser()
goods_parser.goods.delete_many({})
goods_parser.get_goods_from_mvideo()

count = 0
for good in goods_parser.goods.find({}):
    print(good)
    count += 1

print(count)
