from pymongo import MongoClient
from src.settings import settings

mongo_client = MongoClient(
    f"mongodb://{settings.mongo_host}:{settings.mongo_port}/", 
    username=settings.mongo_username, 
    password=settings.mongo_password,
)
challenge_db = mongo_client.challenge
