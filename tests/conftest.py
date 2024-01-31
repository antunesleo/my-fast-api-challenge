import pytest
from src.database import get_mongo_database


@pytest.fixture
def mongo_database():
    return get_mongo_database(is_test=True)
