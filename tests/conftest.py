import pytest
from src.database import get_mongo_database


@pytest.fixture
def mongo_database():
    return get_mongo_database(is_test=True)


@pytest.fixture
def clean_database(mongo_database):
    yield
    mongo_database.places.drop()
