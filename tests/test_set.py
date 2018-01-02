from pyCoW import *
from copy import copy

class Test(CoW):
    pass


def test_set_basic():
    t = Test()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])

    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l = set([5])
    assert t.l == set([5])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

