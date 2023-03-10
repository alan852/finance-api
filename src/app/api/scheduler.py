import logging

import requests
from rocketry import Rocketry
from rocketry.conditions.api import cron

from .utils import get_env, ENV, get_latest_from_db_or_api

app = Rocketry(config={"task_execution": "async"})

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


@app.task(cron('0 * * * *'))
async def get_rate():
    get_latest_from_db_or_api()


@app.task(cron('* * * * *'))
async def report_health():
    push_url = get_env(ENV.HEALTH_CHECK_PUSH_URL)
    if push_url is not None and push_url != '':
        requests.get(push_url)
