from api_requester import APIRequester
from handlers.base import BaseHandler


class GetProductsHandler(BaseHandler):
    command = '/list'

    def __init__(self):
        self.api_requester = APIRequester()
        self.default_count = 10

    def answer(self, count=None):
        count = int(count) if count else self.default_count
        products = self.api_requester.get_products(page_size=count).json()['results']
        message = "🛍️ Список товаров (_id_: название - *текущая цена*):\n\n"
        for product in products:
            message += (
                f"🔹 _{product['id']}:_ [{product['name']}]({product['url']}) - "
                f"*{product['last_price']}* руб.\n"
            )
        return 'text', {
            'text': message,
            'disable_web_page_preview': True,
            'parse_mode': 'Markdown',
        }
