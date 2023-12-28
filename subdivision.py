import pyglet
from pyglet import shapes
import networkx as nx
from objects import *

class PointSubdivision:
    def __init__(self, points = [], 
            mod_func = lambda x,y: (x,y), inverse_mod_func = lambda x,y: (x,y)) -> None:
        self._points = points
        self._inverse_mod_func = inverse_mod_func
        self._mod_func = mod_func

    def get_points(self):
        return self._points

    def add_point(self, p):
        self._points.append(p)

    def get_Q(self):
        return self._Q

    def _initialize_subdivision(self, i):
        self._Q = []
        self._i = i
        side_length = 2**i

        for p in self._points:
            alg_x = ((p.get_alg_x() // side_length) * side_length) 
            alg_y = ((p.get_alg_y() // side_length) * side_length) - 3*side_length

            bottom_left_corner = Point.from_inverse_mod_func(alg_x, alg_y, self._inverse_mod_func)
            self._Q.append(IQuad(bottom_left_corner, i, self._inverse_mod_func))

    # Follows growth algorithm in section 6.4
    def _grow(self, S):
        results = []
        G = nx.Graph()

        G.add_nodes_from([i for i in range(len(S))])

        for i, q1 in enumerate(S):
            for j, q2 in enumerate(S):
                if i != j and q1.does_closure_overlap(q2):
                    G.add_edge(i, j)

        matching = nx.maximal_matching(G)

        covered_quads = []
        for e in matching:
            covered_quads.append(e[0])
            covered_quads.append(e[1])

            q1 = S[e[0]], q2 = S[e[1]]
            q1_bottom_left = q1.get_bottom_left_corner()
            q2_bottom_left = q2.get_bottom_left_corner()


            core_bottom_left_x = min(q1_bottom_left.get_alg_x(), q2_bottom_left.get_alg_x())
            core_bottom_left_y = min(q1_bottom_left.get_alg_y(), q2_bottom_left.get_alg_y())

            core_bottom_left = Point.from_inverse_mod_func(core_bottom_left_x, 
                                    core_bottom_left_y, self._inverse_mod_func)
            
            parent_quad = IQuad.from_core_bottom_left(core_bottom_left, q1.get_i(), self._inverse_mod_func)
            results.append(parent_quad)

            q1.set_grown(parent_quad)
            q2.set_grown(parent_quad)

        for i, quad in enumerate(S):
            if i not in covered_quads:
                parent_quad = IQuad.from_core_bottom_left(quad.get_bottom_left_corner(),
                                    quad.get_i(), self._inverse_mod_func)
                
                results.append(parent_quad)
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

    