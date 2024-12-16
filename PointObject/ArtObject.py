from PointObject.Point import Point
from PointObject.GeodesicCoordinates import GeodesicCoordinates

from sqlalchemy import Column, Float, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ArtObject(Base, Point):
    __tablename__ = 'ArtObjects'

    id = Column(Integer, primary_key=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    amenity = 'art_object'
    category = Column(String, nullable=False)

    def __init__(self):
        Base.__init__(self)
        Point.__init__(self, GeodesicCoordinates(latitude=self.lat,
                                                 longitude=self.lon),
                       set(self.category))

    def __str__(self) -> str:
        return (f'{self.name} at {self.coordinates.latitude}, '
                f'{self.coordinates.longitude}')