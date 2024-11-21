from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pathfinder


app = FastAPI()

# Добавление middleware для поддержки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"]  # Разрешить все заголовки
)


class Query(BaseModel):
    address: str
    radius: float
    place_type: list[str]


@app.post("/api/places/search/")
async def search_places(data: Query):
    print(data)
    pf = pathfinder.PathFinder(data.address, data.radius, data.place_type)
    test_path = pf.the_dumbest_greedy_algorithm()
    print(test_path)
    results = [{"name": place.__repr__(), "address": place.__repr__(), "coordinates": place.__repr__()} for place in test_path]

    return {"results": results}
    # return test_path
