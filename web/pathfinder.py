import math
import pymap3d as pm
import Address
import APIYandex


class PlaneCoordinates:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_distance_to(self, other) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def get_length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class GeodesicCoordinates:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def convert_to_plane(self, conversion_point) -> PlaneCoordinates:
        result = pm.geodetic2enu(self.latitude, self.longitude, 0,
                                 conversion_point.latitude,
                                 conversion_point.longitude,
                                 0)
        return PlaneCoordinates(result[0], result[1])

    def __repr__(self):
        return f'{self.latitude},{self.longitude}'


class Point:
    def __init__(self, address: GeodesicCoordinates,
                 tags: set[str] = None):
        self.coordinates = address
        self.tags = tags

    def get_tags(self) -> set[str]:
        return self.tags

    def __repr__(self):
        return f'{self.coordinates}'


class BDRequests:
    bd = None
    approximation_delta = 0.00001

    @staticmethod
    def get_geographic_coordinates(address: str) -> GeodesicCoordinates:
        parser = APIYandex.YandexApiGeocoderParser()
        response = parser.get_cords(address)
        return GeodesicCoordinates(response[1], response[0])

    @staticmethod
    def get_points(start_point: GeodesicCoordinates, length: float, tags) \
            -> set[Point]:
        length = math.sqrt(2) * length
        bottom_left = GeodesicCoordinates(start_point.latitude,
                                          start_point.longitude)
        top_right = GeodesicCoordinates(start_point.latitude,
                                        start_point.longitude)
        while True:
            bottom_left.latitude -= BDRequests.approximation_delta
            bottom_left.longitude -= BDRequests.approximation_delta
            if bottom_left.convert_to_plane(
                    start_point).get_length() >= length:
                break
        while True:
            top_right.latitude += BDRequests.approximation_delta
            top_right.longitude += BDRequests.approximation_delta
            if top_right.convert_to_plane(start_point).get_length() >= length:
                break
        db = Address.DatabaseConnector()
        db.connect_to_db()
        response = db.get_answer(bottom_left.longitude, top_right.longitude,
                                 bottom_left.latitude, top_right.latitude,
                                 tags)
        points = set()
        db.close_data_base()
        for point in response:
            address = GeodesicCoordinates(point.lat, point.lon)
            points.add(Point(address, point.amenity))
        return points


class PathFinder:
    meters_per_hour = 3000

    def __init__(self, address: str, desired_time: float,
                 tags) -> None:
        start_loc = BDRequests.get_geographic_coordinates(address)
        self.start_point = Point(start_loc)
        self.current_point = self.start_point
        self.desired_length = desired_time * PathFinder.meters_per_hour
        self.points = BDRequests.get_points(start_loc, self.desired_length,
                                            tags)
        self.points.add(self.start_point)
        self.plane_points = dict[Point, PlaneCoordinates]()
        for point in self.points:
            self.plane_points[point] = point.coordinates.convert_to_plane(
                self.current_point.coordinates)

    def find_path(self) -> list[Point]:
        return self.the_dumbest_greedy_algorithm()

    def the_dumbest_greedy_algorithm(self) -> list[Point]:
        path = []
        unused = set(self.points)
        current_point = self.start_point
        remaining_length = self.desired_length
        plane_start_point = self.plane_points[self.start_point]
        while True:
            closest_point = min(unused, key=lambda p: self.plane_points[
                p].get_distance_to(plane_current_point))
            plane_closest_point = self.plane_points[closest_point]
            plane_current_point = self.plane_points[current_point]
            remaining_length -= plane_current_point.get_distance_to(
                plane_closest_point)
            if plane_closest_point.get_distance_to(
                    plane_start_point) > remaining_length:
                break
            path.append(closest_point)
            current_point = closest_point
            unused.remove(closest_point)
        path.append(self.start_point)
        return path


if __name__ == '__main__':
    pf = PathFinder('Фонвизина 8', 1, ['art_object'])
    test_path = pf.the_dumbest_greedy_algorithm()

    print(test_path)
