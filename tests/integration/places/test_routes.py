from fastapi.testclient import TestClient
from src.main import app
from src.database import get_mongo_database
from src.settings import settings


client = TestClient(app)


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
