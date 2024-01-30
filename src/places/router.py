from fastapi import APIRouter

router = APIRouter()

@router.post("/places")
def create_places():
    return "not implemented"
