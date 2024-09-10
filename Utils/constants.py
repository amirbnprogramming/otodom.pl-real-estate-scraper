base_url = "https://wahi.com/"
url = ""
profile_path = 'C:/Users/amirb/AppData/Roaming/Mozilla/Firefox/Profiles/28c7uhg3.default-release'

mongo_url = 'mongodb://localhost:27017/'
database_name = 'otodom'
collection_name = 'links'

payload = {"query":"query PopularSearch($input: PopularSearchInput!) {\n  popularSearch(input: $input) {\n    ... on PopularSearch {\n      data\n      __typename\n    }\n    ... on ErrorBadRequest {\n      code\n      message\n      __typename\n    }\n    ... on ErrorInternal {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}","operationName":"PopularSearch","variables":{"input":{"transactionType":"sell","estateType":"flat","location":"mazowieckie/warszawa/warszawa/warszawa","page":1}}}

# search_api_based = 'https://www.otodom.pl/_next/data/aly8yeIHgGP3teRZ9v1IH/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa.json?limit=36&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&searchingCriteria=mazowieckie&searchingCriteria=warszawa&searchingCriteria=warszawa&searchingCriteria=warszawa'
search_api_based = 'https://www.otodom.pl/_next/data/uoyObqrI-E788tD-piIci/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa.json?limit=72&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&searchingCriteria=mazowieckie&searchingCriteria=warszawa&searchingCriteria=warszawa&searchingCriteria=warszawa'
