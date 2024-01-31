from pymongo import MongoClient


mongo_client = MongoClient(
    "mongodb://localhost:27017/", username="root", password="example"
)
challenge_db = mongo_client.challenge
