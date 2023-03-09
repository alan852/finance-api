from abc import ABC, abstractmethod
from typing import Any

import requests

from ..db.db import Rate


class Crawler(ABC):
    session = requests.Session()

    def get_json(self, url: str, params: str) -> Any:
        r = self.session.get(url=url, params=params)
        r.raise_for_status()
        return r.json()

    @abstractmethod
    def get_rate(self, base: str = 'USD') -> Rate:
        pass
