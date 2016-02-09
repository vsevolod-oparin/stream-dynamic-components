#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from algo.algo_sketch import DynamicGraph as DynamicGraph

class TestCcGraph(unittest.TestCase):

    def test_graph_add(self):
        g = DynamicGraph(6, 0.01)
        edges = [(1, 2), (2, 3), (2, 4), (3, 4), (5, 6)]
        for u, v in edges:
            g.add_edge(u, v)
        result = g.cc()
        answer = [[1, 2, 3, 4], [5 ,6]]
        self.assertEqual(result, answer)

    def test_graph_add_rem(self):
        g = DynamicGraph(6, 0.01)
        add = g.add_edge
        rem = g.remove_edge
        edges = [(1, 3, add), (1, 2, add), (2, 3, add), (1, 3, rem), \
                 (2, 4, add), (3, 4, add), (2, 6, add), (5, 6, add),\
                 (2, 6, rem)]
        for u, v, comd in edges:
            comd(u, v)
        result = g.cc()
        answer = [[1, 2, 3, 4], [5 ,6]]
        self.assertEqual(result, answer)

    def test_graph_empty(self):
        g = DynamicGraph(6, 0.01)
        add = g.add_edge
        rem = g.remove_edge
        edges = [(1, 3, add), (1, 2, add), (2, 3, add), (1, 3, rem), \
                 (2, 4, add), (3, 4, add), (2, 6, add), (5, 6, add),\
                 (2, 6, rem), (1, 2, rem), (2, 3, rem), (5, 6, rem),\
                 (2, 4, rem), (3, 4, rem)]
        for u, v, comd in edges:
            comd(u, v)
        result = g.cc()
        answer = [[i] for i in xrange(1, 7)]
        self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()