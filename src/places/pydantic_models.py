from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float


class Place(BaseModel):
    name: str
    description: str
    location: Location
