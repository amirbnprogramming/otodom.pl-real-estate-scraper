import random
import time

import pymongo
import requests

from Utils.constants import search_api_based, mongo_url
from Final.consts import user_agents

client = pymongo.MongoClient(mongo_url)
db = client['api_results']
collection = db['Otodom_collection']

temp_dic = {}
cookie = {
    "__eoi": "ID=ad51e1083e4aff31:T=1719908618:RT=1720265679:S=AA-Afjbx8pKg62Ga1A7lqquY3uAT",
    "__gads": "ID=e89b17b50cc98cff:T=1719908618:RT=1720265679:S=ALNI_Mbpf1NrqS3xq1-TjaTIkJ5Wh1rfRQ",
    "__gfp_64b": "HtFqwPVh0GHhBsnUXywsDBmpu.5AVuwSrT1GxXlKNHn.G7|1719908542|2",
    "__gpi": "UID=00000e622bc68bb6:T=1719908618:RT=1720265679:S=ALNI_MasWo3adAxXgWreYNOIYi6JkM-Bfw",
    "__rtbh.lid": "{\"eventType\":\"lid\",\"id\":\"20SylyhYI7ydtLLDcNpl\"}",
    "__rtbh.uid": "{\"eventType\":\"uid\",\"id\":\"null\"}",
    "_clck": "11tyi4l|2|fn8|0|1644",
    "_clsk": "1yoaacv|1720265679535|6|0|v.clarity.ms/collect",
    "_fbp": "fb.1.1719908541499.507248627900840664",
    "_ga": "GA1.1.444306882.1719908539",
    "_ga_20T1C2M3CQ": "GS1.1.1720264365.7.1.1720265680.49.0.0",
    "_ga_6PZTQNYS5C": "GS1.1.1720264365.7.1.1720265674.55.0.0",
    "_gat_clientNinja": "1",
    "_gcl_au": "1.1.217174759.1719908539",
    "_gid": "GA1.2.1474298781.1720264369",
    "_hjSession_2028838": "eyJpZCI6ImYwZTBlODdlLTdlNGEtNDg0NS1iNmE3LTU3ZmU0MzhkNDA2MCIsImMiOjE3MjAyNjQzNjkyNDksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
    "_hjSessionUser_2028838": "eyJpZCI6IjU5MDA2NGI3LTU0OWMtNWI1ZS05MzdjLTQxY2NkNTJkZjVlZiIsImNyZWF0ZWQiOjE3MjAwNDI0NTgzNDYsImV4aXN0aW5nIjp0cnVlfQ==",
    "_tt_enable_cookie": "1",
    "_ttp": "KkjQ08w7wWH_joI_jEKLLe6c2hk",
    "_uetsid": "ad0edfe03b8811ef804dd94e98a88cb3",
    "_uetvid": "33b551c0384c11efbe50a12dd9df805b",
    "dfp_user_id": "9bd15327-1771-4734-aa6d-2604146b2452",
    "eupubconsent-v2": "CQBHrHQQBHrHQAcABBENA7E8AP_gAAAAAAYgJ9NV_G_fbXlj8Xp0aftkeY1f99h7rsQxBhfJk-4FyLuW_JwX32EzNA16pqYKmRIEu3bBIQFlHIDUDUCgaogVrTDMakWMgTNKJ6BEiFMRe2dYCF5vmQFD-QKY5tpvd3d52Re9_dv83dzyz4Vnn3Kp_-e1WJCdA5cgAAAAAAAAAAAAAAAQAAAAAAAAAQAIAAAAAAAAAAAAAAAAAAAAA_cBf78AAABgSCAAAgABcAFAAVAA4AB4AEEALwA1AB4AEQAJgAVQA3gB6AD8AISAQwBEgCOAEsAJoAYAAw4BlAGWANkAc8A7gDvgHsAfEA-wD9gH-AgABFICLgIwARqAkQCSwE_AUGAqACrgFzAL0AYoA0QBtADcAHEgR6BIgCdgFDgKPAUiAtgBcgC7wF5gMGAYbAyMDJAGTgMzAZzA1cDWQG3gNzAbqA4IByYDlwJuBAC4ADgASABHAIOARwAmgBfQErAJtAUgArkBYQCxAFuALyAYgAxYBkIDRgGpgNoAbcA3QcArAARAA4ADwALgAkAB-AEcAKAAaABHADkAIBAQcBCACIgEcAJoAVAA6QCVgExAJlATaApOBXIFdgLEAWoAtwBdADBAGIAMWAZCAyYBowDUwGvANoAbYA26BuYG6AOPActA50DnwJtjoJoAC4AKAAqABwAEEALgA1AB4AEQAJgAVYAuAC6AGIAN4AegA_QCGAIkASwAmgBRgDAAGGAMoAaIA2QBzwDuAO8Ae0A-wD9AH_ARQBGICOgJLAT8BQYCogKuAWIAucBeQF6AMUAbQA3ABxADqAH2ARfAj0CRAEyAJ2AUPAo8CkAFNAKsAWLAtgC2QFugLgAXIAu0Bd4C8wF9AMGAYaAx6BkYGSAMnAZUAywBmYDOQGmwNXA1gBt4DdQHFgOTAcuBNwCbwE4SABYABAADwA0ADkAI4AWIAvoCbQFJgK5AWIAvIBggDPAGjANTAbYA24BugDlgHPgTbIQIQAFgAUABcADUAJgAVQAuABiADeAHoARwAwABzwDuAO8Af4BFACUgFBgKiAq4BcwDFAG0AOoAj0BTQCrAFigLRAXAAuQBkYDJwGckoEgACAAFgAUAA4ADwAIgATAAqgBcADFAIYAiQBHACjAGAANkAd4A_ICogKuAXMAxQB1AETAIvgR6BIgCjwFNALFAWwAvOBkYGSAMnAZyA1gBt4E3AJwkgCQAFwAjgDuAIAAQcAjgBUAErAJiATaApMBbgDFgGWAM8AboA5YCbZQBGAAoAC4AJAAXABHAC2AI4AcgA7gB9gEAAIOAWIAuoBrwDtgH_ATEAm0BUgCuwFuALoAXkAwQBiwDJgGeANGAamA16BuYG6AOWAm2BOEpA7AAXABQAFQAOAAggBkAGoAPAAiABMACqAGIAP0AhgCJAFGAMAAZQA0QBsgDnAHfAPwA_QCLAEYgI6AkoBQYCogKuAXMAvIBigDaAG4AOoAe0A-wCJgEXwI9AkQBOwChwFIAKaAVYAsUBbAC4AFyALtAXmAvoBhsDIwMkAZOAywBnMDWANZAbeA3UBwQDkwJvFoBQANQBHADAAHcAXoA-wCmgFWAMzAm4WAFADLAI4Aj0BMQCbQFcgNGAamA3QBywAAA.f_wAAAAAAAAA",
    "lang": "pl",
    "laquesis": "eure-19720@b#eure-21385@a#eure-25610@b#eure-26607@a#eure-27170@c#eure-27417@b#eure-27544@b#smr-3426@b",
    "laquesisff": "euads-4389#gre-12226#rer-165#rer-166#rst-73#rst-74",
    "laquesissu": "",
    "ldTd": "true",
    "lqstatus": "1720265686|19087bf124ax54a72c79|eure-19720#eure-27170#eure-26607#eure-27417||",
    "onap": "19072892915x526f6da4-6-19087bf124ax54a72c79-131-1720267482",
    "OptanonAlertBoxClosed": "2024-07-02T08:22:18.694Z",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Sat+Jul+06+2024+15:04:31+GMT+0330+(Iran+Standard+Time)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f9b2cd72-57a0-482b-8b65-9e9661e23be8&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0002:1,C0003:1,C0004:1,gad:1&geolocation=;&AwaitingReconsent=false",
    "st_userID": "GA1.1.444306882.1719908539__unlogged"
}
i=2
url = search_api_based
while i<=260:
    user_agent = random.choice(user_agents)
    headers = {"Content-Type": "application/json",
               "User-Agent": user_agent,
               }
    response = requests.get(url,headers=headers)
    print(response.status_code)
    results = response.json()['pageProps']['data']['searchAds']['items']

    for result in results:
        id = result['id']
        slug = result['slug']
        title = result['title']
        link = 'https://www.otodom.pl/pl/oferta' + slug
        print(id, slug, title, link)

        total_price = None
        rent_price = None
        price_per_meter = None
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

        temp_dic = {'_id': id,
                    'slug': slug,
                    'title': title,
                    'link': link,
                    'total_price': total_price,
                    'rent_price': rent_price,
                    'price_per_meter': price_per_meter,
                    'meter_area': meter_area,
                    'rooms': rooms,
                    'created_at': created_at,
                    }
        try:
            pass
            # collection.insert_one(temp_dic)
        except Exception as e:
            pass

        print(total_price, rent_price, price_per_meter, meter_area, rooms, created_at)
        print("*******************")

    time.sleep(random.randint(3,10))
    url = search_api_based + f'&page={i}'
    print(f'Page:({i})')
    i += 1
# time.sleep(random.randint(10,25))
