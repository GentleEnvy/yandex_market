from services.api_requester import APIRequester
from handlers.base import BaseHandler


class DelProductHandler(BaseHandler):
    command = '/del'

    def __init__(self, api_requester: APIRequester):
        self.api_requester = api_requester

    def answer(self, args: str, user_id: int = None, **kwargs):
        product_id = int(args)
        try:
            self.api_requester.del_product(product_id, user_id)
        except IndexError:
            return 'text', {
                'text': f"Вы не отслеживаете продукт с id _{product_id}_",
                'parse_mode': 'Markdown',
            }
        return 'text', {
            'text': f"Продукт с id _{product_id}_ был удалён",
            'parse_mode': 'Markdown',
        }
