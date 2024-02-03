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

    def assert_place(self, place_db, actual_place):
        actual_place.name == place_db["name"]
        actual_place.description == place_db["description"]
        actual_place.location.latitude == place_db["location"]["latitude"]
        actual_place.location.longitude == place_db["location"]["longitude"]

    def test_add(
        self,
        mongo_database: Database,
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
        self,
        mongo_database: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        first_place_db, second_place_db = PlaceDBFactory(), PlaceDBFactory()
        mongo_database.places.insert_many([first_place_db, second_place_db])
        assert len([p for p in mongo_database.places.find()]) == 2

        actual_places = mongo_place_repository.list_with(0, 100)

        assert len(actual_places) == 2
        self.assert_place(first_place_db, actual_places[0])
        self.assert_place(second_place_db, actual_places[1])

    def test_list_with_name(
        self,
        mongo_database: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        place_db = PlaceDBFactory(name="zas")
        mongo_database.places.insert_many(
            [place_db, PlaceDBFactory(name="zes")]
        )
        assert len([p for p in mongo_database.places.find()]) == 2

        actual_places = mongo_place_repository.list_with(0, 100, "za")

        assert len(actual_places) == 1
        self.assert_place(place_db, actual_places[0])

    def test_list_with_filtering_by_offset_and_limit(
        self,
        mongo_database: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        places_db = PlaceDBFactory.build_batch(5)
        mongo_database.places.insert_many(places_db)
        assert len([p for p in mongo_database.places.find()]) == 5

        actual_places = mongo_place_repository.list_with(0, 1)
        assert len(actual_places) == 1
        self.assert_place(places_db[0], actual_places[0])

        actual_places = mongo_place_repository.list_with(2, 3)
        assert len(actual_places) == 3
        self.assert_place(places_db[2], actual_places[0])
        self.assert_place(places_db[3], actual_places[1])
        self.assert_place(places_db[4], actual_places[2])

        actual_places = mongo_place_repository.list_with(5, 3)
        assert len(actual_places) == 0
