import math
from typing import Any

class Point:
    def __init__(self, x: int, y: int, alg_x=-1, alg_y=-1) -> None:
        self._x = x
        self._y = y

        self._alg_x = alg_x
        self._alg_y = alg_y
        
        if alg_x < 0:
            self._alg_x = self._x
        if alg_y < 0:
            self._alg_y = self._y

        self._shape = None

    def from_inverse_mod_func(alg_x, alg_y, inverse_mod_func):
        x, y = inverse_mod_func(alg_x, alg_y)

        return Point(x, y, alg_x, alg_y)

    def from_mod_func(x, y, mod_func):
        alg_x, alg_y = mod_func(x,y)

        return Point(x, y, alg_x, alg_y)

    def get_x(self) -> int:
        return self._x
    
    def get_y(self) -> int:
        return self._y
    
    def get_alg_x(self):
        return self._alg_x
    
    def get_alg_y(self):
        return self._alg_y
    
    def add_shape(self, shape):
        self._shape = shape

    def has_shape(self):
        return not (self._shape is None)
    
    def point_distance(self, p, mod=False):
        if mod:
            return self.distance(p.get_alg_x(), p.get_alg_y())
        else:
            return self.distance(p.get_x(), p.get_y())
        #return math.sqrt((p.get_x() - self._x)**2 + (p.get_y() - self._y)**2)

    def distance(self, x, y, mod_func=None):
        if not (mod_func is None):
            alg_x, alg_y = mod_func(x, y) 
            return math.sqrt((alg_x - self._alg_x)**2 + (alg_y - self._alg_y)**2)
        else:
            return math.sqrt((x - self._x)**2 + (y - self._y)**2)
    
class Circle:
    def __init__(self, x, y, r, mod_func = lambda x,y: (x,y)):
        self._center = Point.from_mod_func(x, y, mod_func)
        self._rightmost_point = Point.from_mod_func(x + r, y, mod_func)
        self._leftmost_point = Point.from_mod_func(x - r, y, mod_func)
        self._mod_func = mod_func
        self._r = r
        self._shape = None

    def get_r(self):
        return self._r
    
    def get_alg_r(self):
        return self._center.point_distance(self._rightmost_point, mod=True)

    def get_center(self):
        return self._center
    
    def get_rightmost_point(self):
        return self._rightmost_point
    
    def get_leftmost_point(self):
        return self._leftmost_point
    
    def add_shape(self, shape):
        self._shape = shape

    def has_shape(self):
        return not (self._shape is None)
    
    def get_shape(self):
        return self._shape
    
class Edge:
    def __init__(self, p1: Point, p2: Point) -> None:
        self._p1 = p1
        self._p2 = p2

        self._shape = None

    def get_p1(self):
        return self._p1
    
    def get_p2(self):
        return self._p2
    
    def get_shape(self):
        return self._shape

    def add_shape(self, shape):
        self._shape = shape

    def has_shape(self):
        return not (self._shape is None)
    
class IBox:
    def __init__(self, bottom_left_corner, i, inverse_mod_func=lambda x,y: (x,y)):
        self._i = i
        self._side_length = 2**i

        self._inverse_mod_func = inverse_mod_func

        self._center_x = bottom_left_corner.get_alg_x() + 0.5*self._side_length
        self._center_y = bottom_left_corner.get_alg_x() + 0.5*self._side_length

        self._fill_vertices_list(bottom_left_corner)
        self._fill_edges_list()

    def _fill_vertices_list(self, bottom_left_corner):
        self._vertices = [[bottom_left_corner, None], [None, None]]

        #adds the other three vertices
        for x_flag in [0,1]:
            for y_flag in [0,1]:
                if x_flag == 0 and y_flag == 0:
                    continue

                alg_x = bottom_left_corner.get_alg_x() + x_flag*self._side_length
                alg_y = bottom_left_corner.get_alg_y() + y_flag*self._side_length
                x, y = self._inverse_mod_func(alg_x, alg_y)
                
                self._vertices[x_flag][y_flag] = Point(x, y, alg_x, alg_y)

    def _fill_edges_list(self):
        self._edges = []

        self._edges.append(Edge(self._vertices[0][0], self._vertices[0][1]))
        self._edges.append(Edge(self._vertices[0][0], self._vertices[1][0]))
        self._edges.append(Edge(self._vertices[1][1], self._vertices[0][1]))
        self._edges.append(Edge(self._vertices[1][1], self._vertices[1][0]))

    def get_vertices(self):
        return self._vertices
    
    def get_edges(self):
        return self._edges
    
class IQuad:
    def __init__(self, bottom_left_corner, i, inverse_mod_func=lambda x,y: (x,y)):
        self._i = i

        self._inverse_mod_func = inverse_mod_func

        self._bottom_left_corner = bottom_left_corner

        side_length = 2**i
        center_x = bottom_left_corner.get_alg_x() + 2*side_length
        center_y = bottom_left_corner.get_alg_x() + 2*side_length
        self._center = Point.from_inverse_mod_func(center_x, center_y, self._inverse_mod_func)

        self._fill_box_list(bottom_left_corner, i, inverse_mod_func)

        self._grown = None

    def from_core_bottom_left(core_bottom_left_corner, i, inverse_mod_func=lambda x,y: (x,y)):
        side_length = 2**i

        x_alg = core_bottom_left_corner.get_alg_x() - side_length
        y_alg = core_bottom_left_corner.get_alg_y() - side_length
        bottom_left_corner = Point.from_inverse_mod_func(x_alg, y_alg, inverse_mod_func)

        return IQuad(bottom_left_corner, i, inverse_mod_func)

    def _fill_box_list(self, bottom_left_corner, i, inverse_mod_func):
        self._boxes = [[None, None, None, None] for i in range(0,4)]
        side_length = 2**i

        for x_steps in [0, 1, 2, 3]:
            for y_steps in [0, 1, 2, 3]:
                alg_x = bottom_left_corner.get_alg_x() + x_steps*side_length
                alg_y = bottom_left_corner.get_alg_y() + y_steps*side_length
                x, y = self._inverse_mod_func(alg_x, alg_y)
                
                self._boxes[x_steps][y_steps] = IBox(Point(x, y, alg_x, alg_y), i, inverse_mod_func)

    def get_boxes(self):
        return self._boxes
    
    def get_box(self, i, j):
        return self._boxes[i][j]
    
    def get_bottom_left_corner(self):
        return self._bottom_left_corner
    
    def get_center(self):
        return self._center
    
    def get_i(self):
        return self._i
    
    def grow(self):
        return self._grown
    
    def set_grown(self, quad):
        self._grown = quad
    
    def does_interior_overlap(self, q) -> bool:
        x_dist = abs(self._center.get_alg_x() - q.get_center().get_alg_x())
        y_dist = abs(self._center.get_alg_y() - q.get_center().get_alg_y())
        return (x_dist < 4*self._side_length) and (y_dist < 4*self._side_length)
        
    def does_closure_overlap(self, q) -> bool:
        x_dist = abs(self._center.get_alg_x() - q.get_center().get_alg_x())
        y_dist = abs(self._center.get_alg_y() - q.get_center().get_alg_y())
        return (x_dist <= 4*self._side_length) and (y_dist <= 4*self._side_length)