from pyCoW import *
from copy import copy

class Test(CoW):
    pass

def test_dict_values():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert list(t.d.values()) == ['test', 'test2']

def test_dict_update():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    t.d.update({3: 'test3'})
    assert t.d == {1: 'test', 2: 'test2', 3: 'test3'}
    assert t2.d == d

def test_dict_setdefault():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.setdefault(2) == 'test2'
    assert t.d.setdefault(3, 'test3') == 'test3'
    assert t.d == {1: 'test', 2: 'test2', 3: 'test3'}
    assert t2.d == d


def test_dict_popitem():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.popitem() in [(1, 'test'), (2, 'test2')]
    assert t.d.popitem() in [(1, 'test'), (2, 'test2')]
    assert t.d == {}
    assert t2.d == d

def test_dict_pop():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.pop(1) == 'test'
    assert t.d == {2: 'test2'}

def test_dict_keys():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.keys() == set([1, 2])

def test_dict_items():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.items() == set([(1, 'test'), (2, 'test2')])

def test_dict_get():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.get(1) == 'test'

def test_dict_copy():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.copy() == t.d

def test_dict_clear():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    t.d.clear()
    assert t.d == {}
    assert t2.d == {1: 'test', 2: 'test2'}

def test_dict_setitem():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    t.d[1] = 'test2'
    assert t.d == {1: 'test2', 2: 'test2'}
    assert t2.d == {1: 'test', 2: 'test2'}

    t2.d[2] = 'test3'
    assert t.d == {1: 'test2', 2: 'test2'}
    assert t2.d == {1: 'test', 2: 'test3'}

    t.d[3] = 'blerg'
    assert t.d == {1: 'test2', 2: 'test2', 3: 'blerg'}
    assert t2.d == {1: 'test', 2: 'test3'}


def test_dict_basic():
    t = Test()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d

    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

