from pyCoW import CoW
from copy import copy

class Test(CoW):
    pass


def test_bool_basic():
    t = Test()

    t.i = True
    assert t.i == True

    # bool is ignored
    assert len(t._flyweight_cache) == 0

    t2 = copy(t)
    assert t2.i == t.i

    t.i &= False
    assert t.i == False
    assert t2.i == True
    assert len(t._flyweight_cache) == 0

