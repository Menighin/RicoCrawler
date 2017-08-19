import time
import json
import parsers as parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RICO_LOGIN_URL = 'https://www.rico.com.vc/login?url=/dashboard/'
MAX_WAIT_TIME = 60

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
    home_by_type = driver.find_element_by_css_selector('#home-step-menu-resumo-investimentos table')
    home_treasury = driver.find_element_by_css_selector("div[summary-position-product=treasury]")

    json['home_by_type'] = parser.parse_home_by_type(home_by_type.get_attribute('innerHTML'))


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
