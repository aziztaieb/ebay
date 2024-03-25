from datetime import datetime
import pathlib
from threading import Thread
from actions.register_ebay import register_ebay, ebay_phone_verification
from tools.config import NUMBER_OF_THREADS, REPEATS, START_PORT
from tools.driver import get_browser_fingerprint
from tools.store import store_result
from tools.user import Profile
from tools.proxies import get_proxies, get_proxy

path = pathlib.Path().resolve()

STOP_ON_ERROR = True


def register_account_cycle(port, repeats=20):
    for i in range(repeats):
        try:
            profile = register_account(port, i, repeats)
            print(f'\033[92m[{port}, {i+1}/{repeats}] Success! {profile.get_email()}\033[0m')
        except Exception as e:
            if STOP_ON_ERROR:
                raise e
            print(f'\033[91m[{port}, {i+1}/{repeats}] {e}\033[0m\n', end='')
    print(f'\033[94m[{port}] Completed. \033[0m\n', end='')


def register_account(port, attempt, repeats):

    proxy = get_proxy()
    print(f"--proxy-server={proxy}")
    profile = Profile()
    profile_dir = f'{path}/profiles/{profile.get_email()}'

    driver = get_browser_fingerprint(profile_dir, port, proxy)

    try:
        print(f'\033[90m[{port}, {attempt+1}/{repeats}] Process eBay registration...\033[0m')
        register_ebay(driver, profile)
        print(f'\033[90m[{port}, {attempt+1}/{repeats}] Process phone verification...\033[0m')
        ebay_phone_verification(driver)
        store_result(proxy, profile_dir, profile)
    except Exception as e:
        fine = driver.save_screenshot(f'{path}/screenshots/[{port}, {attempt+1}/{repeats}] {profile.get_email()}.png')
        input(fine)
        raise e
    # driver.get('https://bot.sannysoft.com')
    # driver.get("https://nowsecure.nl")

    driver.close()
    driver.quit()

    return profile

threads = []

for port_tail in range(NUMBER_OF_THREADS):
    port = str(START_PORT + port_tail)
    t = Thread(target=register_account_cycle, args=[port, REPEATS])
    t.start()
    threads.append(t)

for t in threads:
    t.join()
