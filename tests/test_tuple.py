from pyCoW import *
from copy import copy

class Test(CoW):
    pass


def test_tuple_basic():
    t = Test()

    t.l = (1,2,3,4)
    assert t.l == (1,2,3,4)

    assert len(t._flyweight_cache[ProxyTuple]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l += (5,)
    assert t.l == (1,2,3,4,5)
    assert t2.l == (1,2,3,4)
    assert len(t._flyweight_cache[ProxyTuple]) == 2

