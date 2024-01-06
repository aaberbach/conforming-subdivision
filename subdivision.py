import pyglet
from pyglet import shapes
import networkx as nx
from objects import *

# Given a point, return the bottom left corner
# of the ibox it is in
def ibox_of_point(x, y, i):
    side_length = 2**i

    res_x = (x // side_length) * side_length
    res_y = (y // side_length) * side_length

    return res_x, res_y

def get_quad_core_coordinates(q):
    coords = []

    for i in [1, 2]:
        for j in [1, 2]:
            p = q.get_box(i, j).get_bottom_left_corner()
            coords.append((p.get_alg_x(), p.get_alg_y()))

    return coords

def get_quad_coordinates(q):
    coords = []

    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            p = q.get_box(i, j).get_bottom_left_corner()
            coords.append((p.get_alg_x(), p.get_alg_y()))

    return coords

def decompose_ibox_coord(coord, i):
    coords = []
    x, y = coord
    side_length = 2**(i-2)

    for x_flag in [0, 1, 2, 3]:
        for y_flag in [0, 1, 2, 3]:
            coords.append((x + x_flag*side_length, y + y_flag*side_length))

    return coords

class PointSubdivision:
    def __init__(self, points = [], 
            mod_func = lambda x,y: (x,y), inverse_mod_func = lambda x,y: (x,y)) -> None:
        self._points = points
        self._inverse_mod_func = inverse_mod_func
        self._mod_func = mod_func
        self._initialized = False


    def get_points(self):
        return self._points

    def add_point(self, p):
        self._points.append(p)

    def get_stage(self):
        return self._i

    def get_Q(self):
        return self._Q
    
    def get_prev_Q(self):
        return self._previous_Q

    def get_drawn_subdiv(self):
        return self._drawn
    
    def get_newly_drawn_subdiv(self):
        return self._newly_drawn
    
    def is_initialized(self):
        return self._initialized

    def _initialize_subdivision(self, i):
        self._initialized = True
        self._previous_Q = []
        self._Q = []
        self._drawn = Graph(self._inverse_mod_func)
        self._newly_drawn = Graph(self._inverse_mod_func)
        self._i = i
        side_length = 2**i

        for p in self._points:
            box_alg_x, box_alg_y = ibox_of_point(p.get_alg_x(), p.get_alg_y(), self._i)

            quad_alg_x = box_alg_x - side_length
            quad_alg_y = box_alg_y - 2*side_length

            self._drawn.add_square(box_alg_x, box_alg_y, side_length)
            self._newly_drawn.add_square(box_alg_x, box_alg_y, side_length)


            bottom_left_corner = Point.from_inverse_mod_func(quad_alg_x, quad_alg_y, self._inverse_mod_func)
            self._Q.append([IQuad(bottom_left_corner, i, self._inverse_mod_func)])

    def _reset_previous_Q(self):
        for comp in self._previous_Q:
            for quad in comp:
                quad.delete_shapes()
        self._previous_Q = self._Q.copy()

    def _next_stage(self):
        self._reset_previous_Q()
        self._i += 2
        self._Q = []
        self._newly_drawn = Graph(self._inverse_mod_func)

        self._build_new_Q()
        self._draw_new_subdivision()

    def _build_new_Q(self):
        for equiv_class in self._previous_Q:
            self._Q += self._grow(equiv_class)

        G = nx.Graph()
        G.add_nodes_from([i for i in range(len(self._Q))])

        for i, q1 in enumerate(self._Q):
            for j, q2 in enumerate(self._Q):
                if i != j and q1.does_interior_overlap(q2):
                    G.add_edge(i, j)

        conn_comps = nx.connected_components(G)

        self._Q = [[self._Q[i] for i in comp] for comp in conn_comps]

    def _draw_new_subdivision(self):
        self._process_simple_components()
        self._process_complex_components()
    
    def _process_simple_components(self):
        for component in self._previous_Q:
            if len(component) == 1:
                q = component[0]
                # if q is a simple component
                if len(q.get_children()) <= 1:
                    q_hat = q.grow()
                    # if q_hat is not a simple component
                    if len(q_hat.get_children()) != 1 or ([q_hat] not in self._Q):
                        p = q.get_bottom_left_corner()
                        x = p.get_alg_x()
                        y = p.get_alg_y()
                        side_length = 2**self._i

                        self._drawn.add_square(x, y, side_length, [True,True,True,True])
                        self._newly_drawn.add_square(x, y, side_length, [True,True,True,True])

    def _process_complex_components(self):
        for S in self._Q:
            children = self._children_of_component(S)

            # if S is a complex component
            if len(children) > 1:
                R_2 = set()
                R_1_split = set()
                R_1_whole = set()
                S_coords = set()

                for q in children:
                    g = q.grow()

                    R_2.update(get_quad_coordinates(q))

                    core_coords = get_quad_core_coordinates(g)
                    R_1_whole.update(core_coords)
                    for coord in core_coords:
                        R_1_split.update(decompose_ibox_coord(coord, self._i))

                    S_coords.update(get_quad_coordinates(g))

                for coord in R_1_split.difference(R_2):
                    self._drawn.add_square(coord[0], coord[1], 2**(self._i - 2))
                    self._newly_drawn.add_square(coord[0], coord[1], 2**(self._i - 2))
                
                for coord in S_coords.difference(R_1_whole):
                    self._drawn.add_square(coord[0], coord[1], 2**(self._i))
                    self._newly_drawn.add_square(coord[0], coord[1], 2**(self._i))
    
    def _children_of_component(self, S):
        children = []

        for quad in S:
            for child in quad.get_children():
                if child not in children:
                    children.append(child)

        return children

    # Follows growth algorithm in section 6.4
    def _grow(self, S):
        results = []
        G = nx.Graph()

        G.add_nodes_from([i for i in range(len(S))])

        for i, q1 in enumerate(S):
            for j, q2 in enumerate(S):
                if i > j and q1.does_closure_overlap(q2):
                    q1_bottom_left = q1.get_bottom_left_corner()
                    q2_bottom_left = q2.get_bottom_left_corner()

                    min_x = min(q1_bottom_left.get_alg_x(), q2_bottom_left.get_alg_x())
                    min_y = min(q1_bottom_left.get_alg_y(), q2_bottom_left.get_alg_y())

                    core_bottom_left_x, core_bottom_left_y = ibox_of_point(min_x, min_y, self._i)

                    containable_in_core = True

                    for q in [q1, q2]:
                        y_diff = q.get_boxes()[0][3].get_vertices()[0][1].get_alg_y() - core_bottom_left_y
                        x_diff = q.get_boxes()[3][0].get_vertices()[1][0].get_alg_x() - core_bottom_left_x

                        # Checks if the quad surpases the core boundary
                        if y_diff > 2*(2**self._i) or x_diff > 2*(2**self._i):
                            containable_in_core = False

                    if containable_in_core:
                        G.add_edge(i, j)

        matching = nx.maximal_matching(G)

        covered_quads = []
        for e in matching:
            covered_quads.append(e[0])
            covered_quads.append(e[1])

            q1 = S[e[0]]
            q2 = S[e[1]]
            q1_bottom_left = q1.get_bottom_left_corner()
            q2_bottom_left = q2.get_bottom_left_corner()

            min_x = min(q1_bottom_left.get_alg_x(), q2_bottom_left.get_alg_x())
            min_y = min(q1_bottom_left.get_alg_y(), q2_bottom_left.get_alg_y())

            core_bottom_left_x, core_bottom_left_y = ibox_of_point(min_x, min_y, self._i)

            # core_bottom_left_x = min(q1_bottom_left.get_alg_x(), q2_bottom_left.get_alg_x())
            # core_bottom_left_y = min(q1_bottom_left.get_alg_y(), q2_bottom_left.get_alg_y())

            #print(self._i, core_bottom_left_x, core_bottom_left_y)

            core_bottom_left = Point.from_inverse_mod_func(core_bottom_left_x, 
                                    core_bottom_left_y, self._inverse_mod_func)
            
            parent_quad = IQuad.from_core_bottom_left(core_bottom_left, self._i, self._inverse_mod_func)
            results.append(parent_quad)

            parent_quad.add_child(q1)
            parent_quad.add_child(q2)

            q1.set_grown(parent_quad)
            q2.set_grown(parent_quad)

        for i, quad in enumerate(S):
            if i not in covered_quads:
                min_p = quad.get_bottom_left_corner()
                min_x = min_p.get_alg_x()
                min_y = min_p.get_alg_y()

                alg_x, alg_y = ibox_of_point(min_x, min_y, i=self._i)

                parent_quad = IQuad.from_core_bottom_left(
                                    Point.from_inverse_mod_func(alg_x, alg_y, self._inverse_mod_func),
                                    self._i, self._inverse_mod_func)
                
                results.append(parent_quad)
                parent_quad.add_child(quad)
                quad.set_grown(parent_quad)

        return results

class CircleSubdivision:
    def __init__(self, circles):
        self._circles = circles

    def __init__(self):
        self._circles = []

    def get_circles(self):
        return self._circles

    def add_circle(self, c):
        self._circles.append(c)

    