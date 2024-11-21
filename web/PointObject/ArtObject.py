from PointObject.Point import Point
from PointObject.GeodesicCoordinates import GeodesicCoordinates


class ArtObject(Point):
    def __init__(self, lon: float, lat: float, answer: dict) -> None:
        super().__init__(GeodesicCoordinates(lat, lon), answer['tags'])
        self.id = answer['id']
        self.name = answer['name']
        self.amenity = 'art_object'
        self.category = answer['category']

    def __str__(self) -> str:
        return (f'{self.name} at {self.coordinates.latitude}, '
                f'{self.coordinates.longitude}')