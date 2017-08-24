from bs4 import BeautifulSoup as Soup
from decimal import Decimal
from enum import Enum

# This file contains the logic for parsing each page HTML into JSON data

class HomeTableType(Enum):
    ZERO_TWO_THREE = 1
    ZERO_ONE_TWO = 2
    ZERO_THREE = 3

def brl_to_decimal(value: str) -> Decimal:
    return value.replace('.', '').replace(',', '.')[3:]
    # return Decimal(value.replace('.', '').replace(',', '.')[3:])

def parse_home_table(html: str, tableType: HomeTableType) -> dict:
    dom = Soup(html, 'html.parser').find('tbody')
    json = []
    for tr in dom.find_all('tr')[1:]:
        tds = tr.find_all('td')
        applied = '-'
        if tableType == HomeTableType.ZERO_TWO_THREE:
            name, *_, applied, actual = [ td.text.strip() for td in tds ]
        elif tableType == HomeTableType.ZERO_ONE_TWO:
            name, applied, actual, *_ = [ td.text.strip() for td in tds ]
        elif tableType == HomeTableType.ZERO_THREE:
            name, _, _, actual, *_ = [ td.text.strip() for td in tds ]

        if applied == '--':
            continue
        
        if tableType != HomeTableType.ZERO_THREE:
            json.append({ 'name': name, 'applied': brl_to_decimal(applied), 'actual': brl_to_decimal(actual) })
        else:
            json.append({ 'name': name, 'actual': brl_to_decimal(actual) })
    
    return json

def parse_treasury_item(html: str):

    dom = Soup(html, 'html.parser')
    json = {}

    i = 0
    for tr in dom.find_all('tr')[:-1]:

        if i == 1: # It is the headers for the products
            i += 1
            continue

        tds = tr.find_all('td')

        if i == 0: # It is the consolidated
            name, _, _, applied, actual, *_ = [ td.text.strip() for td in tds ]

            json = { 'name': name, 'applied': brl_to_decimal(applied), 'actual': brl_to_decimal(actual), 'products': [] }

        else:
            _, name, _, _, applied, actual, *_ = [ td.text.strip() for td in tds ]

            json['products'].append({ 'name': name, 'applied': brl_to_decimal(applied), 'actual': brl_to_decimal(actual)})

        i += 1

    return json

def parse_fixed_income(html: str):

    dom = Soup(html, 'html.parser')
    json = []

    for tr in dom.find_all('tr')[1:]:

        tds = tr.find_all('td')

        name, _, _, _, applied, actual, *_ = [ td.text.strip() for td in tds ]

        json.append({ 'name': name, 'applied': brl_to_decimal(applied), 'actual': brl_to_decimal(actual) })

    return json