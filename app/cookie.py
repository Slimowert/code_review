import time
import undetected_chromedriver as uc


def get_cookies():
    print("Создаются куки сесии")
    driver = uc.Chrome(version_main=114, headless=True)
    driver.maximize_window()
    driver.get('https://www.dns-shop.ru/')
    time.sleep(3)
    cookies = driver.get_cookies()
    c = {c['name']:c['value'] for c in cookies}
    driver.close()
    driver.quit()
    return c

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}