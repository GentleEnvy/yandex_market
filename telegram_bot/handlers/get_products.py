from services.api_requester import APIRequester
from handlers.base import BaseHandler


class GetProductsHandler(BaseHandler):
    command = '/list'

    def __init__(self, api_requester: APIRequester):
        self.api_requester = api_requester
        self.default_count = 10

    def answer(self, count, **kwargs):
        count = int(count) if count else self.default_count
        products = self.api_requester.get_products(page_size=count)['results']
        message = "🛍️ Список товаров (_id_: название - *текущая цена*):\n\n"
        for product in products:
            name = product['name'] or '???'
            last_price = product['last_price'] or '???'
            message += (
                f"🔹 _{product['id']}:_ [{name}]({product['url']}) - *{last_price}* "
                f"руб.\n"
            )
        return 'text', {
            'text': message,
            'disable_web_page_preview': True,
            'parse_mode': 'Markdown',
        }
