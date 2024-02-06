from pymongo import MongoClient
from pymongo.database import Database
from src.settings import settings

mongo_client = MongoClient(
    f"mongodb://{settings.mongo_host}:{settings.mongo_port}/",
    username=settings.mongo_username,
    password=settings.mongo_password,
)

def mockable_get_mongo_database(is_test: bool):
    database_name = "challenge"
    if is_test:
        return getattr(mongo_client, f"{database_name}_test")
    return getattr(mongo_client, database_name)


def get_mongo_database(is_test: bool) -> Database:
    from src.database import mockable_get_mongo_database as zas
    database_module = __import__("src.database") 
    return database_module.mockable_get_mongo_database(is_test)

