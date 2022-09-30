from app.products.driver import Driver
from app.products.models import Product, ProductPrice


class ProductParser:
    def __init__(self):
        self.driver = Driver()
        self.name_xpath = (
            '/html/body/div[4]/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]/div['
            '1]/h1'
        )
        self.price_xpath = (
            '/html/body/div[4]/div[2]/div/div[4]/div/div[2]/div/div/section/div['
            '2]/div/div/div/div/div/div[1]/div/div[2]/span/span[1]'
        )

    def parse(self, product: Product) -> None:
        self.driver.get(product.url)
        name_element = self.driver.find_element_by_xpath(self.name_xpath)
        product.name = name_element.text
        price_element = self.driver.find_element_by_xpath(self.price_xpath)
        price = int(price_element.text.replace(' ', ''))
        product.save()
        if product.last_price != price:
            ProductPrice.objects.create(product=product, price=price)
