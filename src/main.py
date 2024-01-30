from typing import Union

from fastapi import FastAPI
from src.places import router as places_router


app = FastAPI()
app.include_router(places_router.router)

@app.get("/ping")
def read_ping():
    return "pong"
