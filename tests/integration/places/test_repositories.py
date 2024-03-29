from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.places.pydantic_models import Location, Place
from src.places.repositories import MongoPlaceRepository
from tests.integration.places.factories import LocationDBFactory, PlaceDBFactory
from pymongo.database import Database

client = TestClient(app)


@pytest.mark.usefixtures("test_mongo_db")
class TestMongoPlaceRepository:
    @pytest.fixture
    def mongo_place_repository(self, test_mongo_db: Database) -> MongoPlaceRepository:
        return MongoPlaceRepository(test_mongo_db)

    def assert_place(self, place_db, actual_place):
        actual_place.name == place_db["name"]
        actual_place.description == place_db["description"]
        actual_place.location.latitude == place_db["location"]["coordinates"][1]
        actual_place.location.longitude == place_db["location"]["coordinates"][0]

    def test_add(
        self,
        test_mongo_db: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        place_db = PlaceDBFactory()
        assert len([p for p in test_mongo_db.places.find(place_db)]) == 0
        test_mongo_db.places.insert_one(place_db)
        place = Place(
            name=place_db["name"],
            description=place_db["description"],
            location=Location(
                latitude=place_db["location"]["coordinates"][1],
                longitude=place_db["location"]["coordinates"][0],
            ),
        )
        mongo_place_repository.add(place)

        assert len([p for p in test_mongo_db.places.find(place_db)]) == 1

    def test_list_with_no_filter(
        self,
        test_mongo_db: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        first_place_db, second_place_db = PlaceDBFactory(), PlaceDBFactory()
        test_mongo_db.places.insert_many([first_place_db, second_place_db])
        assert len([p for p in test_mongo_db.places.find()]) == 2

        actual_places = mongo_place_repository.list_with(0, 100)

        assert len(actual_places) == 2
        self.assert_place(first_place_db, actual_places[0])
        self.assert_place(second_place_db, actual_places[1])

    def test_list_with_name(
        self,
        test_mongo_db: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        place_db = PlaceDBFactory(name="zas zes")
        test_mongo_db.places.insert_many([place_db, PlaceDBFactory(name="zes zis")])
        assert len([p for p in test_mongo_db.places.find()]) == 2

        actual_places = mongo_place_repository.list_with(0, 100, "zas")

        assert len(actual_places) == 1
        self.assert_place(place_db, actual_places[0])

    def test_list_with_filtering_by_offset_and_limit(
        self,
        test_mongo_db: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        places_db = PlaceDBFactory.build_batch(5)
        test_mongo_db.places.insert_many(places_db)
        assert len([p for p in test_mongo_db.places.find()]) == 5

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

    def test_list_with_location(
        self,
        test_mongo_db: Database,
        mongo_place_repository: MongoPlaceRepository,
    ):
        place_db_within_radius = PlaceDBFactory(
            location=LocationDBFactory(coordinates=[-49.254984, -25.439095]),
        )
        place_db_outside_radius = PlaceDBFactory(
            location=LocationDBFactory(coordinates=[-49.328086, -25.427196]),
        )
        test_mongo_db.places.insert_many(
            [place_db_within_radius, place_db_outside_radius]
        )
        assert len([p for p in test_mongo_db.places.find()]) == 2

        actual_places = mongo_place_repository.list_with(
            0, 100, longitude=-49.254337, latitude=-25.439062, radius=500
        )

        assert len(actual_places) == 1
        self.assert_place(place_db_within_radius, actual_places[0])
