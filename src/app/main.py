from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI

from api import router_currencies
from api.utils import get_env, ENV

load_dotenv(dotenv_path=find_dotenv())

app = FastAPI(
    title=get_env(ENV.APP_NAME),
    version=get_env(ENV.APP_VERSION),
    openapi_url=''
)

app.include_router(router_currencies)
