from fastapi import FastAPI
from src.places import routes as places_router


app = FastAPI()
app.include_router(places_router.router)
