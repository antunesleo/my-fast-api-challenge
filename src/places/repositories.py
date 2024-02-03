from abc import ABC, abstractmethod
from typing import Optional
from pymongo.database import Database

from src.places.pydantic_models import Place, Location


class PlaceRepository(ABC):
    @abstractmethod
    def add(self, place: Place) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_with(
        self, offset: int, limit: int, name: Optional[str] = None
    ) -> list[Place]:
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

    def list_with(
        self, offset: int, limit: int, name: Optional[str] = None
    ) -> list[Place]:
        filters = {}
        if name is not None:
            filters["name"] = {"$regex": name, "$options": "i"}

        places = []
        for place_db in (
            self.db.places.find(filters).skip(offset).limit(limit).sort("name")
        ):
            places.append(
                Place(
                    name=place_db["name"],
                    description=place_db["description"],
                    location=Location(
                        latitude=place_db["location"]["latitude"],
                        longitude=place_db["location"]["longitude"],
                    ),
                )
            )
        return places
