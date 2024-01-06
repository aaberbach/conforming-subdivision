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
    def __init__(self, mod_func, inverse_mod_func, instruction_bar):
        self._circle_subdivision = CircleSubdivision()
        self._circle_drawer = CircleSubdivisionDrawer(self._circle_subdivision)

        self._instruction_bar = instruction_bar
        self._instruction_bar.set_line1('<font size="5">Click and drag to input circles. Circles cannot be too small or too close to eachother for visualization reasons.</font>')
        self._instruction_bar.set_line2('<font size="5" color="#AD4D02">red</font><font size="5"> = invalid</font><font size="5" color="#009E73">  green</font><font size="5"> = valid</font>')
        # self._point_subdivision = PointSubdivision()
        # self._point_drawer = PointSubdivisionDrawer(self._point_subdivision)

        self._mod_func = mod_func
        self._inverse_mod_func = inverse_mod_func

        self._temp_circle_batch = pyglet.graphics.Batch()
        print("Temp circle batch", self._temp_circle_batch)
        self._temp_circle = None
        self._temp_center = None

    def on_draw(self):
        self._temp_circle_batch.draw()
        self._circle_drawer.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the mouse is in any existing circles
        for c in self._circle_subdivision.get_circles():
            if c.get_center().distance(x, y, mod_func=self._mod_func) <= c.get_alg_r():
                return

        self._temp_center = Point.from_mod_func(x, y, self._mod_func)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._temp_center is None:
            return
        
        r = self._temp_center.distance(x, y)
        alg_r = self._temp_center.distance(x, y, mod_func=self._mod_func)

        if self._is_temp_circle_valid(alg_r):
            c = (0, 158, 115)
        else:
            c = (213, 94, 0)

        self._temp_circle = shapes.Arc(self._temp_center.get_x(), self._temp_center.get_y(),
                        r, color = c, batch=self._temp_circle_batch)

    def on_mouse_release(self, x, y, button, modifiers):
        if self._temp_center is None:
            return

        r = self._temp_center.distance(x, y)
        alg_r = self._temp_center.distance(x, y, mod_func=self._mod_func)

        # Only keep new circle if it is large enough and far enough from existing circles
        if self._is_temp_circle_valid(alg_r):
            self._circle_subdivision.add_circle(Circle(self._temp_center.get_x(), 
                            self._temp_center.get_y(), r, mod_func=self._mod_func))
        
        self._temp_center = None
        self._temp_circle = None
        
    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.ENTER:
            return self.next_manager()

    def next_manager(self):
        return PointSubdivisionManager(self._circle_subdivision, self._circle_drawer,
                    self._mod_func, self._inverse_mod_func, self._instruction_bar)

    def _is_temp_circle_valid(self, r):
        if r < 32:
            return False
        for c in self._circle_subdivision.get_circles():
            horizontal_distance = (abs(c.get_center().get_alg_x() - self._temp_center.get_alg_x())
                        - r - c.get_alg_r())
            vertical_distance = (abs(c.get_center().get_alg_y() - self._temp_center.get_alg_y()))
            
            if horizontal_distance < 64 and vertical_distance < 64:
                return False
            if c.get_center().point_distance(self._temp_center) <= c.get_alg_r() + r + 1:
                return False
            
        return True
    
class PointSubdivisionManager(Manager):
    def __init__(self, circle_subdivision, circle_drawer, mod_func, inverse_mod_func, instruction_bar):
        self._circle_subdivision = circle_subdivision
        self._circle_drawer = circle_drawer
        self._circle_drawer.set_all_circle_opacities(100)

        self._instruction_bar = instruction_bar

        self._done = False
        self._stage = -1

        self._mod_func = mod_func
        self._inverse_mod_func = inverse_mod_func

        points = []
        for c in self._circle_subdivision.get_circles():
            points.append(c.get_leftmost_point())
            points.append(c.get_rightmost_point())

        self._point_subdivision = PointSubdivision(points = points, mod_func=self._mod_func,
                                                   inverse_mod_func=self._inverse_mod_func)
        self._point_drawer = PointSubdivisionDrawer(self._point_subdivision)

        self._instruction_bar.set_line1('<font size="5">First, we build a conforming subdivision for the arc endpoints in white.</font>')
        self._instruction_bar.set_line2('<font size="4">We build the subdivision in stages of increasing size. Each stage has its own grid, only part of which is saved into the final subdivision.</font>')

    def on_draw(self):
        self._circle_drawer.draw()

        if self._done:
            self._point_drawer.draw(["drawn"])
        elif self._stage == -1:
            self._point_drawer.draw([])
        elif self._stage == 1:
            self._point_drawer.draw(["prev_Q"])
        elif self._stage == 2:
            self._point_drawer.draw(["prev_Q", "Q"])
        elif self._stage == 3:
            self._point_drawer.draw(["prev_Q", "Q", "newly_drawn"])
        else:
            self._point_drawer.draw()

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.ENTER:
            # If the base structure has not already been initialized
            if not self._point_subdivision.is_initialized():
                self._point_subdivision._initialize_subdivision(3)
                self._instruction_bar.set_line1('<font size="5">We start with this base at <b>Stage 3</b> and will increase the stage by 2 each time.</font>')
                self._instruction_bar.set_line2('<font size="5" color="#009E73">green</font><font size="5"> = current stage grid</font><font size="5" color="#0072B2">  blue</font><font size="5"> = previous stage grid</font><font size="5" color="#AD4D02">  red</font><font size="5"> = saved subdivision</font><font size="5" color="#E69F00">  orange</font><font size="5"> = newly saved subdivision</font>')

                # Means we are ready to move to the next stage
                self._stage = 4
            else:
                # Time to move on to the Circle Subdivision manager
                if self._done:
                    pass
                # #The subdivision is done being built
                # elif len(self._point_subdivision.get_Q()) == 1:
                #     self._done = True

                #     self._instruction_bar.set_line1('<font size="5">The point subdivision is done, we will now add in the circles!</font>')
                #     self._instruction_bar.set_line2("")
                # The normal progression
                else:
                    if self._stage == 1:
                        self._instruction_bar.set_line1(f'<font size="5"><b>Stage {self._point_subdivision.get_stage()}: </b> We now grow the grid for this stage.</font>')
                    elif self._stage == 2:
                        self._instruction_bar.set_line1(f'<font size="5"><b>Stage {self._point_subdivision.get_stage()}: </b> We now show the parts of this grid that are added to the subdivision.</font>')
                    elif self._stage == 3:
                        self._instruction_bar.set_line1(f'<font size="5"><b>Stage {self._point_subdivision.get_stage()}: </b> Finally, we show everything combined.</font>')
                    else:
                        #The subdivision is done being built
                        if len(self._point_subdivision.get_Q()) == 1:
                            self._done = True

                            self._instruction_bar.set_line1('<font size="5">The point subdivision is done, we will now add in the circles!</font>')
                            self._instruction_bar.set_line2("")
                        else:
                            self._point_subdivision._next_stage()
                            self._instruction_bar.set_line1(f'<font size="5"><b>Stage {self._point_subdivision.get_stage()}: </b> Here is the grid from the last stage.</font>')
                            self._stage = 0

                    self._stage += 1
            
            self._point_drawer.update_batches()