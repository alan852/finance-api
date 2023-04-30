from datetime import datetime

import pytz

from .env import get_env, ENV
from ..crawlers import OpenExchangeRates, CoinMarketCap
from ..db import Rate, Mongo


def get_latest_from_db_or_api() -> Rate:
    now = datetime.now().replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
    db = Mongo(get_env(ENV.MONGO_CONNECTION), get_env(ENV.MONGO_CURRENCIES_DB))
    r = db.get_rate(now)
    if r is None:
        crawler = OpenExchangeRates(api_key=get_env(ENV.OER_API_KEY))
        r = crawler.get_rate()
        crawler = CoinMarketCap(api_key=get_env(ENV.CMC_API_KEY))
        symbols = get_env(ENV.CRYPTO_SYMBOLS).split(',')
        cr = crawler.get_crypto_rate(symbols=symbols)
        for symbol in symbols:
            r['rates'][symbol] = cr[symbol]
        db.insert_rate(r)
        r = db.get_latest_rate()
    return r
