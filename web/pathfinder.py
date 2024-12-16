import math
# hello
from web.Address import DatabaseConnector
from web.APIYandex import YandexApiGeocoderParser

from PointObject.Point import Point
from PointObject.PlaneCoordinates import PlaneCoordinates
from PointObject.GeodesicCoordinates import GeodesicCoordinates


class BDRequests:
    bd = None
    approximation_delta = 0.00001
    length_approximation_ratio = math.sqrt(2) * 1.2

    @staticmethod
    def get_geographic_coordinates(address: str) -> GeodesicCoordinates:
        parser = YandexApiGeocoderParser()
        response = parser.get_cords(address)
        return GeodesicCoordinates(response[1], response[0])

    @staticmethod
    def get_points(start_point: GeodesicCoordinates, length: float, tags) \
            -> set[Point]:
        length = math.sqrt(2) * length
        bottom_left, top_right = BDRequests.get_rectangle_approximation_of_area(
            start_point, length)
        db = DatabaseConnector()
        db.connect_to_db()
        response = db.get_answer(bottom_left.longitude, top_right.longitude,
                                 bottom_left.latitude, top_right.latitude,
                                 tags)
        return set(response)

    @staticmethod
    def get_rectangle_approximation_of_area(start_point: GeodesicCoordinates,
                                            length: float) \
            -> tuple[GeodesicCoordinates, GeodesicCoordinates]:
        length = length * BDRequests.length_approximation_ratio
        bottom_left = GeodesicCoordinates(start_point.latitude,
                                          start_point.longitude)
        top_right = GeodesicCoordinates(start_point.latitude,
                                        start_point.longitude)
        while True:
            bottom_left.latitude -= BDRequests.approximation_delta
            bottom_left.longitude -= BDRequests.approximation_delta * 2
            if bottom_left.convert_to_plane(
                    start_point).get_length() >= length:
                break
        while True:
            top_right.latitude += BDRequests.approximation_delta
            top_right.longitude += BDRequests.approximation_delta * 2
            if top_right.convert_to_plane(start_point).get_length() >= length:
                break
        return bottom_left, top_right


class PathFinder:
    meters_per_hour = 3000

    def __init__(self, address: str, desired_time: float,
                 tags, points: set[Point] = None,
                 start_loc: GeodesicCoordinates = None) -> None:
        if start_loc is None:
            start_loc = BDRequests.get_geographic_coordinates(address)
        self.start_point = Point(start_loc)
        self.current_point = self.start_point
        self.desired_length = desired_time * PathFinder.meters_per_hour
        if points is None:
            self.points = BDRequests.get_points(start_loc, self.desired_length,
                                                tags)
        else:
            self.points = points
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
            plane_current_point = self.plane_points[current_point]
            if not unused:
                break
            closest_point = min(unused, key=lambda p: self.plane_points[
                p].get_distance_to(plane_current_point))
            plane_closest_point = self.plane_points[closest_point]
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
    pf = PathFinder('Фонвизина 8', 1, ['bar'])
    test_path = pf.the_dumbest_greedy_algorithm()

    print(test_path)
