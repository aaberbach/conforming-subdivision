import pyglet
from pyglet import shapes

class PointSubdivision:
    def __init__(self, points = []) -> None:
        self._points = points

    def get_points(self):
        return self._points

    def add_point(self, p):
        self._points.append(p)

class CircleSubdivision:
    def __init__(self, circles):
        self._circles = circles

    def __init__(self):
        self._circles = []

    def get_circles(self):
        return self._circles

    def add_circle(self, c):
        self._circles.append(c)

    