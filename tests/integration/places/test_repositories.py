from typing import Callable
from uuid import uuid4
from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.places.pydantic_models import Location, Place
from src.places.repositories import MongoPlaceRepository
from src.settings import settings
from pymongo.database import Database

client = TestClient(app)


class TestMongoPlaceRepository:
    @pytest.fixture
    def mongo_place_repository(self, mongo_database: Database) -> MongoPlaceRepository:
        return MongoPlaceRepository(mongo_database)

    @pytest.fixture
    def place_db_factory():
        def inner() -> dict:
            return {
                "name": f"name {uuid4()}",
                "description": f"description {uuid4()}",
                "location": {
                    "latitude": 45.45,
                    "longitude": 46.46,
                },
            }
        return inner

    def test_add(
        self, mongo_database: Database, 
        mongo_place_repository: MongoPlaceRepository, 
        place_db_factory: Callable[[], dict]
    ):
        place_db = place_db_factory()
        assert len([p for p in mongo_database.places.find(place_db)]) == 0
        mongo_database.places.insert_one(place_db)
        place = Place(
            name=place_db["name"],
            description=place_db["description"],
            location=Location(
                latitude=place_db["location"]["latitude"],
                longitude=place_db["location"]["longitude"],
            ),
        )
        mongo_place_repository.add(place)

        assert len([p for p in mongo_database.places.find(place_db)]) == 1
