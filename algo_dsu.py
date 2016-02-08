# Algorithm and graph data structure

class DsuGraph:
    def __init__(self, n):
        self.n = n
        self.rank = [0 for i in xrange(n + 1)]
        self.parent = [i for i in xrange(n + 1)]
        self.edges = dict()

    def refine(self, u, v):
        u, v = u, v if u < v else v, u
        if (u, v) not in self.edges:
            self.edges[(u, v)] = 0
        return u, v

    def add_edge(self, u, v):
        u, v = self.refine(u, v)
        self.edges[(u, v)] += 1
        
    def remove_edge(self, u, v):
        u, v = self.refine(u, v)
        self.edges[(u, v)] -= 1

    def cc(self):
        for edge in self.keys():
            if self.edges[edge] != 0:
                u, v = edge
                self.union(u, v)
        result = dict()
        for i in xrange(1, self.n + 1):
            p = self.find(i)
            if p not in result:
                result[p] = []
            result[p].append(i)
        return [result[v] for v in result.keys()]

    def find(self, u):
        if self.parent[u] == u:
            return u
        self.parent[u] = find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        u = self.find(u)
        v = self.find(v)
        if self.rank[u] > self.rank[v]:
            u, v = v, u
        if self.rank[u] == self.rank[v]:
            self.rank[v] += 1
        self.parent[u] = v