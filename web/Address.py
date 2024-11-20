class Point:
    def __init__(self, lon: float, lat: float) -> None:
        self.lon = lon
        self.lat = lat


class ArtObject(Point):
    def __init__(self, lon: float, lat: float, answer: dict) -> None:
        super().__init__(lon, lat)
        self.id = answer['id']
        self.name = answer['name']
        self.amenity = 'art_object'
        self.category = answer['category']
        self.tags = answer['tags']

    def __str__(self) -> str:
        return f'{self.name} at {self.lat}, {self.lon}'


class Address(Point):
    def __init__(self, lon: float, lat: float, answer: dict) -> None:
        super().__init__(lon, lat)
        self.id = answer["id"]
        self.street = answer["street"]
        self.house = answer["house"]
        self.amenity = answer["amenity"]
        self.name = answer["name"]
        self.tags = answer["tags"]

    def __str__(self):
        return f"{self.street}, {self.house} at {self.lat}, {self.lon}"


import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnector:

    _host = 'b19mrygsbv2ejyfwxeb8-postgresql.services.clever-cloud.com'
    _port = 50013
    _user = 'upisxsl8ebyt76zvmwdc'
    _password = 'k7W50CFPTAjR3GsTHZL2PrTQsSV4ud'
    _db_name = 'b19mrygsbv2ejyfwxeb8'

    tags: list[str] = [
        'theatre',
        'restaurant',
        'bar',
        'arts_centre',
        'social_facility',
        'cafe',
        'hookah_lounge',
        'pub',
        'fast_food',
        'place_of_worship',
        'library',
        'university',
    ]

    def __init__(self):
        self.answer = list()
        self._connection = None

    def __enter__(self):
        return self.connect_to_db()

    def get_answer(self, min_lon: float, max_lon: float,
                   min_lat: float, max_lat: float, tags=None) -> list[Point]:
        """
        Выдает список объектов, находящихся в заданных диапахонах с нужными
        тегами и всегда с арт объектами
        :param min_lon: минимальная долгота
        :param max_lon: максимальная долгота
        :param min_lat: минимальная широта
        :param max_lat: максимальная широта
        :param tags: (по умолчанию уже стоят) теги для не арт-объектов
        :return: список из точек, тип которых или Address, или ArtObject
        """
        if tags is None:
            tags = self.tags

        answer = []

        for result in self._get_answer_from_objects((min_lon, max_lon),
                                                    (min_lat, max_lat),
                                                    tags):
            address = Address(float(result['lon']), float(result['lat']),
                              result)
            answer.append(address)

        for result in self._get_answer_from_art((min_lon, max_lon),
                                                (min_lat, max_lat)):
            address = ArtObject(float(result['lon']), float(result['lat']),
                                result)
            answer.append(address)

        return answer

    def _get_answer_from_objects(self,
                   lon: tuple[float, float],
                   lat: tuple[float, float],
                   tags: list[str]) -> list[dict[str, str]]:
        command = self._get_command_for_objects((lon[0], lon[1]),
                                                (lat[0], lat[1]))
        with self._connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(command, (tuple(tags),))
            result = cur.fetchall()

        return result

    def _get_answer_from_art(self,
                    lon: tuple[float, float],
                    lat: tuple[float, float]) -> list[dict[str, str]]:
        command = self._get_command_for_art((lon[0], lon[1]),
                                            (lat[0], lat[1]))
        with self._connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(command)
            result = cur.fetchall()

        return result


    @staticmethod
    def _get_command_for_objects(lon: tuple[float, float],
                     lat: tuple[float, float]) -> str:
        return f"""SELECT * FROM Objects WHERE lon BETWEEN {lon[0]} AND {lon[1]} AND lat BETWEEN {lat[0]} AND {lat[1]} AND amenity IN %s"""

    @staticmethod
    def _get_command_for_art(lon: tuple[float, float],
                                 lat: tuple[float, float]) -> str:
        return f"""SELECT * FROM ArtObjects WHERE lon BETWEEN {lon[0]} AND {lon[1]} AND lat BETWEEN {lat[0]} AND {lat[1]}"""

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
        if exc_type is None:
            print('Произошло это: ', exc_type, exc_val, exc_tb)
            return True
        return False

    def connect_to_db(self):
        try:
            self._connection = psycopg2.connect(
                host=DatabaseConnector._host,
                user=DatabaseConnector._user,
                password=DatabaseConnector._password,
                database=DatabaseConnector._db_name,
                port=DatabaseConnector._port
            )
            return self
        except psycopg2.Error as e:
            print("Ну там бд сдохла похоже, не подключилось к ней :(")
            raise e

    def close_data_base(self):
        self._connection.close()
