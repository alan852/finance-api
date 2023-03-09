from datetime import datetime
from unittest import TestCase

import pytz
from dotenv import load_dotenv, find_dotenv

from src.app.api.crawlers import OpenExchangeRates
from src.app.api.utils import ENV, get_env

load_dotenv(dotenv_path=find_dotenv())


class OpenExchangeRatesTest(TestCase):
    crawler = OpenExchangeRates(api_id=get_env(ENV.OER_API_KEY))

    def test_get_currencies(self):
        symbol = 'USD'
        currencies = self.crawler.get_currencies()
        self.assertIsNotNone(currencies)
        self.assertTrue(symbol in currencies.keys())
        self.assertEqual(currencies[symbol], 'United States Dollar')

    def test_get_rate(self):
        now = datetime.now().replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
        rate = self.crawler.get_rate()
        print(rate)
        self.assertIsNotNone(rate)
        self.assertEqual(rate['timestamp'], now)
        self.assertEqual(rate['base'], 'USD')
        self.assertTrue('GBP' in rate['rates'].keys())
