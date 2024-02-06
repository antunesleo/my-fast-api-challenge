from uuid import uuid4
from pymongo import MongoClient
import pytest
from src.database import get_mongo_database
from src.settings import Settings


settings = Settings()


@pytest.fixture
def test_mongo_db(mocker):
    mongo_client = MongoClient(
        f"mongodb://{settings.mongo_host}:{settings.mongo_port}/",
        username=settings.mongo_username,
        password=settings.mongo_password,
    )
    dbname = str(uuid4())
    database = getattr(mongo_client, dbname)
    mocker.patch("src.mockable_get_mongo_database", return_value=database)
    yield database
    mongo_client.drop_database(dbname)
