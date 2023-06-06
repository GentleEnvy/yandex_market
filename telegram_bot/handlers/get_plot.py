from io import BytesIO

from services.api_requester import APIRequester
from handlers.base import BaseHandler


class GetPlotHandler(BaseHandler):
    command = '/plot'

    def __init__(self, api_requester: APIRequester):
        self.api_requester = api_requester

    def answer(self, args: str, **kwargs) -> tuple[str, dict]:
        product_id = int(args)
        plot = BytesIO(self.api_requester.get_plot(product_id))
        return 'photo', {'photo': plot}
