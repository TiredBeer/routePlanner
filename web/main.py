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
    allow_headers=["*"]   # Разрешить все заголовки
)


class CounterUpdate(BaseModel):
    counter: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/update_counter")
async def update_counter(data: CounterUpdate):
    print(f"Received counter: {data.counter}")
    return {"status": "success", "received_counter": data.counter}
