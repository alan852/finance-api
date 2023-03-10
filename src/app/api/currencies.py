from datetime import datetime
from typing import TypedDict

from fastapi import APIRouter, status, Depends, Query

from .auth import Auth0Bearer
from .utils import get_latest_from_db_or_api

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


@router.get("/exchange_rates", status_code=status.HTTP_200_OK)
async def get_exchange_rates(symbols: str = Query(regex=symbols_regex)) -> ExchangeRatesResponse:
    r = get_latest_from_db_or_api()
    return {'timestamp': r['timestamp'],
            'rates': [{'symbol': _, 'rate': r['rates'][_[3:]] / r['rates'][_[:3]]} for _ in symbols.upper().split(',')
                      if _[:3] in r['rates'].keys() and _[3:] in r['rates'].keys()]}
