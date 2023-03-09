from datetime import datetime
from typing import Any

import pytz

from .crawler import Crawler
from ..db import Rate


class OpenExchangeRates(Crawler):
    base_url = 'https://openexchangerates.org/api'
    currencies_endpoint = 'currencies.json'
    latest_endpoint = 'latest.json'
    required_fields = ['timestamp', 'base', 'rates']

    def __init__(self, api_id: str):
        self.app_id = api_id

    def get_currencies(self) -> Any:
        return super().get_json(url=f'{self.base_url}/{self.currencies_endpoint}', params=f'app_id={self.app_id}')

    def get_rate(self, base: str = 'USD') -> Rate:
        currencies_json = self.get_currencies()
        rates_json = super().get_json(
            url=f'{self.base_url}/{self.latest_endpoint}',
            params=f'app_id={self.app_id}&symbols={",".join(currencies_json.keys())}'
        )
        rates_json['timestamp'] = datetime.fromtimestamp(rates_json['timestamp'])\
            .replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
        rates_json = {k: v for k, v in rates_json.items() if k in self.required_fields}
        return rates_json
