from datetime import datetime

import pytz

from .env import get_env, ENV
from ..crawlers import OpenExchangeRates
from ..db import Rate, Mongo


def get_latest_from_db_or_api() -> Rate:
    now = datetime.now().replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
    db = Mongo(get_env(ENV.MONGO_CONNECTION), get_env(ENV.MONGO_CURRENCIES_DB))
    r = db.get_rate(now)
    if r is None:
        crawler = OpenExchangeRates(api_id=get_env(ENV.OER_API_KEY))
        r = crawler.get_rate()
        db.insert_rate(r)
    return r
