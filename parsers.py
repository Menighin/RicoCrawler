from bs4 import BeautifulSoup as Soup
from decimal import Decimal

# This file contains the logic for parsing each page HTML into JSON data
def brl_to_decimal(value: str) -> Decimal:
    return Decimal(value.replace('.', '').replace(',', '.')[3:])

def parse_home_by_type(html: str) -> dict:
    dom = Soup(html, 'html.parser').find('tbody')
    json = {}
    for tr in dom.find_all('tr')[1:]:
        name, percentage, applied, actual = [ td.text for td in tr.find_all('td') ]

        if applied == '--':
            continue

        json[name] = { 'applied': brl_to_decimal(applied), 'actual': brl_to_decimal(actual) }
    
    print(json)
    return json