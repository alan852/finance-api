from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypedDict


class Rate(TypedDict):
    timestamp: datetime
    base: str
    rates: dict[str, float]


class DB(ABC):
    @abstractmethod
    def get_latest_rate(self) -> Rate | None:
        pass

    @abstractmethod
    def get_rate(self, timestamp: datetime) -> Rate | None:
        pass

    @abstractmethod
    def insert_rate(self, rates: Rate) -> None:
        pass
