from pyCoW import CoW
from copy import copy

class Test(CoW):
    pass


def test_int_basic():

    t = Test()

    t.i = 12
    assert t.i == 12

    # Int is ignored
    assert len(t._flyweight_cache) == 0

    t2 = copy(t)
    assert t2.i == t.i

    t.i = 4
    assert t.i == 4
    assert t2.i == 12
    assert len(t._flyweight_cache) == 0

    t.i += 1
    assert t.i == 5
    assert t2.i == 12

