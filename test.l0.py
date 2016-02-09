#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import random

from l0sample import Rec1 as Rec1
from l0sample import RecS as RecS
from l0sample import RecGeneral as RecGeneral

class TestRec1(unittest.TestCase):

    def test_zero(self):
        r = Rec1(100, 0.001)
        self.assertFalse(r.correct())

    def test_one(self):
        r = Rec1(100, 0.001)
        r.update(17, 42)
        self.assertTrue(r.correct())
        self.assertEqual(r.recover(), (17, 42))

    def test_two(self):
        r = Rec1(100, 0.001)
        r.update(1, 1)
        r.update(2, 2)
        self.assertFalse(r.correct())

    def test_many(self):
        r = Rec1(100, 0.001)
        for i in xrange(100):
            r.update(i, i + 17)
        r.update(17, 42)
        for i in xrange(100):
            r.update(i, -(i + 17))
        self.assertTrue(r.correct())
        self.assertEqual(r.recover(), (17, 42))

class TestRecS(unittest.TestCase):
    def test_touched(self):
        r = RecS(100, 5, 0.01)
        self.assertFalse(r.touched())

    def test_zero(self):
        r = RecS(100, 5, 0.01)
        self.assertEqual(r.recover(), dict())

    def test_one(self):
        r = RecS(100, 5, 0.01)
        r.update(17, 42)
        for i in xrange(100):
            ind, val = random.randint(0, 99), random.randint(1, 25)
            r.update(ind, val)
            r.update(ind, -val)
        self.assertTrue(r.touched())
        self.assertEqual(r.recover(), {17: 42})

    def test_five(self):
        r = RecS(100, 5, 0.01)
        updates = dict([(17 + i, 42 + i) for i in xrange(5)])
        for k in updates.keys():
            r.update(k, updates[k])
        for i in xrange(100):
            ind, val = random.randint(0, 99), random.randint(1, 25)
            r.update(ind, val)
            r.update(ind, -val)
        self.assertEqual(r.recover(), updates)

class TestRecGeneral(unittest.TestCase):
    def test_zero(self):
        r = RecGeneral(100, 0.01)
        self.assertEqual(r.sample(), (0, 0))

    def test_many(self):
        size = 20
        rs = [RecGeneral(size, 0.01) for i in xrange(10)]
        vals = [0 for i in xrange(size)]
        for i in xrange(size):
            ind, val = random.randint(0, size - 1), random.randint(-5, 5)
            vals[ind] += val
            for r in rs:
                r.update(ind, val)
        for i in xrange(size):
            if i % 2 == 1 and vals[i] != 0:
                for  r in rs:
                    r.update(i, -vals[i])
                vals[i] -= vals[i]
        answers = [r.sample() for r in rs]
        print vals
        print answers
        for a in answers:
            self.assertTrue(a[0] % 2 == 0 and a[1] == vals[a[0]])


if __name__ == '__main__':
    unittest.main()