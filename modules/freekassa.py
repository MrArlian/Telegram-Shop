import urllib.parse
import hashlib
import typing
import time
import hmac
import json

import requests


PAYMENT_URL = 'https://pay.freekassa.ru/'
API_URL = 'https://api.freekassa.ru/v1'


class FreeKassa:

    def __init__(self, api_key: str, shop_id: int, secret = None) -> None:
        self.shop_id = int(shop_id)
        self.api_key = api_key
        self._secret = secret

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

        url = '/'.join([API_URL, *path])
        data = json.dumps(data or {})

        result = self.session.request(method, url, data=data)

        return result.json()

    def _signature(self, data: dict) -> str:
        sorted_data = '|'.join(str(data[key]) for key in sorted(data.keys()))
        sha256 = hmac.new(self.api_key.encode(), sorted_data.encode(), hashlib.sha256)

        return sha256.hexdigest()

    def _signature_url(self, amount: float, order_id: int, currency: str = 'RUB') -> str:
        signature = ':'.join(map(str, (self.shop_id, amount, self._secret, currency, order_id)))
        md5 = hashlib.md5(signature.encode())

        return md5.hexdigest()

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

    def generate_payment_url(self,
                             amount: float,
                             order_id: int = None,
                             currency: str = 'RUB') -> str:
        """
            Generates a payment link.
        """

        data = {
            'm': self.shop_id,
            'oa': amount,
            'o': order_id or int(time.time()),
            'currency': currency,
            's': self._signature_url(amount, order_id)
        }
        return f'{PAYMENT_URL}?{urllib.parse.urlencode(data)}'
