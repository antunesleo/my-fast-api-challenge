from uuid import uuid4
from pymongo import MongoClient
import pytest
from src.database import create_indexes
from src.settings import settings


@pytest.fixture
def test_mongo_db(mocker):
    mongo_client = MongoClient(
        f"mongodb://{settings.mongo_host}:{settings.mongo_port}/",
        username=settings.mongo_username,
        password=settings.mongo_password,
    )
    dbname = str(uuid4())
    database = getattr(mongo_client, dbname)
    database.places.create_index({ "name": "text", "description": "text" })
    mocker.patch("src.mockable_get_mongo_database", return_value=database)
    create_indexes()
    yield database
    mongo_client.drop_database(dbname)
