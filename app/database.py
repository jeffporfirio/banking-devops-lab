import os

from pymongo import MongoClient


_client = None


def get_database():
    global _client

    if _client is None:
        mongo_uri = os.getenv(
            "MONGO_URI",
            "mongodb://localhost:27017"
        )

        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=3000
        )

    return _client["banking_lab"]


def get_collection():
    database = get_database()
    return database["transactions"]