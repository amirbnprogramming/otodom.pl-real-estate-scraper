import csv
import os
import random
import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumwire2 import webdriver

from Utils.logger import logger
from Constants import url_html_view, csv_filename, csv_header

# region : Chrome drvier configurations
logger.info('Implement Selenium WebDriver Configuration')
chrome_options = webdriver.ChromeOptions()
caps = chrome_options.to_capabilities()
caps["acceptInsecureCerts"] = True
chrome_options.add_argument('--allow-insecure-localhost')
driver = webdriver.Chrome(options=chrome_options)
# endregion : Chrome drvier configurations

# region : Clicking on search button
driver.get(url_html_view)
try:
    wait = WebDriverWait(driver, 15)
    pop_up = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
    pop_up.click()
    time.sleep(2)

except Exception as e:
    pass

finally:
    search_button = driver.find_element(By.CSS_SELECTOR, '#search-form-submit')
    search_button.click()
    logger.info('Search Button Clicked')

    time.sleep(5)


# endregion : Clicking on search button


def csv_updater(data_dicts_list):
    logger.info(f'Update CSV file ({csv_filename})')

    existed_data = []
    with open(csv_filename, mode='r+', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        writer = csv.writer(file)
        existed_data = [row[0] for row in reader]
        for row in data_dicts_list:
            if row[0] not in existed_data:
                writer.writerow(row)


def json_parser(json_data):
    logger.info(f'Pars Json data')

    items = []
    for result in json_data:
        total_price = None
        rent_price = None
        price_per_meter = None

        id = result['id']
        slug = result['slug']
        title = result['title']
        link = 'https://www.otodom.pl/pl/oferta' + slug

        try:
            street = result['location']['address']['street']['name']
        except Exception as e:
            street = None
        try:
            city = result['location']['address']['city']['name']
        except Exception as e:
            city = None
        try:
            province = result['location']['address']['province']['name']
        except Exception as e:
            province = None

        logger.info(f'Id: ({id})')
        logger.info(f'Slug: ({slug})')
        logger.info(f'Title: ({title})')
        logger.info(f'Link: ({link})')

        logger.info(f'Street:({street})')
        logger.info(f'City:({city})')
        logger.info(f'Province:({province})')

        if result['totalPrice']:
            total_price = str(result['totalPrice']['value']) + result['totalPrice']['currency']
        if result['rentPrice']:
            rent_price = str(result['rentPrice']['value']) + result['rentPrice']['currency']
        if result['pricePerSquareMeter']:
            price_per_meter = str(result['pricePerSquareMeter']['value']) + result['pricePerSquareMeter'][
                'currency'] or None
        meter_area = result['areaInSquareMeters']
        rooms = result['roomsNumber']
        created_at = result['dateCreatedFirst']

        temp_list = [str(id), slug, title, link, total_price, rent_price, price_per_meter, meter_area, rooms,
                     created_at, street, city, province]
        items.append(temp_list)
        logger.info(f'Total Price: ({total_price})')
        logger.info(f'Rent Price: ({rent_price})')
        logger.info(f'Price per Meter: ({price_per_meter})')
        logger.info(f'Meter: ({meter_area})')
        logger.info(f'Rooms: ({rooms})')
        logger.info(f'Create Date: ({created_at})')
        logger.info("*******************")

    csv_updater(items)


# region : find base url and authorization data
logger.info(f'Finding the API and Header . . .')

api_url = None
header = None
page = 1
for req in driver.requests:
    if req.response and 'https://www.otodom.pl/_next/data' in req.url:
        scraped_headers = req.headers
        api_url = req.url.replace('limit=36', 'limit=72')
        header = scraped_headers
driver.close()
# endregion : find base url and authorization data


# region : check csv file existance
logger.info(f'Checking CSV file existance . . .')

if os.path.exists(csv_filename):
    logger.info(f"The file '{csv_filename}' exists.")
else:
    logger.info(f"The file '{csv_filename}' does not exist.")

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        csv_writer.writeheader()
# endregion : check csv file existance

# Start scraping items
if api_url is not None and header is not None:
    url = api_url
    while True:
        logger.info(f'page={page}')
        logger.info(f'Send request to ({url})')
        response = requests.get(url, headers=header)
        results = response.json()['pageProps']['data']['searchAds']['items']
        if results:
            json_parser(results)
        else:
            break
        # pagination section and updating URL
        time.sleep(random.randint(3, 10))
        page += 1
        url = api_url + f'&page={page}'
