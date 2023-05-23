import time
import random

from django.conf import settings
import docker
from docker.errors import ContainerError

from app.products.models import Product


class ProductParser:
    class ParseException(Exception):
        pass

    def __init__(self):
        self.docker_client = docker.from_env()
        self.max_tries = 3
        self.inter_requests_time = 10
        self.captcha_status = 42
        self.captcha_wait = 30 * 60

    def sleep(self, sec: float) -> None:
        add_sec = random.uniform(sec * 0.01, sec * 0.1)
        time.sleep(sec + add_sec)

    def parse(self, product: Product) -> tuple[str, int]:
        for i in range(self.max_tries):
            if i:
                print(f"try: {i}")
            try:
                logs = self.docker_client.containers.run(
                    settings.PARSER_IMAGE_NAME,
                    f'./start.sh "{product.url}"',
                    remove=True,
                ).decode()
                name, price = logs.splitlines()[-1].split('::')
                price = int(price)
                if price:
                    self.sleep(self.inter_requests_time)
                    return name, price
            except ContainerError as exc:
                if exc.exit_status == self.captcha_status:
                    print('Oops!')
                    self.sleep(self.captcha_wait)
                else:
                    print('crash')
            self.sleep(self.inter_requests_time)
        raise self.ParseException
