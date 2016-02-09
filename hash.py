# Polynomial k-hash algorithm
# -*- coding: utf-8 -*-

import util

class HashK:
    def __init__(self, dom, k = 2):
        self.dom = dom
        self.p = primeMoreThan(2 * dom)
        self.coeffs = [random.randint(0, self.p - 1) for i in xrange(k)]

    def at(self, x):
        res, mult = 0, 1
        for v in self.coeffs:
            res = (res + mult * v) % self.p
            mult = (mult * x) % self.p
        return res % self.dom