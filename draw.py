from subdivision import *

class PointSubdivisionDrawer:
    def __init__(self, subdivision: PointSubdivision) -> None:
        self._subdivision = subdivision
        self._point_batch = pyglet.graphics.Batch()
        self._points = []

        self.update_points()

    def update_points(self):
        if self._points != self._subdivision.get_points():
            self._points = self._subdivision.get_points().copy()
            for p in self._points:
                if not p.has_shape():
                    p.add_shape(shapes.Circle(p.get_x(), p.get_y(), 2, batch=self._point_batch))

    def draw(self):
        self.update_points()
        self._point_batch.draw()

class CircleSubdivisionDrawer:
    def __init__(self, subdivision: CircleSubdivision) -> None:
        self._subdivision = subdivision
        self._circle_batch = pyglet.graphics.Batch()
        self._circles = []

        self.update_circles()

    def update_circles(self):
        if self._circles != self._subdivision.get_circles():
            self._circles = self._subdivision.get_circles().copy()
            for c in self._circles:
                if not c.has_shape():
                    c.add_shape(shapes.Circle(c.get_center().get_x(), c.get_center().get_y(), c.get_r(), color = (0,0,255), batch=self._circle_batch))
                    #c.add_shape(shapes.Circle(c.get_center.get_x(), c.get_center.get_y(), c.get_r - 1, color = (100,100,100), batch=self._circle_batch))

    def draw(self):
        self.update_circles()
        self._circle_batch.draw()