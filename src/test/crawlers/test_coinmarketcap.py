from unittest import TestCase

from dotenv import load_dotenv, find_dotenv

from src.app.api.crawlers import CoinMarketCap
from src.app.api.utils import ENV, get_env

load_dotenv(dotenv_path=find_dotenv())


class CoinMarketCapTest(TestCase):
    crawler = CoinMarketCap(api_key=get_env(ENV.CMC_API_KEY))

    def test_get_crypto_rate(self):
        rate = self.crawler.get_crypto_rate(symbols=get_env(ENV.CRYPTO_SYMBOLS).split(','))
        print(rate)
        self.assertIsNotNone(rate)
