from typing import Callable
from uuid import uuid4
from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.places.pydantic_models import Location, Place
from src.places.repositories import MongoPlaceRepository
from tests.integration.places.factories import PlaceDBFactory
from pymongo.database import Database

client = TestClient(app)


@pytest.mark.usefixtures("clean_database")
class TestMongoPlaceRepository:
    @pytest.fixture
    def mongo_place_repository(self, mongo_database: Database) -> MongoPlaceRepository:
        return MongoPlaceRepository(mongo_database)

    def test_add(
        self, mongo_database: Database, 
        mongo_place_repository: MongoPlaceRepository, 
    ):
        place_db = PlaceDBFactory()
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

    def test_list_with_no_filter(
        self, mongo_database: Database, 
        mongo_place_repository: MongoPlaceRepository, 
    ):
        mongo_database.places.insert_many([PlaceDBFactory(), PlaceDBFactory()])
        assert len([p for p in mongo_database.places.find()]) == 2

        actual_places = mongo_place_repository.list_with(0, 100)
        assert len(actual_places) == 2
