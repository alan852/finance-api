import os
from enum import Enum


class ENV(Enum):
    APP_NAME = {'name': 'APP_NAME', 'default': 'Personal Finance API'}
    APP_VERSION = {'name': 'APP_VERSION', 'default': '1.0.0'}
    AUTH0_DOMAIN = {'name': 'AUTH0_DOMAIN', 'default': ''}
    AUTH0_API_AUDIENCE = {'name': 'AUTH0_API_AUDIENCE', 'default': ''}
    AUTH0_ISSUER = {'name': 'AUTH0_ISSUER', 'default': ''}
    AUTH0_ALGORITHMS = {'name': 'AUTH0_ALGORITHMS', 'default': 'RS256'}
    OER_API_KEY = {'name': 'OER_API_KEY', 'default': ''}
    CMC_API_KEY = {'name': 'CMC_API_KEY', 'default': ''}
    CRYPTO_SYMBOLS = {'name': 'CRYPTO_SYMBOLS', 'default': 'BTC'}
    MONGO_CONNECTION = {'name': 'MONGO_CONNECTION', 'default': ''}
    MONGO_CURRENCIES_DB = {'name': 'MONGO_CURRENCIES_DB', 'default': ''}
    HEALTH_CHECK_PUSH_URL = {'name': 'HEALTH_CHECK_PUSH_URL', 'default': ''}


def get_env(env: ENV):
    return os.environ.get(env.value['name'], env.value['default'])
