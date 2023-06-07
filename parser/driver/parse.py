import sys
import time

import undetected_chromedriver as uc

CAPTCHA_STATUS = 42

name_xpaths = (
    '/html/body/div[1]/div[2]/main/div[4]/div/div/div[2]/div/div/div[1]/div[1]/h1',
    '/html/body/div[2]/div[2]/main/div[4]/div/div/div[2]/div/div/div[1]/div[1]/h1',
    '/html/body/div[2]/div[2]/main/div[3]/div/div/div[2]/div/div/div[1]/div[1]/h1',
)
min_price_xpaths = ('//*[@id="cardAddButton"]/div[6]/div/div/a/span/span/span[2]',)
price_xpaths = (
    '//*[@id="cardAddButton"]/div[1]/div/div/div/div/div[3]/div[1]/div/div/div['
    '2]/span/span[1]',
    '//*[@id="cardAddButton"]/div[1]/div/div/div/div/div[4]/div[1]/div/div['
    '1]/div/h3/span[2]',
)
wait_page_time = 0.1
captcha_title = 'Oops!'

options = uc.ChromeOptions()
options.add_argument("--window-size=100,100")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(advanced_elements=True, options=options)

url = sys.argv[1]

driver.get(url)
time.sleep(wait_page_time)
if driver.title == captcha_title:
    sys.exit(CAPTCHA_STATUS)

name = ''
for name_xpath in name_xpaths:
    try:
        name_element = driver.find_elements('xpath', name_xpath)[0]
        name = name_element.text
        break
    except IndexError:
        pass

price = 0
for min_price_xpath in min_price_xpaths:
    try:
        price_element = driver.find_elements('xpath', min_price_xpath)[0]
        price = price_element.text.replace(' ', '').replace('\u2009', '')
        price = int(''.join(filter(lambda s: s.isdigit(), price)))
        break
    except (IndexError, ValueError):
        pass

if not price:
    for price_xpath in price_xpaths:
        try:
            price_element = driver.find_elements('xpath', price_xpath)[0]
            price = int(price_element.text.replace(' ', '').replace('\u2009', ''))
            break
        except (IndexError, ValueError):
            pass

print(f"{name}::{price}")
