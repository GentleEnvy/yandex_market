from services.api_requester import APIRequester
from handlers.base import BaseHandler


class AddProductHandler(BaseHandler):
    command = '/add'

    def __init__(self, api_requester: APIRequester):
        self.api_requester = api_requester

    def answer(self, args: str, user_id: int = None, **kwargs):
        product_id = self.api_requester.post_products(args, user_id)
        return 'text', {
            'text': f"Продукт зарегистрирован под id _{product_id}_",
            'parse_mode': 'Markdown',
        }
