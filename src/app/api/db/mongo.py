from datetime import datetime

import pymongo
from pymongo import MongoClient

from .db import DB, Rate


class Mongo(DB):
    rate_collection = 'rates'

    def __init__(self, connection_str: str, database: str):
        client = MongoClient(connection_str)
        self.database = client[database]
        self.database[self.rate_collection].create_index([('timestamp', pymongo.DESCENDING)], background=True)

    def get_latest_rate(self) -> Rate | None:
        collection = self.database[self.rate_collection]
        r = collection.find_one(projection={'_id': False}, sort=[('timestamp', pymongo.DESCENDING)])
        return r

    def get_rate(self, timestamp: datetime) -> Rate | None:
        collections = self.database[self.rate_collection]
        return collections.find_one(
            {"timestamp": timestamp},
            projection={'_id': False}
        )

    def insert_rate(self, rate: Rate) -> bool:
        rate['_id'] = f'{rate["timestamp"]} {rate["base"]}'
        collection = self.database[self.rate_collection]
        result = collection.update_one({'_id': rate['_id']}, {"$set": rate}, upsert=True)
        return result.acknowledged
