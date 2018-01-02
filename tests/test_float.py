from pyCoW import CoW
from copy import copy

class Test(CoW):
    pass


def test_float_basic():
    t = Test()

    t.i = 12.5
    assert t.i == 12.5

    # float is ignored
    assert len(t._flyweight_cache) == 0

    t2 = copy(t)
    assert t2.i == t.i

    t.i = 4.2
    assert t.i == 4.2
    assert t2.i == 12.5
    assert len(t._flyweight_cache) == 0

    t.i += 1
    assert t.i == 5.2
    assert t2.i == 12.5

