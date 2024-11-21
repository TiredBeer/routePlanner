from PointObject.Point import Point
from PointObject.GeodesicCoordinates import GeodesicCoordinates


class Address(Point):
    def __init__(self, lon: float, lat: float, answer: dict) -> None:
        super().__init__(GeodesicCoordinates(lat, lon), answer['tags'])
        self.id = answer["id"]
        self.street = answer["street"]
        self.house = answer["house"]
        self.amenity = answer["amenity"]
        self.name = answer["name"]

    def __str__(self):
        return (f"{self.street}, {self.house} at {self.coordinates.latitude},"
                f" {self.coordinates.longitude}")