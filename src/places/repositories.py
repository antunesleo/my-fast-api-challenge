from abc import ABC, abstractmethod
from pymongo.database import Database

from src.places.pydantic_models import Place


class PlaceRepository(ABC):
    @abstractmethod
    def add(self, place: Place) -> None:
        raise NotImplementedError


class MongoPlaceRepository(PlaceRepository):
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, place: Place) -> None:
        self.db.places.insert_one(
            {
                "name": place.name,
                "description": place.description,
                "location": {
                    "latitude": place.location.latitude,
                    "longitude": place.location.longitude,
                },
            }
        )
