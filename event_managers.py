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

    def next_manager(self):
        pass

class CircleInputManager(Manager):
    def __init__(self):
        self._circle_subdivision = CircleSubdivision()
        self._circle_drawer = CircleSubdivisionDrawer(self._circle_subdivision)
        # self._point_subdivision = PointSubdivision()
        # self._point_drawer = PointSubdivisionDrawer(self._point_subdivision)

        self._temp_circle_batch = pyglet.graphics.Batch()
        self._temp_circle = None
        self._temp_center = None

    def on_draw(self):
        self._temp_circle_batch.draw()
        self._circle_drawer.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the mouse is in any existing circles
        for c in self._circle_subdivision.get_circles():
            if c.get_center().distance(x, y) <= c.get_r():
                return

        self._temp_center = Point(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._temp_center is None:
            return
        
        r = self._temp_center.distance(x, y)

        if self._is_temp_circle_valid(r):
            c = (0, 158, 115)
        else:
            c = (213, 94, 0)

        self._temp_circle = shapes.Arc(self._temp_center.get_x(), self._temp_center.get_y(),
                        r, color = c, batch=self._temp_circle_batch)

    def on_mouse_release(self, x, y, button, modifiers):
        if self._temp_center is None:
            return

        r = self._temp_center.distance(x, y)

        # Only keep new circle if it is far enough from existing circles
        if self._is_temp_circle_valid(r):
            self._circle_subdivision.add_circle(Circle(self._temp_center.get_x(), 
                            self._temp_center.get_y(), r))
        
        self._temp_center = None
        self._temp_circle = None

    def next_manager(self):
        return PointSubdivisionManager(self._circle_subdivision, self._circle_drawer)

    def _is_temp_circle_valid(self, r):
        for c in self._circle_subdivision.get_circles():
            if c.get_center().point_distance(self._temp_center) <= c.get_r() + r + 20:
                return False
            
        return True
    
class PointSubdivisionManager(Manager):
    def __init__(self, circle_subdivision, circle_drawer):
        self._circle_subdivision = circle_subdivision
        self._circle_drawer = circle_drawer
        self._circle_drawer.set_all_circle_opacities(100)

        points = []
        for c in self._circle_subdivision.get_circles():
            points.append(c.get_leftmost_point())
            points.append(c.get_rightmost_point())

        self._point_subdivision = PointSubdivision(points = points)
        self._point_drawer = PointSubdivisionDrawer(self._point_subdivision)

    def on_draw(self):
        self._circle_drawer.draw()
        self._point_drawer.draw()
