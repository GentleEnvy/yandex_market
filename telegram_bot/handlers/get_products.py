import re

from services.api_requester import APIRequester
from handlers.base import BaseHandler


class GetProductsHandler(BaseHandler):
    command = '/list'

    def __init__(self, api_requester: APIRequester):
        self.api_requester = api_requester
        self.default_size = 10

    def _parse_args(self, args: str | None):
        if not args:
            return 1, self.default_size
        match = re.fullmatch(r'\s*(\d*)\s*(\d*)', args.strip())
        if match:
            page, size = match.groups()
            page = int(page) if page else 1
            size = int(size) if size else self.default_size
            return page, size
        raise ValueError

    def answer(self, args, **kwargs):
        page, size = self._parse_args(args)
        product_data = self.api_requester.get_products(page=page, page_size=size)
        products = product_data['results']
        total_products = product_data['count']
        total_pages = -(-total_products // size)
        page_size_text = (
            f", размер страницы: {size}" if size != self.default_size else ""
        )
        text = f"📖 Вы на странице: {page}{page_size_text} из {total_pages} 📖\n"
        text += f"🔎 Общее количество отслеживаемых товаров: {total_products} 🔎\n"
        text += (
            "🛍️ Ваш список отслеживаемых товаров: 🛍️\n\n_Товары и их текущие "
            + "цены:_\n"  # black bag
        )
        for product in products:
            id, name, url = product['id'], product['name'], product['url']
            last_price = product['last_price']
            if not name:
                text += f"🔹 №{id} - _Название и цена товара обновляются..._"
            elif not last_price:
                text += f"🔹 №{id} - [{name}]({url}): _цена товара обновляется..._"
            else:
                text += f"🔹 №{id} - [{name}]({url}): *{last_price}* руб.\n"
        text += "\nСледите за изменениями цен и делайте выгодные покупки! 🎁"
        return 'text', {
            'text': text,
            'disable_web_page_preview': True,
            'parse_mode': 'Markdown',
        }
