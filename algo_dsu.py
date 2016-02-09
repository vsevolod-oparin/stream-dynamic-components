# Algorithm and graph data structure
# -*- coding: utf-8 -*-

from dsu import DSU as DSU

class DsuGraph:
    def __init__(self, n):
        self.n = n
        self.dsu = DSU(n)
        self.edges = dict()

    def refine(self, u, v):
        u, v = (u, v) if u < v else (v, u)
        if (u, v) not in self.edges:
            self.edges[(u, v)] = 0
        return u, v

    def add_edge(self, u, v):
        u, v = self.refine(u, v)
        self.edges[(u, v)] += 1
        
    def remove_edge(self, u, v):
        u, v = self.refine(u, v)
        self.edges[(u, v)] -= 1
        if self.edges[(u, v)] < 0:
            print "Non-existing edge is deleted"
            raise

    def cc(self):
        for edge in self.edges.keys():
            if self.edges[edge] > 0:
                u, v = edge
                self.dsu.union(u - 1, v - 1)
        result = dict()
        for i in xrange(0, self.n):
            p = self.dsu.find(i)
            if p not in result:
                result[p] = []
            result[p].append(i + 1)
        return sorted([sorted(result[v]) for v in result.keys()])