import random
from datetime import datetime, timedelta
from typing import Iterator
from unittest import TestCase

import pytz
from dotenv import load_dotenv, find_dotenv

from src.app.api.db import Rate, Mongo
from src.app.api.utils import get_env, ENV

load_dotenv(dotenv_path=find_dotenv())


class MongoTest(TestCase):
    db = Mongo(get_env(ENV.MONGO_CONNECTION), get_env(ENV.MONGO_CURRENCIES_DB))

    @staticmethod
    def generate_dummy_rates(start: datetime, end: datetime) -> Iterator[Rate]:
        start = start.replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
        end = end.replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
        while end >= start:
            yield {
                'timestamp': start,
                'base': 'USD',
                'rates': {
                    'HKD': round(random.uniform(7.75, 7.85), 2),
                    'GBP': round(random.uniform(0.71, 0.92), 2)
                }
            }
            start += timedelta(hours=1)

    def test_get_rate(self):
        now = datetime.now().replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
        days = 250
        count = 0
        for r in MongoTest.generate_dummy_rates(now - timedelta(days=days), now):
            if self.db.insert_rate(r):
                count += 1
        self.assertEqual(count, days * 24 + 1)
        r = self.db.get_rate(now)
        self.assertEqual(r['timestamp'].astimezone(pytz.UTC), now)

    def test_get_rates(self):
        now = datetime.now().replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
        self.db.get_rate(now)

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass called')
