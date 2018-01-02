from pyCoW import *
from copy import copy

class Test(CoW):
    pass

def test_list_setitem():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l[2] = 10
    assert t.l == [1,2,10,4]
    assert t2.l == [1,2,3,4]

def test_list_sort():
    t = Test()

    t.l = [4,2,3,1]
    assert t.l == [4,2,3,1]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.sort()
    assert t.l == [1,2,3,4]
    assert t2.l == [4,2,3,1]

def test_list_reverse():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.reverse()
    assert t.l == [4,3,2,1]
    assert t2.l == [1,2,3,4]

def test_list_remove():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.remove(4)
    assert t.l == [1,2,3]
    assert t2.l == [1,2,3,4]

def test_list_pop():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    assert t.l.pop(2) == 3
    assert t.l == [1,2,4]
    assert t2.l == [1,2,3,4]


def test_list_insert():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.insert(1,5)
    assert t.l == [1, 5, 2, 3, 4]
    assert t2.l == [1,2,3,4]

def test_list_extend():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.extend([5,6,7])
    assert t.l == [1,2,3,4,5,6,7]
    assert t2.l == [1,2,3,4]

def test_list_clear():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.clear()
    assert t.l == []
    assert t2.l == [1,2,3,4]

    t = copy(t2)
    assert t2.l == t.l

    t2.l.clear()
    assert t2.l == []
    assert t.l == [1,2,3,4]


def test_list_append():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.append(5)
    assert t.l == [1,2,3,4,5]
    assert t2.l == [1,2,3,4]

def test_list_basic():
    t = Test()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]

    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l += [5]
    assert t.l == [1,2,3,4,5]
    assert t2.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 2

