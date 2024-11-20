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


class Point:
    def __init__(self, address: GeodesicCoordinates,
                 tags: set[str] = None):
        self.coordinates = address
        self.tags = tags

    def get_tags(self) -> set[str]:
        return self.tags


class BDRequests:
    bd = None

    @staticmethod
    def get_geographic_coordinates(address: str) -> GeodesicCoordinates:
        parser = APIYandex.YandexApiGeocoderParser()
        response = parser.get_cords(address)
        return GeodesicCoordinates(response[0], response[1])

    @staticmethod
    def get_points(start_point: GeodesicCoordinates, length: float) \
            -> set[Point]:
        length = math.sqrt(2) * length
        delta = 0.0001
        bottom_left = GeodesicCoordinates(start_point.longitude,
                                          start_point.latitude)
        top_right = GeodesicCoordinates(start_point.longitude,
                                        start_point.latitude)
        while True:
            bottom_left.latitude -= delta
            bottom_left.longitude -= delta
            if bottom_left.convert_to_plane(
                    start_point).get_length() >= length:
                break
        while True:
            top_right.latitude -= delta
            top_right.longitude -= delta
            if top_right.convert_to_plane(start_point).get_length() >= length:
                break
        db = Address.DatabaseConnector()
        response = db.get_answer(bottom_left.longitude, top_right.longitude,
                                                        bottom_left.latitude, top_right.latitude)
        points = set()
        for point in response:
            address = GeodesicCoordinates(point.lat, point.lon)
            points.add(Point(address, point.tags))
        return points


class PathFinder:
    meters_per_hour = 3000

    def __init__(self, address: str, points: set[Point],
                 desired_time: float) -> None:
        start_loc = BDRequests.get_geographic_coordinates(address)
        self.start_point = Point(start_loc)
        self.current_point = self.start_point
        self.desired_length = desired_time * PathFinder.meters_per_hour
        self.points = points
        self.points.add(self.start_point)
        self.plane_points = dict[Point, PlaneCoordinates]()
        self.update_distances()

    def find_path(self) -> list[Point]:
        paths = self.find_all_paths()
        sorted_paths = sorted(paths, key=lambda p: len(p), reverse=True)
        return sorted_paths[0]

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


if __name__ == '__main__':
    points = {Point(GeodesicCoordinates(0.01, -0.01)),
              Point(GeodesicCoordinates(0.01, 0.01)),
              Point(GeodesicCoordinates(0.02, 0.02)),
              Point(GeodesicCoordinates(0.03, 0.00))}
    pathfinder = PathFinder(GeodesicCoordinates(0, 0), points, 7)
    paaths = pathfinder.find_all_paths()
    paath = pathfinder.find_path()
    print(paath)
