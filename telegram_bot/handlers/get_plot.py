from io import BytesIO

from api_requester import APIRequester
from handlers.base import BaseHandler


class GetPlotHandler(BaseHandler):
    command = '/plot'
    
    def __init__(self):
        self.api_requester = APIRequester()

    def answer(self, args: str = None) -> tuple[str, dict]:
        product_id = int(args)
        plot = BytesIO(self.api_requester.get_plot(product_id))
        return 'photo', {'photo': plot}
