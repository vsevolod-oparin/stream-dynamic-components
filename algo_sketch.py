# Algorithm and graph data structure

class DynamicGraph:
    def __init__(self, n, delta):
        self.n = n
        self.sketches = generate_graph_sketch(n, n**2, delta)

    def refine(self, u, v):
        u, v = u, v if u < v else v, u
        return u - 1, v - 1

    def add_edge(self, u, v):
        u, v = self.refine(u, v)
        self.sketches[u].update(u * n + v, +1)
        self.sketches[v].update(u * n + v, -1)

    def remove_edge(self, u, v):
        u, v = self.refine(u, v)
        self.sketches[u].update(u * n + v, -1)
        self.sketches[v].update(u * n + v, +1)

    def decode_edge(self, edge_num):
        return edge_num / self.n, edge_num % self.n

    def cc(self):
        levels = self.sketches[0].k
        for i in xrange(k):
            nb = [-1 for i in xrange(n)]
            for v in xrange(n):
                edge_num = self.skethes[v][i].sample()
                a, b = self.decode_edge(edge_num)
                u = a if v == b else b
                nb[v] = u
            # TODO: like a wrong way to implement...