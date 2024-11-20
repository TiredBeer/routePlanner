from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    # Здесь вы можете добавить логику поиска интересных мест
    # Пример данных для демонстрации
    print(data)
    results = [
        {"name": "Музей искусств", "address": "ул. Ленина, 10"},
        {"name": "Театр драмы", "address": "просп. Мира, 5"}
    ]

    return {"results": results}
