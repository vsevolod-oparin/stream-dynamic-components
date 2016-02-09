# Algorithm and graph data structure
# -*- coding: utf-8 -*-

import math

from dsu import DSU as DSU
from l0sample import RecGeneral as RecGeneral
from l0sample import generate_graph_sketch as generate_graph_sketch

class DynamicGraph:
    def __init__(self, n, delta):
        self.n = n
        self.k = 1 + int(math.ceil(math.log(n, 2.0)))
        self.sketch = [generate_graph_sketch(n, n**2, delta) for i in xrange(self.k)]

    def refine(self, u, v):
        u, v = (u, v) if u < v else (v, u)
        return u - 1, v - 1, (u - 1) * self.n + (v - 1)

    def add_edge(self, u, v):
        u, v, edge_num = self.refine(u, v)
        print edge_num
        for i in xrange(self.k):
            self.sketch[i][u].update(edge_num, +1)
            self.sketch[i][v].update(edge_num, -1)

    def remove_edge(self, u, v):
        u, v, edge_num = self.refine(u, v)
        print edge_num
        for i in xrange(self.k):
            self.sketch[i][u].update(edge_num, -1)
            self.sketch[i][v].update(edge_num, +1)

    def decode_edge(self, edge_num):
        return edge_num / self.n, edge_num % self.n

    def cc(self):
        cur_cc = dict([(i, [i]) for i in xrange(self.n)])
        dsu = DSU(self.n)
        for lev in xrange(self.k):
            # computing sketches for level lev
            sketch_sum = dict()
            for key in cur_cc.keys():
                component = cur_cc[key]
                sketch_sum[key] = self.sketch[lev][component[0]]
                for j in xrange(1, len(component)):
                    add_sketch = self.sketch[lev][component[j]]
                    sketch_sum[key] = sketch_sum[key].sum(add_sketch)

            # sampling and union
            for key in sketch_sum.keys():
                edge_num, val = sketch_sum[key].sample()
                if (edge_num, val) != (0, 0):
                    u, v = self.decode_edge(edge_num)
                    print (u, v, edge_num, self.n)
                    dsu.union(u, v)

            # forming new components
            cur_cc = dict()
            for i in xrange(self.n):
                parent = dsu.find(i)
                if parent not in cur_cc:
                    cur_cc[parent] = []
                cur_cc[parent].append(i)

        return sorted([sorted([u + 1 for u in cur_cc[k]]) for k in cur_cc.keys()])