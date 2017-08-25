import time
import json
import datetime
import parsers as parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RICO_LOGIN_URL = 'https://www.rico.com.vc/login?url=/dashboard/'
RICO_TREASURY_PAGE = 'https://www.rico.com.vc/dashboard/tesouro-direto/'
RICO_FIXED_INCOME_PAGE = 'https://www.rico.com.vc/dashboard/renda-fixa/'
TRACKED_PROPERTIES = ['actual', 'applied']
MAX_WAIT_TIME = 60

def tryGetElement(driver, selector: str) -> object:
    try:
        return driver.find_element_by_css_selector(selector)
    except NoSuchElementException as e:
        print (e.message)

def get_actives_data(props: dict):

    if 'username' not in props or 'password' not in props:
        print('O arquivo de propriedades não contém as chaves "username" ou "password"')
        return False

    username = props['username']
    password = props['password']
    webdriver_path = props['chromeWebdriver'] if 'chromeWebdriver' in props else None

    options = webdriver.ChromeOptions() 
    options.add_argument("user-data-dir=C:\\Users\\Menighin\\AppData\\Local\\Google\\Chrome\\User Data") #Path to your chrome profile

    driver = webdriver.Chrome(webdriver_path, chrome_options = options) if webdriver_path is not None else webdriver.Chrome(chrome_options = options)

    driver.implicitly_wait(MAX_WAIT_TIME) # Wait for element to appear in each call
    driver.get(RICO_LOGIN_URL)

    form_user =  driver.find_element_by_name('loginController.usernameForm')
    input_username = form_user.find_element_by_xpath(".//input[@placeholder='Usuário']")
    input_username.send_keys(username)
    time.sleep(0.2)
    form_user.submit()
    form_password = driver.find_element_by_name('loginController.passwordForm')
    buttons = form_password.find_elements_by_tag_name('button')

    for c in password:
        for button in buttons:
            if c in button.text:
                button.click()

    form_password.submit()

    # Crawling the home page
    jsonDict = {}
    summary = tryGetElement(driver, '#home-step-menu-resumo-investimentos table')
    driver.implicitly_wait(1)
    home_treasury = tryGetElement(driver, "div[summary-position-product='treasury'] #tableAllocatedValue")
    fixed_income = tryGetElement(driver, "div[summary-position-product='fixed-income'] #tableAllocatedValue")
    funds = tryGetElement(driver, "div[summary-position-product='funds'] #tableAllocatedValue")

    driver.implicitly_wait(MAX_WAIT_TIME) # Wait for element to appear in each call

    jsonDict['home'] = {}
    jsonDict['home']['summary'] = parser.parse_home_table(summary.get_attribute('innerHTML'), parser.HomeTableType.ZERO_TWO_THREE)
    jsonDict['home']['homeTreasury'] = parser.parse_home_table(home_treasury.get_attribute('innerHTML'), parser.HomeTableType.ZERO_ONE_TWO)
    jsonDict['home']['fixedIncome'] = parser.parse_home_table(fixed_income.get_attribute('innerHTML'), parser.HomeTableType.ZERO_THREE)
    jsonDict['home']['funds'] = parser.parse_home_table(funds.get_attribute('innerHTML'), parser.HomeTableType.ZERO_ONE_TWO)
    
    # Crawling the Treasury page
    jsonDict['homeTreasury'] = []
    driver.get(RICO_TREASURY_PAGE)

    tbodies = driver.find_elements_by_css_selector('#tableAllocatedValue tbody')
    i = 0
    for tbody in tbodies: # Ignores first tbody
        if i == 0:
            i += 1
            continue
        jsonDict['homeTreasury'].append(parser.parse_treasury_item(tbody.get_attribute('innerHTML')))


    # Crawling Fixed Income
    driver.get(RICO_FIXED_INCOME_PAGE)

    jsonDict['fixedIncome'] = parser.parse_fixed_income(driver.find_element_by_css_selector('#tableAllocatedValue tbody').get_attribute('innerHTML'))

    driver.quit()

    return jsonDict

def recursive_update_obj(f_json, res, now_str): 
    if isinstance(res, list):
        for item in res:
            found = False
            for obj in f_json:
                if item['name'] == obj['name']:
                    found = True
                    for tracked in TRACKED_PROPERTIES:
                        if tracked in obj and tracked in item:
                            obj[tracked].append(item[tracked])
                        elif tracked in item and tracked not in obj:
                            obj[tracked] = [item[tracked]]
                    # Date
                    if 'date' in obj:
                        obj['date'].append(now_str)
                    elif 'date' not in obj:
                        obj['date'] = [now_str]

                    break
            if found is False:
                j_item = {}
                j_item['name'] = item['name']

                for tracked in TRACKED_PROPERTIES:
                    if tracked in item:
                        j_item[tracked] = [item[tracked]]
                j_item['date'] = [now_str]
                f_json.append(j_item)

    elif isinstance(res, dict):
        for k, v in res.items():
            if isinstance(v, dict) or isinstance(v, list):
                if k not in f_json:
                    f_json[k] = {} if isinstance(v, dict) else []
                recursive_update_obj(f_json[k], v, now_str)

def write_file(f_json, res, file, now_str):

    # Fill up the date information on the result json
    f_json['lastRun'] = now_str

    recursive_update_obj(f_json, res, now_str)

    file.write('var DATA=' + json.dumps(f_json))
    # recursive_append_date(res, now_str)


def read_properties() -> dict:
    with open('config.json') as json_file:
        return json.load(json_file)


if __name__ == '__main__':

    NOW = datetime.datetime.now()
    NOW_STR = '{}-{:02}-{:02}'.format(NOW.year, NOW.month, NOW.day)

    with open('html/data.js', 'r') as f:
        fStr = f.read().replace('var DATA=', '')
        fJson = json.loads(fStr) if len(fStr) > 0 else {'lastRun': ''}

    if NOW_STR == fJson['lastRun']:
        print('Bot já gravou dados hoje. Volte amanhã.')
    else: 
        with open('html/data.js', 'w+') as f:
            try:    
                props = read_properties()
                result = get_actives_data(props)
                write_file(fJson, result, f, NOW_STR)
            except FileNotFoundError:
                print('Você deve criar o arquivo "config.json" na mesma pasta que está o seu "main.py"')
