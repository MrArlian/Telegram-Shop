import hashlib
import typing
import time
import hmac
import json

import requests


BASE_URL = 'https://api.freekassa.ru/v1'


class FreeKassa:

    def __init__(self, api_key: str, shop_id: int) -> None:
        self.shop_id = int(shop_id)
        self.api_key = api_key

        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    def _do_request(self,
                    method: str,
                    path: typing.Union[str, typing.Iterable],
                    data: dict = None) -> dict:

        if isinstance(path, str):
            path = (path, )

        url = '/'.join([BASE_URL, *path])
        data = json.dumps(data or {})

        result = self.session.request(method, url, data=data)

        return result.json()

    def _signature(self, data: dict) -> str:
        """
            Generates a signature for the Free-Kassa merchant.
        """

        sorted_data = '|'.join(str(data[key]) for key in sorted(data.keys()))
        sha256 = hmac.new(self.api_key.encode(), sorted_data.encode(), hashlib.sha256)

        return sha256.hexdigest()

    def create_order(self, amount: float, system: int, currency: str = 'RUB') -> dict:
        """
            Creates an order in the Free-kassa merchant.
        """

        data = {
            'shopId': self.shop_id,
            'nonce': int(time.time()),
            'currency': currency,
            'amount': int(amount) if amount.is_integer() else amount,
            'i': system,
            'email': 'example@example.com',
            'ip': ''
        }
        data['signature'] = self._signature(data)
        return self._do_request('post', ('orders', 'create'), data)

    def check(self, order_id: int) -> dict:
        """
            Checks order status.
        """

        data = {
            'shopId': self.shop_id,
            'nonce': int(time.time()),
            'orderId': order_id
        }
        data['signature'] = self._signature(data)
        return self._do_request('post', 'orders', data)['orders'][0]
