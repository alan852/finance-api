import asyncio
import logging

from dotenv import load_dotenv, find_dotenv
from uvicorn import Server, Config
from api import api_app, scheduler_app

load_dotenv(dotenv_path=find_dotenv())


class FinanceApiServer(Server):
    def handle_exit(self, sig: int, frame) -> None:
        scheduler_app.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    server = FinanceApiServer(
        config=Config(api_app, proxy_headers=True, host='0.0.0.0', port=80, workers=1, loop='asyncio')
    )

    api = asyncio.create_task(server.serve())
    scheduler = asyncio.create_task(scheduler_app.serve())

    await asyncio.wait([api, scheduler])


if __name__ == '__main__':
    asyncio.run(main())
