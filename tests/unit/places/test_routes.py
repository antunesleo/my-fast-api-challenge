from fastapi.testclient import TestClient
from fastapi import status
import pytest
from src.main import app
from src.places.pydantic_models import Location, Place
from src.places.routes import get_place_service
from src.settings import settings


client = TestClient(app)


@pytest.fixture
def place_service_mock(mocker):
    return mocker.patch("src.places.routes.PlaceService", autospec=True)


@pytest.fixture
def override_place_service_dependency(place_service_mock):
    def get_place_service_mock():
        return place_service_mock

    app.dependency_overrides[get_place_service] = get_place_service_mock


@pytest.mark.usefixtures("override_place_service_dependency")
class TestRouteCreatePlace:
    @pytest.fixture
    def payload(self) -> dict:
        return {
            "name": "test",
            "description": "test",
            "location": {"latitude": 12.0, "longitude": 11.0},
        }

    def test_succeed(self, payload, place_service_mock):
        expected_place = Place(
            name=payload["name"],
            description=payload["description"],
            location=Location(
                latitude=payload["location"]["latitude"],
                longitude=payload["location"]["longitude"],
            ),
        )
        response = client.post(
            "/places", json=payload, headers={"API-KEY": settings.global_api_key}
        )
        assert response.status_code == status.HTTP_201_CREATED
        place_service_mock.create.assert_called_once_with(expected_place)

    def test_authentication_fail(self, payload):
        response = client.post("/places", json=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authorization_fail(self, payload):
        response = client.post("/places", json=payload, headers={"API-KEY": "wrongKey"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("override_place_service_dependency")
class TestRouteSearchPlace:
    def test_search_with_no_filter(self, place_service_mock):
        response = client.get(
            "/places", headers={"API-KEY": settings.global_api_key}
        )
        assert response.status_code == status.HTTP_200_OK
        place_service_mock.search.assert_called_once_with(1, 100, None)

    def test_authentication_fail(self):
        response = client.get("/places")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authorization_fail(self):
        response = client.get("/places", headers={"API-KEY": "wrongKey"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
