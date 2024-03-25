from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from tools.captchas import get_recaptcha_solve, solve_recaptcha
from tools.shortcuts import fill_input, wait
from tools.user import Profile
from tools.config import COUNTRY_NUMBER_CODE, EBAY_COUNTRY_CODE
from tools.shortcuts import click_element
from fivesim import FiveSim
import re
import time
import random

# These example values won't work. You must get your own api_key
API_KEY = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI3MzA2NDEsImlhdCI6MTcxMTE5NDY0MSwicmF5IjoiOWFkN2UyY2U5YWY2NzA0MzU0NzZmNWQxMWM2OTRiNWQiLCJzdWIiOjczOTM5Mn0.V2VXZqKJDGnM9hSq4NXH8oxadAbAt0286n30066pBHSCdCUHt8w3onq6UBrazL05hslmhv3vZPy4pZHRM46QwiBCsUKsA7m8DK2_LaMCvVReRE4kNkkglyEUGKpDsy3yKThHLiT5rc3j4-x86tTC8-szhaG-Hrr1EnlNhZ37uXzyhPFUIawpHOFX3gZC3AcntMS_n-wed3vH9UwIKxDcouH9xpIJLZ7q6vNeYQo2nwJFUpsDpwDrWWyzsEB3XSaHxkCCO6K_mDwFn0UFQwM4hjLKVY5h5nQajh_h9tLx15xhinW6C9Rmz1rFn5t4Y8oScsVvOO8Rjv9uhbRFE3xTRg'

client = FiveSim(API_KEY) 
def human_like_typing(element, text, min_delay=0, max_delay=0.2):
        for character in text:
            delay = random.uniform(min_delay, max_delay)
            element.send_keys(character)
            time.sleep(delay)

def register_ebay(driver: WebDriver, profile: Profile):

    driver.get('https://signup.ebay.com/pa/crte')

    fill_input(driver, profile.firstName, By.XPATH, '//*[@id="firstname"]')
    fill_input(driver, profile.lastName, By.XPATH, '//*[@id="lastname"]')
    fill_input(driver, profile.get_email(), By.XPATH, '//*[@id="Email"]')
    fill_input(driver, profile.ebay_password, By.XPATH, '//*[@id="password"]')
    
    driver.find_element(By.ID, 'gdpr-banner-accept').click()
    driver.find_element(By.ID, 'EMAIL_REG_FORM_SUBMIT').click()


def get_code(html_content):
     pattern = r"\d{6}"
     match = re.search(pattern, html_content)
     if match:
         return match.group(1)  # Return the entire match as a string
     else:
         return None 
     
def wait_for_sms(phone):
    sms = None
    attempts = 0
    while not sms and attempts < 10:  
        wait(10) 
        print("[*] Checking for SMS...")
        print(phone['id'])
        result = client.check_order(order_id= phone['id'])
        print("[*] SMS Result:", result)
        if len(result['sms']) > 5:
            sms = get_code(result['sms'])  
            if sms:
                print(f"[*] SMS code: {sms}")
                break
        else: attempts += 1
    return sms  
 
def ebay_phone_verification(driver): # select country from menu not working yet 

    select_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'countryCd')))
    select_menu.click()
    russia_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Russische Föderation')]")))
    russia_option.click()
    phone = client.buy_number(country='russia', operator='mts', product='ebay') # Buy new activation number
    print("[*] phone:" , phone)
    number = str(phone['phone'])
    number_tail = number[len(COUNTRY_NUMBER_CODE):]


    fill_input(driver, number_tail, By.XPATH, '//*[@id="phoneCountry"]')
    click_element(driver, By.ID, 'SEND_AUTH_CODE')

    code = wait_for_sms(client)

    fill_input(driver, code[0], By.XPATH, '//*[@id="pinbox-0"]')
    fill_input(driver, code[1], By.XPATH, '//*[@id="pinbox-1"]')
    fill_input(driver, code[2], By.XPATH, '//*[@id="pinbox-2"]')
    fill_input(driver, code[3], By.XPATH, '//*[@id="pinbox-3"]')
    fill_input(driver, code[4], By.XPATH, '//*[@id="pinbox-4"]')
    fill_input(driver, code[5], By.XPATH, '//*[@id="pinbox-5"]')

    print('[*] solving the hcaptcha')
    wait(30)

