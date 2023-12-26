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
                    p.add_shape(shapes.Circle(p.get_x(), p.get_y(), 3, batch=self._point_batch))

    def draw(self):
        self.update_points()
        self._point_batch.draw()

class CircleSubdivisionDrawer:
    def __init__(self, subdivision: CircleSubdivision) -> None:
        self._subdivision = subdivision
        self._circle_batch = pyglet.graphics.Batch()
        self._circles = []
        self._opacity = 255

        self.update_circles()

    def update_circles(self):
        if len(self._circles) != len(self._subdivision.get_circles()):
            self._circles = self._subdivision.get_circles().copy()
            for c in self._circles:
                if not c.has_shape():
                    c.add_shape(shapes.Arc(c.get_center().get_x(), c.get_center().get_y(), 
                        c.get_r(), color = (255,255,255), batch=self._circle_batch))
                    c.get_shape().opacity = self._opacity
    
    def set_all_circle_opacities(self, a):
        for c in self._circles:
            c.get_shape().opacity = a
        
        self._opacity = a

    def draw(self):
        self.update_circles()
        self._circle_batch.draw()


class InstructionBar:
    def __init__(self, window_w, window_h, bar_h) -> None:
        self._window_w = window_w
        self._window_h = window_h
        self._bar_h = bar_h
        self._background_batch = pyglet.graphics.Batch()
        self._foreground_batch = pyglet.graphics.Batch()

        self._background = shapes.Rectangle(0, 0, self._window_w, self._bar_h, 
                        color = (160,160,160),
                        batch=self._background_batch)
        
        self._shapes = [self._background]
    
    def draw(self):
        self._background_batch.draw()
        self._foreground_batch.draw()

    # def on_resize(self, width, height):
    #     shift = self._window_w
    #     for shape in self._shapes:
