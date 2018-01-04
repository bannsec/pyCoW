from pyCoW import CoW, ProxySet
from copy import copy

class MyClass(CoW):
    pass

def test_set_add_hash():
    t = MyClass()

    t.l = set([1,2,3,4])
    old_hash = hash(t.l)
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t.l.add(5)
    new_hash = hash(t.l)

    assert old_hash != new_hash
    assert len(t._flyweight_cache[ProxySet]) == 1

    assert new_hash in t._flyweight_cache[ProxySet]


def test_set_symmetric_update():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.update(set([5,6,7]))
    assert t.l == set([1,2,3,4,5,6,7])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_symmetric_difference_update():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.symmetric_difference_update(set([1,3,4]))
    assert t.l == set([2])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_remove():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.remove(3)
    assert t.l == set([1,2,4])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_pop():
    t = MyClass()

    t.l = set([1])
    assert t.l == set([1])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    assert t.l.pop() == 1
    assert t.l == set()
    assert t2.l == set([1])
    assert len(t._flyweight_cache[ProxySet]) == 2


def test_set_intersection_update():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.intersection_update(set([1,4,5]))
    assert t.l == set([1,4])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_discard():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.discard(2)
    assert t.l == set([1,3,4])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_difference_update():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.difference_update([1,2])
    assert t.l == set([3,4])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_clear():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.clear()
    assert t.l == set()
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_add():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l.add(5)
    assert t.l == set([1,2,3,4,5])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

def test_set_basic():
    t = MyClass()

    t.l = set([1,2,3,4])
    assert t.l == set([1,2,3,4])

    assert len(t._flyweight_cache[ProxySet]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l = set([5])
    assert t.l == set([5])
    assert t2.l == set([1,2,3,4])
    assert len(t._flyweight_cache[ProxySet]) == 2

