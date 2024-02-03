from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.settings import settings
from tests.integration.places.factories import PlaceDBFactory


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
    def test_succeed_with_no_filter(mocker, mongo_database):
        place_db = PlaceDBFactory()
        mongo_database.places.insert_one(place_db)
        response = client.get("/places", headers={"API-KEY": settings.global_api_key})
        assert response.status_code == 200
        actual_places = response.json()
        assert len(actual_places) == 1

        assert actual_places[0]["name"] == place_db["name"]
        assert actual_places[0]["description"] == place_db["description"]
        assert (
            actual_places[0]["location"]["latitude"] == place_db["location"]["latitude"]
        )
        assert (
            actual_places[0]["location"]["longitude"]
            == place_db["location"]["longitude"]
        )
