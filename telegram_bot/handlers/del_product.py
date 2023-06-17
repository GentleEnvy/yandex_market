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
            return 'text', {'text': f"""❌ Ошибочный ID товара !

Вы не отслеживаете товар с ID: {product_id}.
Пожалуйста, убедитесь в корректности введенного ID"""}
        return 'text', {'text': """✅ Успешное удаление товара! ✅

Товар с ID: {product_id} больше не отслеживается"""}
