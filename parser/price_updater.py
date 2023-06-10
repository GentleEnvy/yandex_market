import subprocess
import time
import random

from app.products.models import Product


class PriceUpdater:
    class ParseException(Exception):
        pass

    def __init__(self):
        self.driver_image = 'yandex_market_driver'
        self.max_tries = 2
        self.inter_requests_time = 135
        self.captcha_status = 42
        self.captcha_wait = 60 * 40

    def sleep(self, sec: float) -> None:
        add_sec = random.uniform(sec * 0.01, sec * 0.1)
        time.sleep(sec + add_sec)

    def update(self, product: Product) -> tuple[str, int]:
        for i in range(self.max_tries):
            command = [
                'docker',
                'run',
                '-t',
                '--rm',
                self.driver_image,
                './start.sh',
                product.url,
            ]
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            logs = stdout.decode()
            status = process.returncode
            if not status:
                name, price = logs.splitlines()[-1].split('::')
                print(f"{name}::{price}")
                price = int(price)
                if price:
                    self.sleep(self.inter_requests_time)
                    return name, price
            else:
                if status == self.captcha_status:
                    print('Oops!')
                    self.sleep(self.captcha_wait)
                else:
                    print('crash')
            self.sleep(self.inter_requests_time)
        raise self.ParseException
