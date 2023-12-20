import pyglet
from pyglet import shapes

class PointSubdivision:
    def __init__(self, points) -> None:
        self._points = points

    def __init__(self):
        self._points = []

    def get_points(self):
        return self._points

    def add_point(self, p):
        self._points.append(p)

    