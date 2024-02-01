from fastapi.testclient import TestClient
from fastapi import status
import pytest
from src.main import app
from src.places.routes import get_place_service
from src.settings import settings


client = TestClient(app)


@pytest.mark.usefixtures("override_place_service_dependency")
class TestRouteCreatePlace:
    @pytest.fixture
    def payload(self) -> dict:
        return {
            "name": "test",
            "description": "test",
            "location": {"latitude": 12, "longitude": 11},
        }

    @pytest.fixture
    def override_place_service_dependency(self, mocker):
        def get_place_service_mock():
            return mocker.patch("src.places.routes.PlaceService", autospec=True)

        app.dependency_overrides[get_place_service] = get_place_service_mock

    def test_succeed(self, payload):
        response = client.post(
            "/places", json=payload, headers={"API-KEY": settings.global_api_key}
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_authentication_fail(self, payload):
        response = client.post("/places", json=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authorization_fail(self, payload):
        response = client.post("/places", json=payload, headers={"API-KEY": "wrongKey"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
