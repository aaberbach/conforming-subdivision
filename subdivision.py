import pyglet
from pyglet import shapes
import networkx as nx
from objects import *

class PointSubdivision:
    def __init__(self, points = [], 
            mod_func = lambda x,y: (x,y), inverse_mod_func = lambda x,y: (x,y)) -> None:
        self._points = points
        self._inverse_mod_func = inverse_mod_func
        self._mod_func = mod_func

    def get_points(self):
        return self._points

    def add_point(self, p):
        self._points.append(p)

    def _initialize_subdivision(self, i):
        self._Q = []
        self._i = i
        side_length = 2**i

        for p in self._points:
            alg_x = ((p.get_alg_x() // side_length) * side_length) 
            alg_y = ((p.get_alg_y() // side_length) * side_length) - 3*side_length

            bottom_left_corner = Point.from_inverse_mod_func(alg_x, alg_y, self._inverse_mod_func)
            self._Q.append(IQuad(bottom_left_corner, i, self._inverse_mod_func))

class CircleSubdivision:
    def __init__(self, circles):
        self._circles = circles

    def __init__(self):
        self._circles = []

    def get_circles(self):
        return self._circles

    def add_circle(self, c):
        self._circles.append(c)

    