import requests


class APIRequester:
    def __init__(self, secret: str = None):
        self.base_api_url = 'http://api:8000'
        self.requester = requests
        self.secret = secret
        self.auth_header = 'Authorization'
        self.auth_keyword = 'Secret'

    def post_register_telegram(
        self, user_id: int, username: str, first_name: str, last_name: str = None
    ) -> None:
        data = {'telegram_id': user_id, 'username': username, 'first_name': first_name}
        if last_name:
            data['last_name'] = last_name
        url = f"{self.base_api_url}/users/register/telegram/"
        self.requester.post(url, json=data)

    def get_products(self, page: int = 1, page_size: int = 10) -> dict:
        url = f"{self.base_api_url}/products/?{page=}&{page_size=}"
        return self.requester.get(url).json()

    def get_plot(self, product_id: int) -> bytes:
        url = f"{self.base_api_url}/products/{product_id}/plot/"
        response = self.requester.get(url)
        return response.content

    def post_products(self, product_url: str, user_id: int) -> int:
        url = f"{self.base_api_url}/products/"
        response = self.requester.post(
            url, json={'url': product_url}, headers=self._get_headers(user_id)
        )
        return response.json()['id']

    def del_product(self, product_id: int, user_id: int) -> None:
        url = f"{self.base_api_url}/products/{product_id}/"
        response = self.requester.delete(url, headers=self._get_headers(user_id))
        if response.status_code == 404:
            raise IndexError
        if response.status_code != 204:
            raise Exception("Status code != 204")

    def _get_headers(self, user_id: int) -> dict[str, str]:
        if not self.secret:
            raise PermissionError("Secret is empty")
        return {self.auth_header: f"{self.auth_keyword} {self.secret} {user_id}"}
