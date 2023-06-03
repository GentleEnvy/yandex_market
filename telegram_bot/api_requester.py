import requests


class APIRequester:
    def __init__(self):
        self.base_api_url = 'http://api:8000'
        self.requester = requests
    
    def get_products(self, page: int = 1, page_size: int = 10):
        url = f"{self.base_api_url}/products/?{page=}&{page_size=}"
        return self.requester.get(url)

    def get_plot(self, product_id: int) -> bytes:
        url = f"{self.base_api_url}/products/{product_id}/plot/"
        response = self.requester.get(url)
        return response.content
