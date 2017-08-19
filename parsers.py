from bs4 import BeautifulSoup as Soup
from decimal import Decimal
from enum import Enum

# This file contains the logic for parsing each page HTML into JSON data

class HomeTableType(Enum):
    ZERO_TWO_THREE = 1
    ZERO_ONE_TWO = 2
    ZERO_THREE = 3


def brl_to_decimal(value: str) -> Decimal:
    return Decimal(value.replace('.', '').replace(',', '.')[3:])

def parse_home_table(html: str, tableType: HomeTableType) -> dict:
    dom = Soup(html, 'html.parser').find('tbody')
    json = {}
    for tr in dom.find_all('tr')[1:]:
        tds = tr.find_all('td')
        applied = '-'
        if tableType == HomeTableType.ZERO_TWO_THREE:
            name, *_, applied, actual = [ td.text.strip() for td in tr.find_all('td') ]
        elif tableType == HomeTableType.ZERO_ONE_TWO:
            name, applied, actual, *_ = [ td.text.strip() for td in tr.find_all('td') ]
        elif tableType == HomeTableType.ZERO_THREE:
            name, _, _, actual, *_ = [ td.text.strip() for td in tr.find_all('td') ]

        if applied == '--':
            continue
        
        if tableType != HomeTableType.ZERO_THREE:
            json[name] = { 'applied': brl_to_decimal(applied), 'actual': brl_to_decimal(actual) }
        else:
            json[name] = { 'actual': brl_to_decimal(actual) }
    
    print(json)
    return json