from unittest.mock import MagicMock
import pytest
from src.places.pydantic_models import Location, Place
from src.places.services import PlaceService


class TestPlaceService:
    @pytest.fixture
    def place_repository_mock(self, mocker) -> MagicMock:
        return mocker.patch("src.places.services.PlaceRepository", autospec=True)

    @pytest.fixture
    def place_service(self, place_repository_mock: MagicMock) -> PlaceService:
        return PlaceService(place_repository_mock)

    def test_create(
        self, place_service: PlaceService, place_repository_mock: MagicMock
    ):
        place = Place(
            name="test name",
            description="test description",
            location=Location(
                latitude=57.45,
                longitude=53.11,
            ),
        )
        place_service.create(place)
        place_repository_mock.add.assert_called_once_with(place)

    def test_search_with_name(
        self, place_service: PlaceService, place_repository_mock: MagicMock
    ):
        list_with_return = [MagicMock()]
        place_repository_mock.list_with.return_value = list_with_return
        actual_places = place_service.search(1, 10, "filter")
        place_repository_mock.list_with.assert_called_once_with(1, 10, "filter", None, None, None)
        assert actual_places == list_with_return

    def test_search_with_location(
        self, place_service: PlaceService, place_repository_mock: MagicMock
    ):
        list_with_return = [MagicMock()]
        place_repository_mock.list_with.return_value = list_with_return
        actual_places = place_service.search(1, 10, latitude=45.45, longitude=46.46, radius=500)
        place_repository_mock.list_with.assert_called_once_with(1, 10, name=None, latitude=45.45, longitude=46.46, radius=500)
        assert actual_places == list_with_return
