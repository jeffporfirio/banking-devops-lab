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

        mongo_username = os.getenv("MONGO_USERNAME")
        mongo_password = os.getenv("MONGO_PASSWORD")
        mongo_auth_source = os.getenv(
            "MONGO_AUTH_SOURCE",
            "banking_lab"
        )

        client_options = {
            "serverSelectionTimeoutMS": 3000
        }

        if mongo_username and mongo_password:
            client_options.update({
                "username": mongo_username,
                "password": mongo_password,
                "authSource": mongo_auth_source
            })

        _client = MongoClient(mongo_uri, **client_options)

    return _client["banking_lab"]

def get_collection():
    database = get_database()
    return database["transactions"]