from fastapi import FastAPI

from .utils import get_env, ENV
from .currencies import router as router_currencies

app = FastAPI(
    title=get_env(ENV.APP_NAME),
    version=get_env(ENV.APP_VERSION),
    openapi_url=''
)

app.include_router(router_currencies)
