import random
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json
from random import randint

file_lock = threading.Lock()
EXTENSION_LINK = "C:\\Users\\AzizTaieb\\Documents\\GitHub\\ebay\\example_2\\solver"

def get_browser_fingerprint(profile_dir: str, port, proxy=None):
    options = uc.ChromeOptions()
    options.add_argument(f"--load-extension={EXTENSION_LINK}")
    options.add_argument(f"--user-agent={getRandomUa()}")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(f'--user-data-dir={profile_dir}')

    executable_path=f'{ChromeDriverManager().install()}'
    driver_executable_path=f'drivers/chromedriver{port}'
    service = ChromeService(executable_path=executable_path)
    with file_lock:
        browser = uc.Chrome( options=options ,use_subprocess=False)
    browser.execute_script("Date.prototype.toLocaleString = function() { return new Date(this + 3600000*(new Date().getTimezoneOffset()/60 + 1)).toLocaleString(); }")
    return browser

def getRandomUa():
    with open('uarandom.json', 'r') as ua:
        ua = json.load(ua)
    MAX_LEN = len(ua)
    rand_index = randint(0, (MAX_LEN - 1))
    return ua[rand_index]


