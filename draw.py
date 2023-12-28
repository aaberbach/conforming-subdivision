from subdivision import *

def add_point_to_batch(point, batch, radius=2, color=(255, 255, 255)):
    shape = shapes.Circle(point.get_x(), point.get_y(), radius, color=color, batch=batch)
    point.add_shape(shape)

def add_edge_to_batch(edge, batch, thickness=2, color=(255,255,255)):
    shape = shapes.Line(edge.get_p1().get_x(), edge.get_p1().get_y(),
                        edge.get_p2().get_x(), edge.get_p2().get_y(),
                        width=thickness, color=color, batch=batch)
    edge.add_shape(shape)

def add_ibox_to_batch(ibox, batch, vertex_radius=2, edge_thickness=1, color=(0,114,178)):
    for row in ibox.get_vertices():
        for p in row:
            add_point_to_batch(p, batch, radius=vertex_radius, color=color)

    for e in ibox.get_edges():
        add_edge_to_batch(e, batch, edge_thickness, color)

def add_iquad_to_batch(iquad, batch, vertex_radius=2, edge_thickness=1, color=(0,114,178)):
    box_matrix = iquad.get_boxes()

    for row in box_matrix:
        for ibox in row:
            add_ibox_to_batch(ibox, batch, vertex_radius, edge_thickness, color)


class PointSubdivisionDrawer:
    def __init__(self, subdivision: PointSubdivision) -> None:
        self._subdivision = subdivision
        self._point_batch = pyglet.graphics.Batch()
        self._points = []

        self._subdivision_batch = pyglet.graphics.Batch()

        self.update_points()

    def update_points(self):
        #if len(self._points) != len(self._subdivision.get_points()):
            self._points = self._subdivision.get_points()#.copy()
            for p in self._points:
                if not p.has_shape():
                    add_point_to_batch(p, self._point_batch, radius=2, color=(255,255,255))
                    #p.add_shape(shapes.Circle(p.get_x(), p.get_y(), 3, batch=self._point_batch))

    def update_subdivision(self):
        for iquad in self._subdivision.get_Q():
            add_iquad_to_batch(iquad, self._subdivision_batch)

    def draw(self):
        self.update_points()
        self._point_batch.draw()
        #self._subdivision_batch.draw()

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
