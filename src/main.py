from fastapi import FastAPI
from src.places import routes as places_router
from src.database import create_indexes


app = FastAPI()
app.include_router(places_router.router)
create_indexes()
