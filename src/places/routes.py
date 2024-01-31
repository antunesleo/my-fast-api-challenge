from typing import Annotated
from fastapi import APIRouter, Depends, status, Security, HTTPException
from fastapi.security import APIKeyHeader
from src.database import challenge_db
from src.places.services import PlaceService
from src.places.repositories import MongoPlaceRepository
from src.places.pydantic_models import Place
from src.settings import settings


router = APIRouter()
api_key_header = APIKeyHeader(name="API-KEY")


def validate_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == settings.global_api_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
    )


def get_place_service() -> PlaceService:
    return PlaceService(MongoPlaceRepository(challenge_db))


@router.post("/places", status_code=status.HTTP_201_CREATED)
def create_places(
    place: Place,
    service: Annotated[PlaceService, Depends(get_place_service)],
    api_key: str = Security(validate_api_key),
):
    service.create(place)
