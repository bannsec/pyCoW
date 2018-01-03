from pyCoW import CoW
from copy import copy

class MyClass(CoW):
    pass

def test_none_basic():
    t = MyClass()

    t.i = None
    assert t.i == None

    # None is ignored
    assert len(t._flyweight_cache) == 0

    t2 = copy(t)
    assert t2.i == t.i

    t.i = 1
    assert t.i == 1
    assert t2.i == None
    assert len(t._flyweight_cache) == 0

