from PointObject.Point import Point
from PointObject.GeodesicCoordinates import GeodesicCoordinates

from sqlalchemy import Column, Float, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Address(Base, Point):
    __tablename__ = 'Objects'

    id = Column(Integer, primary_key=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    amenity = Column(String, nullable=False)
    tags = Column(JSON, nullable=False)

    def __init__(self) -> None:
        Base.__init__(self)
        Point.__init__(self,
                       GeodesicCoordinates(self.lat, self.lon), self.tags)

    def __str__(self):
        return (f"{self.street}, {self.house} at {self.coordinates.latitude},"
                f" {self.coordinates.longitude}")
