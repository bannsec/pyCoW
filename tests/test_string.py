from pyCoW import CoW, ProxyStr
from copy import copy

class MyClass(CoW):
    pass


def test_string_basic():
    t = MyClass()

    t.s = "test"
    assert t.s == "test"

    assert len(t._flyweight_cache[ProxyStr]) == 1

    t2 = copy(t)
    assert t2.s == t.s

    t.s += "q"
    assert t.s == "testq"
    assert t2.s == "test"
    assert len(t._flyweight_cache[ProxyStr]) == 2

