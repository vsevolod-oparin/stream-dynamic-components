# Utul methods 
# -*- coding: utf-8 -*-

def isPrime(v):
    if v == 2:
        return True
    if v % 2 == 0:
        return False
    i = 3
    while i * i <= v:
        if v % i == 0:
            return False
        i += 2
    return True

def primeMoreThan(v):
    while not isPrime(v):
        v += 1
    return v
            