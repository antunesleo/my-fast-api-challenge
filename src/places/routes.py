from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from src.database import challenge_db
from pymongo.database import Database
from src.places.services import PlaceService
from src.places.repositories import MongoPlaceRepository
from src.places.pydantic_models import Place


router = APIRouter()


def get_place_service() -> PlaceService:
    return PlaceService(MongoPlaceRepository(challenge_db))


@router.post("/places", status_code=status.HTTP_201_CREATED)
def create_places(
    place: Place, service: Annotated[PlaceService, Depends(get_place_service)]
):
    service.create(place)