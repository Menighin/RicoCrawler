import time
import json
import parsers as parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RICO_LOGIN_URL = 'https://www.rico.com.vc/login?url=/dashboard/'
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
    webdriverPath = props['chromeWebdriver'] if 'chromeWebdriver' in props else None

    driver = webdriver.Chrome(webdriverPath) if webdriverPath is not None else webdriver.Chrome()
    driver.get(RICO_LOGIN_URL)
    driver.implicitly_wait(MAX_WAIT_TIME) # Wait for element to appear in each call

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
    json = {}
    summary = tryGetElement(driver, '#home-step-menu-resumo-investimentos table')
    driver.implicitly_wait(0)
    home_treasury = tryGetElement(driver, "div[summary-position-product='treasury'] #tableAllocatedValue")
    fixed_income = tryGetElement(driver, "div[summary-position-product='fixed-income'] #tableAllocatedValue")
    funds = tryGetElement(driver, "div[summary-position-product='funds'] #tableAllocatedValue")

    driver.implicitly_wait(MAX_WAIT_TIME) # Wait for element to appear in each call

    json['home'] = {}
    json['home']['summary'] = parser.parse_home_table(summary.get_attribute('innerHTML'), parser.HomeTableType.ZERO_TWO_THREE)
    json['home']['homeTreasury'] = parser.parse_home_table(home_treasury.get_attribute('innerHTML'), parser.HomeTableType.ZERO_ONE_TWO)
    json['home']['fixedIncome'] = parser.parse_home_table(fixed_income.get_attribute('innerHTML'), parser.HomeTableType.ZERO_THREE)
    json['home']['funds'] = parser.parse_home_table(funds.get_attribute('innerHTML'), parser.HomeTableType.ZERO_ONE_TWO)
    
    driver.quit()



def read_properties() -> dict:
    with open('config.json') as json_file:
        return json.load(json_file)

if __name__ == '__main__':
    try:    
        props = read_properties()
        result = get_actives_data(props)
    except FileNotFoundError:
        print('Você deve criar o arquivo "config.json" na mesma pasta que está o seu "main.py"')
