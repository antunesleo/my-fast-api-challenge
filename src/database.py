from pymongo import MongoClient
from pymongo.database import Database
from src.settings import settings

mongo_client = MongoClient(
    f"mongodb://{settings.mongo_host}:{settings.mongo_port}/",
    username=settings.mongo_username,
    password=settings.mongo_password,
)
mongo_database = None


def mockable_get_mongo_database():
    global mongo_database
    if mongo_database is not None:
        return mongo_database
    
    mongo_database = getattr(mongo_client, "challenge")
    return mongo_database


def get_mongo_database() -> Database:
    from src.database import mockable_get_mongo_database as zas
    database_module = __import__("src.database") 
    return database_module.mockable_get_mongo_database()


def create_indexes():
    mongo_database = get_mongo_database()
    mongo_database.places.create_index({ "name": "text", "description": "text" })
