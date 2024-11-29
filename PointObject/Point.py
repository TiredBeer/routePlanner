from PointObject.GeodesicCoordinates import GeodesicCoordinates


class Point:
    def __init__(self, address: GeodesicCoordinates,
                 tags: set[str] = None):
        self.coordinates = address
        self.tags = tags

    def get_tags(self) -> set[str]:
        return self.tags

    def __repr__(self):
        return f'{self.coordinates}'
