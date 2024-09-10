import random
import time

import pymongo
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from Utils.bs4_selenium import FirefoxBrowser, ChromeBrowser
from Utils.constants import mongo_url, database_name, collection_name
from Utils.logger import logger
from translator import translator, convert_date

client = pymongo.MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]

browser = ChromeBrowser()


def get_date (soup):
    try:
        date = soup.select_one('.css-1soi3e7').text
        if date is None :
            date = soup.select_one('.css-1cl8nj2').text
            if date is None :
                date=soup.select_one('#__next > main > div.css-1xqxcx5.e1ovh0pn0 > div.css-1w41ge1.e1ovh0pn1 > div.css-1xllj56.e16plgr60 > div.css-wvps4y.e1303neu0 > div > p > font > font').text
    except Exception as e:
        date = None
    return date

def get_price(soup_page):
    try:
        price = soup_page.select_one('#__next > main > div.css-5c9a3k.e172idfj0 > div.css-y6l269.e172idfj3 > header > strong').text
        if price is None :
            price = soup_page.select_one('//*[@id="__next"]/main/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/strong/font/font').text
    except Exception as e:
        price = None
    return price

records = collection.find()
# '//*[@id="__next"]/main/div[1]/div[1]/div[3]/div[3]/div/p[1]/font/font'
for record in records:
    url_page = record.get('url')
    logger.info(url_page)
    soup_page = browser.get_url(url=url_page)
    time.sleep(random.randint(10, 25))
    try:
        date_tag = browser.driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[1]/div[1]/div[3]/div[3]/div/p[1]')
        date = date_tag.text
    except Exception as e:
        date = None
    logger.info(date)
#
#     price = get_price(soup_page)
#     date = get_date(soup_page)
#
#     logger.info(price)
#     logger.info(date)
#
#     if date is not None:
#         date = date.split(": ")[1].strip()
#         translated_date = translator(date)
#         converted_date = convert_date(translated_date)
#         collection.update_one({"_id": record["_id"]}, {"$set": {"date": converted_date, "price": price}})
#         logger.info(converted_date)
#
#     # process_record(record)
#
# client.close()
