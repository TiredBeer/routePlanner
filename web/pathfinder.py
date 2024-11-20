import math

from Address import DatabaseConnector
from APIYandex import YandexApiGeocoderParser

from PointObject.Point import Point
from PointObject.PlaneCoordinates import PlaneCoordinates
from PointObject.GeodesicCoordinates import GeodesicCoordinates


class BDRequests:
    bd = None

    @staticmethod
    def get_geographic_coordinates(address: str) -> GeodesicCoordinates:
        parser = YandexApiGeocoderParser()
        response = parser.get_cords(address)
        return GeodesicCoordinates(response[1], response[0])

    @staticmethod
    def get_points(start_point: GeodesicCoordinates, length: float, tags) \
            -> set[Point]:
        length = math.sqrt(2) * length
        delta = 0.000001
        bottom_left = GeodesicCoordinates(start_point.latitude,
                                          start_point.longitude)
        top_right = GeodesicCoordinates(start_point.latitude,
                                        start_point.longitude)
        while True:
            bottom_left.latitude -= delta
            bottom_left.longitude -= delta
            if bottom_left.convert_to_plane(
                    start_point).get_length() >= length:
                break
        while True:
            top_right.latitude += delta
            top_right.longitude += delta
            if top_right.convert_to_plane(start_point).get_length() >= length:
                break
        db = DatabaseConnector()
        db.connect_to_db()
        response = db.get_answer(bottom_left.longitude, top_right.longitude,
                                 bottom_left.latitude, top_right.latitude,
                                 tags)
        return set(response)


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
        self.update_distances()

    def find_path(self) -> list[Point]:
        # paths = self.find_all_paths()
        # sorted_paths = sorted(paths, key=lambda p: len(p), reverse=True)
        # return sorted_paths[0]
        return self.the_dumbest_greedy_algorithm()

    def the_dumbest_greedy_algorithm(self):
        paths = list[list[Point]]()
        path = []
        unused = set(self.points)
        remaining_length = self.desired_length
        current_point = self.start_point
        length = self.desired_length
        plane_start_point = self.plane_points[self.start_point]
        while True:
            plane_point = self.plane_points[current_point]
            closest_point = min(unused, key=lambda p: self.plane_points[
                p].get_distance_to(plane_point))
            plane_closest_point = self.plane_points[closest_point]
            length -= self.plane_points[current_point].get_distance_to(
                plane_closest_point)
            if plane_closest_point.get_distance_to(plane_start_point) > length:
                break
            path.append(closest_point)
            current_point = closest_point
            unused.remove(closest_point)
        path.append(self.start_point)
        return path

    def find_all_paths(self) -> list[list[Point]]:
        paths = list[list[Point]]()
        path = []
        unused = set(self.points)
        remaining_length = self.desired_length
        stack = [(self.current_point, 0, remaining_length)]
        previous_point = self.start_point
        while stack:
            popped = stack.pop()
            self.current_point = popped[0]
            depth = popped[1]
            remaining_length = popped[2]
            for point in path[depth: len(path)]:
                unused.add(point)
            path = path[0:depth]
            if path:
                previous_point = path[-1]
            path.append(self.current_point)
            unused.remove(self.current_point)
            self.update_distances()
            remaining_length -= self.plane_points[
                previous_point].get_distance_to(
                self.plane_points[self.current_point])
            if (self.plane_points[self.current_point].
                    get_distance_to(self.plane_points[self.start_point])
                    > remaining_length):
                unused.add(path.pop())
                path.append(self.start_point)
                paths.append(list(path))
                path.pop()
                continue
            if not unused:
                path.append(self.start_point)
                paths.append(list(path))
                path.pop()
                continue
            for next_loc in unused:
                stack.append((next_loc, len(path), remaining_length))
        self.current_point = self.start_point
        return paths

    def update_distances(self):
        for point in self.points:
            self.plane_points[point] = point.coordinates.convert_to_plane(
                self.current_point.coordinates)


#
#
if __name__ == '__main__':
    pf = PathFinder('Фонвизина 8', 1, ['art_object'])
    #     points = {Point(GeodesicCoordinates(0.01, -0.01)),
    #               Point(GeodesicCoordinates(0.01, 0.01)),
    #               Point(GeodesicCoordinates(0.02, 0.02)),
    #               Point(GeodesicCoordinates(0.03, 0.00))}
    #     pathfinder = PathFinder(GeodesicCoordinates(0, 0), points, 7)
    # paaths = pf.find_all_paths()
    paath = pf.the_dumbest_greedy_algorithm()

    print(paath)
