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
        self,
        offset: int,
        limit: int,
        name: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        radius: Optional[float] = None,
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
                    "type": "Point",
                    "coordinates": [place.location.longitude, place.location.latitude],
                },
            }
        )

    def list_with(
        self,
        offset: int,
        limit: int,
        name: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        radius: Optional[float] = None,
    ) -> list[Place]:
        filters = {}
        if name is not None:
            filters["$text"] = {"$search": name}

        if longitude is not None and latitude is not None and radius is not None:
            radius_kilometers = radius / 1000
            radius_in_radians = radius_kilometers / 6378.1
            filters["location"] = {
                "$geoWithin": {
                    "$centerSphere": [[longitude, latitude], radius_in_radians]
                }
            }

        places = []
        for place_db in (
            self.db.places.find(filters).skip(offset).limit(limit).sort("name")
        ):
            places.append(
                Place(
                    name=place_db["name"],
                    description=place_db["description"],
                    location=Location(
                        latitude=place_db["location"]["coordinates"][1],
                        longitude=place_db["location"]["coordinates"][0],
                    ),
                )
            )
        return places
