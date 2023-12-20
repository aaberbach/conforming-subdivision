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
                    p.add_shape(shapes.Circle(p.x(), p.y(), 2, batch=self._point_batch))

    def draw(self):
        self.update_points()
        self._point_batch.draw()