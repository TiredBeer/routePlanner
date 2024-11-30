from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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

# Подключение статических файлов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Query(BaseModel):
    address: str
    radius: float
    place_type: list[str]


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content, status_code=200)


@app.post("/api/places/search/")
async def search_places(data: Query):
    print(data)
    pf = pathfinder.PathFinder(data.address, data.radius, data.place_type)
    test_path = pf.the_dumbest_greedy_algorithm()
    print(test_path)
    results = [{"name": place.__repr__(), "address": place.__repr__(), "coordinates": place.__repr__()} for place in test_path]

    return {"results": results}
