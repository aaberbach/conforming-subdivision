from objects import *
from draw import *
from subdivision import *

class Manager:
    def on_draw(self):
        pass

    def on_key_press(self, symbol, modifier):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

class CircleInputManager(Manager):
    def __init__(self):
        self._circle_subdivision = CircleSubdivision()
        self._circle_drawer = CircleSubdivisionDrawer(self._circle_subdivision)
        self._point_subdivision = PointSubdivision()
        self._point_drawer = PointSubdivisionDrawer(self._point_subdivision)

        self._temp_circle_batch = pyglet.graphics.Batch()
        self._temp_inner_circle = None
        self._temp_outer_circle = None
        self._temp_center = None

    def on_draw(self):
        self._temp_circle_batch.draw()
        self._circle_drawer.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for c in self._circle_subdivision.get_circles():
            if c.get_center().distance(x, y) <= c.get_r():
                return

        self._temp_center = Point(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._temp_center is None:
            return

        r = self._temp_center.distance(x, y)
        self._temp_outer_circle = shapes.Circle(self._temp_center.get_x(), self._temp_center.get_y(),
                        r, color = (255,255,255), batch=self._temp_circle_batch)
        self._temp_inner_circle = shapes.Circle(self._temp_center.get_x(), self._temp_center.get_y(),
                        r, color = (20,20,20), batch=self._temp_circle_batch)

    def on_mouse_release(self, x, y, button, modifiers):
        if self._temp_center is None:
            return

        r = self._temp_center.distance(x, y)

        self._circle_subdivision.add_circle(Circle(self._temp_center.get_x(), 
                        self._temp_center.get_y(), r))
        
        self._temp_center = None
        self._temp_inner_circle = None
        self._temp_outer_circle = None