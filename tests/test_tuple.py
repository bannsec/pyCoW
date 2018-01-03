from pyCoW import CoW, ProxyTuple
from copy import copy
import pytest

class MyClass(CoW):
    pass

def test_tuple_setitem_error():
    t = MyClass()

    t.l = (1,2,3,4,1,1)

    with pytest.raises(TypeError):
        t.l[0] = 1

def test_tuple_index():
    t = MyClass()

    t.l = (1,2,3,4,1,1)
    assert t.l == (1,2,3,4,1,1)
    assert len(t._flyweight_cache[ProxyTuple]) == 1
    assert t.l.index(4) == 3

def test_tuple_count():
    t = MyClass()

    t.l = (1,2,3,4,1,1)
    assert t.l == (1,2,3,4,1,1)
    assert len(t._flyweight_cache[ProxyTuple]) == 1
    assert t.l.count(1) == 3

def test_tuple_basic():
    t = MyClass()

    t.l = (1,2,3,4)
    assert t.l == (1,2,3,4)

    assert len(t._flyweight_cache[ProxyTuple]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l += (5,)
    assert t.l == (1,2,3,4,5)
    assert t2.l == (1,2,3,4)
    assert len(t._flyweight_cache[ProxyTuple]) == 2

