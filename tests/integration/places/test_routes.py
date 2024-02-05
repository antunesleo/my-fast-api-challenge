from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.settings import settings
from tests.integration.places.factories import LocationDBFactory, PlaceDBFactory


client = TestClient(app)


@pytest.mark.usefixtures("clean_database")
class TestRouteCreatePlace:
    def test_when_succeed(mocker, mongo_database):
        payload = {
            "name": "test",
            "description": "test",
            "location": {"latitude": 12, "longitude": 11},
        }

        response = client.post(
            "/places", json=payload, headers={"API-KEY": settings.global_api_key}
        )
        assert response.status_code == 201
        mongo_place = mongo_database.places.find_one({"name": "test"})

        assert payload["name"] == mongo_place["name"]
        assert payload["description"] == mongo_place["description"]
        assert payload["location"] == mongo_place["location"]


@pytest.mark.usefixtures("clean_database")
class TestSearchPlace:
    def assert_place_db_and_place_json(self, place_db, place_json):
        assert place_json["name"] == place_db["name"]
        assert place_json["description"] == place_db["description"]
        assert (
            place_json["location"]["latitude"] == place_db["location"]["coordinates"][1]
        )
        assert (
            place_json["location"]["longitude"]
            == place_db["location"]["coordinates"][0]
        )

    def test_succeed_with_no_filter(self, mongo_database):
        place_db = PlaceDBFactory()
        mongo_database.places.insert_one(place_db)
        response = client.get("/places", headers={"API-KEY": settings.global_api_key})
        assert response.status_code == 200
        actual_places = response.json()
        assert len(actual_places) == 1

        self.assert_place_db_and_place_json(place_db, actual_places[0])

    def test_succeed_filtering_by_name(self, mongo_database):
        place_db = PlaceDBFactory()
        mongo_database.places.insert_many([place_db, PlaceDBFactory()])
        response = client.get(
            "/places",
            params={"name": place_db["name"]},
            headers={"API-KEY": settings.global_api_key},
        )
        assert response.status_code == 200
        actual_places = response.json()
        assert len(actual_places) == 1
        self.assert_place_db_and_place_json(place_db, actual_places[0])

    def test_succeed_filtering_by_location(self, mongo_database):
        place_db_within_radius = PlaceDBFactory(
            location=LocationDBFactory(coordinates=[-49.254984, -25.439095]),
        )
        place_db_outside_radius = PlaceDBFactory(
            location=LocationDBFactory(coordinates=[-49.328086, -25.427196]),
        )
        mongo_database.places.insert_many(
            [place_db_within_radius, place_db_outside_radius]
        )
        response = client.get(
            "/places",
            params={"longitude": -49.254337, "latitude": -25.439062, "radius": 500},
            headers={"API-KEY": settings.global_api_key},
        )
        assert response.status_code == 200
        actual_places = response.json()
        assert len(actual_places) == 1
        self.assert_place_db_and_place_json(place_db_within_radius, actual_places[0])
