from typing import Any, Dict

from .crawler import Crawler


class CoinMarketCap(Crawler):
    base_url = 'https://pro-api.coinmarketcap.com'
    latest_quote_endpoint = 'v1/cryptocurrency/quotes/latest'
    required_fields = ['timestamp', 'base', 'rates']

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_crypto_rate(self, symbols: list[str], base: str = 'USD') -> Dict[str, float]:
        crypto_rates_json = super().get_json(
            url=f'{self.base_url}/{self.latest_quote_endpoint}',
            params=f'CMC_PRO_API_KEY={self.api_key}&convert={base}&symbol={",".join(symbols)}'
        )
        return {symbol: crypto_rates_json['data'][symbol]['quote'][base]['price'] for symbol in symbols}
