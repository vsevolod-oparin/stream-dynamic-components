# Algorithm and graph data structure
# -*- coding: utf-8 -*-

class DSU:
    def __init__(self, n):
        self.n = n
        self.rank = [0 for i in xrange(n)]
        self.parent = [i for i in xrange(n)]

    def find(self, u):
        if self.parent[u] == u:
            return u
        self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        u = self.find(u)
        v = self.find(v)
        if self.rank[u] > self.rank[v]:
            u, v = v, u
        if self.rank[u] == self.rank[v]:
            self.rank[v] += 1
        self.parent[u] = v