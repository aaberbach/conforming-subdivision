import math

class Point:
    def __init__(self, x: int, y: int, mod_func = lambda x,y: (x,y)) -> None:
        self._x = x
        self._y = y
        self._mod_x , self._mod_y = mod_func(x, y)
        self._shape = None

    def get_x(self) -> int:
        return self._x
    
    def get_y(self) -> int:
        return self._y
    
    def get_mod_x(self):
        return self._mod_x
    
    def get_mod_y(self):
        return self._mod_y
    
    def add_shape(self, shape):
        self._shape = shape

    def has_shape(self):
        return not (self._shape is None)
    
    def point_distance(self, p):
        return math.sqrt((p.get_x() - self._x)**2 + (p.get_y() - self._y)**2)

    def distance(self, x, y):
        return math.sqrt((x - self._x)**2 + (y - self._y)**2)
    
class Circle:
    def __init__(self, x, y, r, mod_func = lambda x,y: (x,y)):
        self._center = Point(x, y, mod_func)
        self._rightmost_point = Point(x + r, y, mod_func)
        self._leftmost_point = Point(x - r, y, mod_func)
        self._r = r
        self._shape = None#{"circle": None, "rightmost_point": None, "leftmost_point": None}

    def get_r(self):
        return self._r

    def get_center(self):
        return self._center
    
    def get_rightmost_point(self):
        return self._rightmost_point
    
    def get_leftmost_point(self):
        return self._leftmost_point
    
    def add_shape(self, shape):
        self._shape = shape

    def has_shape(self):
        return not (self._shape is None)#len(self._shape) != 0
    
    def get_shape(self):
        return self._shape

    # def add_shape(self, key, shape):
    #     self._shape[key] = shape
    
    # def has_shape(self, key):
    #     return not (self._shape[key] is None)
