class Point:
    def __init__(self, x: int, y: int, mod_func = lambda x,y: (x,y)) -> None:
        self._x = x
        self._y = y
        self._mod_x , self._mod_y = mod_func(x, y)
        self._shape = None

    def x(self) -> int:
        return self._x
    
    def y(self) -> int:
        return self._y
    
    def mod_x(self):
        return self._mod_x
    
    def mod_y(self):
        return self._mod_y
    
    def add_shape(self, shape):
        self._shape = shape

    def has_shape(self):
        return not (self._shape is None)
    
