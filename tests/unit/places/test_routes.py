from fastapi.testclient import TestClient
from src.main import app
from src.places.routes import get_place_service

client = TestClient(app)


def test_create_place_succeed(mocker):
    def get_place_service_mock():
        return mocker.patch("src.places.routes.PlaceService", autospec=True)

    app.dependency_overrides[get_place_service] = get_place_service_mock

    payload = {
        "name": "test",
        "description": "test",
        "location": {"latitude": 12, "longitude": 11},
    }

    response = client.post(
        "/places", json=payload, headers={"API-KEY": "youshallnotpass"}
    )
    assert response.status_code == 201
