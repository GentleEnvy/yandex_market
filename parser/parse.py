import sys
import time
import random

import undetected_chromedriver as uc


class Parser:
    def __init__(self):
        self.driver = None
        self.name_xpaths = (
            '/html/body/div[1]/div[2]/main/div[4]/div/div/div[2]/div/div/div[1]/div['
            '1]/h1',
            '/html/body/div[2]/div[2]/main/div[4]/div/div/div[2]/div/div/div[1]/div['
            '1]/h1',
            '/html/body/div[2]/div[2]/main/div[3]/div/div/div[2]/div/div/div[1]/div['
            '1]/h1',
        )
        self.price_xpaths = (
            '//*[@id="cardAddButton"]/div[1]/div/div/div/div/div[3]/div['
            '1]/div/div/div[2]/span/span[1]',
            '//*[@id="cardAddButton"]/div[1]/div/div/div/div/div[4]/div[1]/div/div['
            '1]/div/h3/span[2]',
        )
        self.max_tries = 3

        self.driver = uc.Chrome()

    def sleep(self, sec: float) -> None:
        add_sec = random.uniform(sec * 0.1, sec * 0.3)
        time.sleep(sec + add_sec)

    def parse(self, url: str) -> tuple[str, int]:
        self.driver.get(url)
        self.sleep(3)
        if self.driver.title == 'Oops!':
            raise PermissionError
        name = self._parse_name()
        price = self._parse_price()
        return name, price

    def _parse_name(self) -> str:
        for name_xpath in self.name_xpaths:
            try:
                name_element = self.driver.find_elements('xpath', name_xpath)[0]
                return name_element.text
            except IndexError:
                pass
        return ''

    def _parse_price(self) -> int:
        for price_xpath in self.price_xpaths:
            try:
                price_element = self.driver.find_elements('xpath', price_xpath)[0]
                return int(price_element.text.replace(' ', '').replace('\u2009', ''))
            except (IndexError, ValueError):
                pass
        return 0


def main():
    parser = Parser()
    url = sys.argv[1]
    try:
        name, price = parser.parse(url)
        print(f"{name}::{price}")
    except PermissionError:
        exit(-1)


if __name__ == '__main__':
    main()
