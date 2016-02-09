#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from algo.algo_dsu import DsuGraph as DsuGraph

class TestDsuGraph(unittest.TestCase):

    def test_graph_add(self):
        g = DsuGraph(6)
        edges = [(1, 2, ), (2, 3), (2, 4), (3, 4), (5, 6)]
        for u, v in edges:
            g.add_edge(u, v)
        result = g.cc()
        answer = [[1, 2, 3, 4], [5 ,6]]
        self.assertEqual(result, answer)

    def test_graph_add_rem(self):
        g = DsuGraph(6)
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


    def test_graph_error(self):
        g = DsuGraph(6)
        with self.assertRaises(TypeError):
            g.remove_edge(1, 2)

if __name__ == '__main__':
    unittest.main()