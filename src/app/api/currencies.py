from datetime import datetime
from typing import TypedDict

import pytz
from fastapi import APIRouter, status, Depends, Query

from .auth import Auth0Bearer
from .crawlers import OpenExchangeRates
from .db import Mongo, Rate
from .utils import get_env, ENV

router = APIRouter(
    prefix='/currencies',
    tags=["currencies"],
    dependencies=[Depends(Auth0Bearer())],
    responses={404: {"description": "Not found"}}
)


class ExchangeRateResponse(TypedDict):
    symbol: str
    rate: float


class ExchangeRatesResponse(TypedDict):
    timestamp: datetime
    rates: list[ExchangeRateResponse]


symbols_regex = '^(?:[A-Za-z]{6})(?:,[A-Za-z]{6})*$'


def get_latest_from_db_or_api() -> Rate:
    now = datetime.now().replace(minute=0, second=0, microsecond=0).astimezone(pytz.UTC)
    db = Mongo(get_env(ENV.MONGO_CONNECTION), get_env(ENV.MONGO_CURRENCIES_DB))
    r = db.get_rate(now)
    if r is None:
        crawler = OpenExchangeRates(api_id=get_env(ENV.OER_API_KEY))
        r = crawler.get_rate()
        db.insert_rate(r)
    return r


@router.get("/exchange_rates", status_code=status.HTTP_200_OK)
async def get_exchange_rates(symbols: str = Query(regex=symbols_regex)) -> ExchangeRatesResponse:
    r = get_latest_from_db_or_api()
    return {'timestamp': r['timestamp'],
            'rates': [{'symbol': _, 'rate': r['rates'][_[3:]] / r['rates'][_[:3]]} for _ in symbols.upper().split(',')
                      if _[:3] in r['rates'].keys() and _[3:] in r['rates'].keys()]}
