# L0 sketch

def Rec1:
    # one test succeeds with wrong valus w.p. 0.25
    # k tests succeed with wrong values w.p. 0.25**k < delta
    # k * log_2 0.25 < log_2 delta
    # k < 2 * log delta^{-1}
    def __init__(self, n, delta):
        self.p = primeMoreThan(4 * n)
        self.s0 = 0
        self.s1 = 0        
        self.k = 1 - 2 * int(math.ceil(math.log(delta, 2)))
        self.tests = [[0, random.randint(0, p - 1)] for i in xrange(self.k)]

    def __init__(self, p, s0, s1, k, tests):
        self.p = p
        self.s0 = s0
        self.s1 = s1
        self.k = k
        self.tests = tests

    def update(self, ind, val):
        self.s0 += val
        self.s1 += i * val
        for test in self.tests:
            test[0] += val * fast_pow(test[1], ind, self.p) % self.p

    def recover(self):
        return (self.s1 / self.s0, self.s0)

    def correct(self):
        if self.s0 == 0:
            return False
        ind, val = self.recover()
        for test in self.tests:
            if (val * fast_pow(test[1], ind, self.p) - test[0]) % self.p != 0:
                return False
        return True

    def sum(self, rhs):
        sum_tests = [[(self.tests[i][0] + rhs.tests[i][0]) % rhs.p, self.tests[i][1]] for i in xrange(rhs.k)]
        return Rec1(rhs.p, self.s0 + rhs.s0, self.s1 + rhs.s1, rhs.k, sum_tests)

def RecS:
    def __init__(self, n, s, delta):
        delta_collision = delta / 2.0
        self.cnt = 0
        self.n = n
        self.s = s
        self.k = 1 - 2 * int(math.ceil(math.log(delta_collision, 2)))
        delta_decoder = delta / (2.0 * self.k * self.s)
        self.skecth = [[Rec1(n, delta_decoder) for j in xrange(2 * s)] for i in xrange(self.k)]
        self.hashes = [HashK(2 * s) for i in xrange(self.k)]

    def __init__(self, cnt, n, s, k, sketch, hashes):
        self.cnt = cnt
        self.n = n
        self.s = s
        self.k = k
        self.sketch = sketch
        self.hashes = hashes

    def update(self, ind, val):
        self.cnt += 1
        for i in xrange(self.k):
            h = self.hashes[i]
            self.sketch[h.at(ind)].update(ind, val)

    def recover(self):
        result = []
        for table in self.sketch:
            for cell in table:
                if cell.correct():
                    result.append(cell.recover())
        return dict(result)

    def sum(self, rhs):
        sum_sketch = [[self.sketch[i][j].sum(rhs.sketch[i][j]) for j in xrange(2 * s)] for i in xrange(self.k)]
        cnt = self.cnt + rhs.cnt
        return RecS(cnt, rhs.n, rhs.s, rhs.k, sum_sketch, rhs.hashes) 

    def touched():
        return self.cnt != 0

def RecGeneral:
    def __init__(self, n, delta):
        delta_filter = delta / 2.0
        delta_decode = delta / 2.0
        s = 12 * (1 - int(math.ceil(math.log(delta_filter, 2))))
        self.k = (1 + int(math.ceil(math.log(n))))
        self.n = n
        self.h = HashK(n**3, self.s)
        self.sketch = [RecS(n, s, delta_decode) for i in xrange(self.k)]

    def __init__(self, k, n, h, sketch):
        self.k = k
        self.n = n
        self.h = h
        self.sketch = sketch

    def update(self, ind, val):
        for i in xrange(k):
            if self.h.at(ind) % (2**i) == 0:
                self.sketch[i].update(ind, val)

    def sample():
        for i in xrange(k):
            if self.sketch[k - 1 - i].touched():
                result = self.sketch[k - 1 - i].recover()
                ind = random.choice(result.keys())
                val = result[ind]
                return ind, val

    def sum(self, rhs):
        sketch_sum = [self.sketch[i].sum(rhs.sketch[i]) for i in xrange(rhs.k)]
        return RecGeneral(rhs.k, rhs.n, rhs.h, sketch_sum)

def generate_graph_sketch(n, m, delta):

            