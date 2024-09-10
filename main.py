import pymongo

from Utils.constants import mongo_url, database_name, collection_name
import pymongo

from Utils.constants import mongo_url, database_name, collection_name

base_url = 'https://www.otodom.pl/'
from Utils.bs4_selenium import FirefoxBrowser

client = pymongo.MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]

url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?limit=72&ownerTypeSingleSelect=ALL&by=LATEST&direction=ASC&viewType=listing"
browser = FirefoxBrowser()
soup = browser.get_soup(url)
i=1
while True:
    print(f"Page={i}")
    items = soup.find_all("article", {"class": "css-136g1q2 eeungyz0"})
    for item in items:
        link = base_url + item.find("a", class_="css-16vl3c1 e17g0c820")["href"]
        record = {'url': link,
                  'title': None,
                  'price': None,
                  'price per m2': None,
                  'rooms': None,
                  'location': None,
                  'date':None,
                  }
        collection.insert_one(record)
    i+=1
    if i ==261:
        break
    new_url = url + f'&page={i}'

    browser.get_soup(new_url)
client.close()