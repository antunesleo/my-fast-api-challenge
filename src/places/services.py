from dataclasses import dataclass
from typing import Optional
from src.places.pydantic_models import Place
from src.places.repositories import PlaceRepository


class PlaceService:
    def __init__(self, repository: PlaceRepository) -> None:
        self.repository = repository

    def create(self, place: Place) -> None:
        self.repository.add(place)

    def search(self, offset: int, limit: int, name: Optional[str]) -> list[Place]:
        return self.repository.list_with(offset, limit, name)
