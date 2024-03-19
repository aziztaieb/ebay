import requests
import random
from useragent import getRandomUa
from parsel import Selector
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

all_types = [
    'all',
    'http-https',
    'http',
    'https',
    'socks',
    'socks4',
    'socks5',
]

def getByCountry(country, proxy_type='all'):
    MAX_PER_PAGE = 20
    proxy_type = proxy_type.lower()
    if proxy_type not in all_types:
        return None
    headers = {
        'User-Agent': getRandomUa()
    }
    js_proxies = []
    with requests.Session() as session:
        # Get token
        session.headers['User-Agent'] = getRandomUa()
        token_data = session.get('https://www.proxydocker.com', headers=headers)
        token_select = Selector(text=token_data.text)
        token = token_select.xpath("//meta[@name='_token']/@content").extract_first()
        URL = 'https://www.proxydocker.com/es/api/proxylist/'
        data = {
            'token': token,
            'country': country,
            'city': 'all',
            'state': 'all',
            'port': 'all',
            'type': proxy_type,
            'anonymity': 'all',
            'need': 'BOT',
            'page': '1'
        }
        r = session.post(URL, headers=headers, data=data)
        if r.ok:
            proxies = r.json()
            js_proxies.extend(proxies.get('proxies', []))
            number_proxies = proxies.get('rows_count', 0)
            number_pages = number_proxies//MAX_PER_PAGE
            if float(number_pages) != number_proxies/MAX_PER_PAGE:
                number_pages += 1
            for page in range(2, number_pages + 1):
                data['page'] = str(page)
                r = session.post(URL, headers=headers, data=data)
                if r.ok:
                    proxies = r.json()
                    js_proxies.extend(proxies.get('proxies', []))
            return ['socks5://{}:{}'.format(x['ip'], x['port']) for x in js_proxies]
        else:
            print('Problem!')


def get_proxies():
    proxies = getByCountry("germany", proxy_type='socks5')
    return proxies[random.randint(0, len(proxies) - 1)]



def proxy_check(proxy):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f'--proxy-server=socks5://{proxy}')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.set_page_load_timeout(10)
        driver.get("http://httpbin.org/ip")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))
        return True
    except (TimeoutException, WebDriverException) as e:
        print(f"Proxy {proxy} failed. Error: {e}")
    finally:
        driver.quit()

    return False
