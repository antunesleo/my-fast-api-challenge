from pymongo import MongoClient
from pymongo.database import Database
from src.settings import settings

mongo_client = MongoClient(
    f"mongodb://{settings.mongo_host}:{settings.mongo_port}/",
    username=settings.mongo_username,
    password=settings.mongo_password,
)

def get_mongo_database(is_test: bool) -> Database:
    database_name = "challenge"
    if is_test:
        return getattr(mongo_client, f"{database_name}_test")
    return getattr(mongo_client, database_name)
