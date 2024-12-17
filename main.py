import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from pathfinder import PathFinder


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Query(BaseModel):
    address: str
    radius: float
    place_type: list[str]


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Запрос: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Ответ: статус {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Ошибка во время обработки запроса: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@app.post("/api/places/search/")
async def search_places(data: Query):
    logger.info(f"Получены данные запроса: {data}")
    try:
        pf = PathFinder.PathFinder(data.address, data.radius, data.place_type)
        test_path = pf.the_dumbest_greedy_algorithm()
        logger.info("Выполнен алгоритм поиска путей")

        results = [
            {"name": place.__repr__(), "address": place.__repr__(), "coordinates": place.__repr__()}
            for place in test_path
        ]
        logger.info(f"Результаты поиска: {results}")

        return {"results": results}

    except ValidationError as e:
        logger.error(f"Ошибка валидации данных: {e}")
        raise HTTPException(status_code=422, detail="Неверный формат данных")

    except AttributeError as e:
        logger.error(f"Ошибка в работе PathFinder: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса")

    except Exception as e:
        logger.exception("Произошла неожиданная ошибка")
        raise HTTPException(status_code=500, detail="Произошла непредвиденная ошибка")


