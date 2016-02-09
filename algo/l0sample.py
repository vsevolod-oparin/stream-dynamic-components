# L0 sketch
# -*- coding: utf-8 -*-

import copy
import primes
import math
import random

from hash import HashK as HashK

def fast_pow(x, p, mod):
    if p == 0:
        return 1
    if p == 1:
        return x
    mult = x if p % 2 == 1 else 1
    return mult * fast_pow(x * x % mod, p / 2, mod)

cache_prime = dict()
def primeMoreThan(n):
    if n not in cache_prime.keys():
        cache_prime[n] = primes.primeMoreThan(4 * n)
    return cache_prime[n]

class Rec1:
    # one test succeeds with wrong valus w.p. 0.25
    # k tests succeed with wrong values w.p. 0.25**k < delta
    # k * log_2 0.25 < log_2 delta
    # k < 2 * log delta^{-1}
    def __init__(self, n, delta):
        self.n = n
        self.p = primeMoreThan(4 * n)
        self.s0 = 0
        self.s1 = 0        
        self.k = 1 - 2 * int(math.ceil(math.log(delta, 2)))
        self.tests = [[0, random.randint(0, self.p - 1)] for i in xrange(self.k)]

    def copy(self):
        result = Rec1(self.n, 1.0)
        result.n = self.n
        result.p = self.p
        result.s0 = self.s0
        result.s1 = self.s1
        result.k = self.k
        result.tests = []
        for test in self.tests:
            result.tests.append([test[0], test[1]])
        return result

    def update(self, ind, val):
        self.s0 += val
        self.s1 += ind * val
        for test in self.tests:
            test[0] += val * fast_pow(test[1], ind, self.p) % self.p

    def recover(self):
        return (self.s1 / self.s0, self.s0)

    def correct(self):
        if self.s0 == 0 or self.s1 % self.s0 != 0 or self.s1 * self.s0 < 0:
            return False
        ind, val = self.recover()
        for test in self.tests:
            if (val * fast_pow(test[1], ind, self.p) - test[0]) % self.p != 0:
                return False
        return True

    def sum(self, rhs):
        result = self.copy()
        result.s0 = self.s0 + rhs.s0
        result.s1 = self.s1 + rhs.s1
        result.tests = [\
            [(self.tests[i][0] + rhs.tests[i][0]) % rhs.p, self.tests[i][1]] for i in xrange(rhs.k)]
        return result
    
class RecS:
    def __init__(self, n, s, delta):
        delta_collision = delta / 2.0
        self.cnt = 0
        self.n = n
        self.s = s
        self.k = 1 - 2 * int(math.ceil(math.log(delta_collision, 2)))
        # print "RecS({0}, {1})".format(self.s, self.k)
        delta_decoder = delta / (2.0 * self.k * self.s)
        self.sketch = [[Rec1(n, delta_decoder) for j in xrange(2 * s)] for i in xrange(self.k)]
        self.hashes = [HashK(2 * s) for i in xrange(self.k)]

    def copy(self):
        result = RecS(self.n, 1, 1.0)
        result.cnt = self.cnt
        result.n = self.n
        result.s = self.s
        result.k = self.k
        result.sketch = [[self.sketch[i][j].copy() for j in xrange(2 * self.s)] for i in xrange(self.k)]
        result.hashes = self.hashes
        return result

    def update(self, ind, val):
        self.cnt += 1
        for i in xrange(self.k):
            h = self.hashes[i]
            self.sketch[i][h.at(ind)].update(ind, val)

    def recover(self):
        result = []
        for table in self.sketch:
            for cell in table:
                if cell.correct():
                    result.append(cell.recover())
        return dict(result)

    def sum(self, rhs):
        result = self.copy()
        result.cnt += rhs.cnt
        result.sketch = [\
            [self.sketch[i][j].sum(rhs.sketch[i][j]) for j in xrange(2 * self.s)] for i in xrange(self.k)]
        return result

    def touched(self):
        return self.cnt != 0

class RecGeneral:
    def __init__(self, n, delta):
        delta_filter = delta / 2.0
        delta_decode = delta / 2.0
        self.s = 3 * (1 - int(math.ceil(math.log(delta_filter, 2))))
        self.k = (1 + int(math.ceil(math.log(n))))
        # print "RecGeneral({0})".format(self.k)
        self.n = n
        self.h = HashK(n**3, self.s)
        self.sketch = [RecS(self.n, self.s, delta_decode) for i in xrange(self.k)]

    def copy(self):
        result = RecGeneral(self.n, 1.0)
        result.s = self.s
        result.k = self.k
        result.n = self.n
        result.h = self.h
        result.sketch = [self.sketch[i].copy() for i in xrange(self.k)]
        return result
    
    def update(self, ind, val):
        for i in xrange(self.k):
            if self.h.at(ind) % (2**i) == 0:
                self.sketch[i].update(ind, val)

    def sample(self):
        for i in xrange(self.k):
            result = self.sketch[self.k - 1 - i].recover()
            if len(result) > 0:
                ind = random.choice(result.keys())
                return ind, result[ind]
        return 0, 0

    def sum(self, rhs):
        result = self.copy()
        result.sketch = [self.sketch[i].sum(rhs.sketch[i]) for i in xrange(rhs.k)]
        return result

def generate_graph_sketch(n, m, delta):
    sketch = RecGeneral(m, delta)
    return [sketch.copy() for i in xrange(n)]

            