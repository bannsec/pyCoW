from pyCoW import CoW, ProxyDict
from copy import copy

class MyClass(CoW):
    pass

def test_dict_subdict_append():
    t = MyClass()

    t.l = [1,2,3,{4: 'four'}]
    t.l[-1][4] = 'five'
    assert t.l == [1,2,3,{4: 'five'}]

def test_dict_recursive_proxify():
    t = MyClass()

    # Make complicated dictionary structure
    d = {1: 'one', 2: 'two'}
    e = {3: 'three', 4: ['four']}
    d['e'] = e

    t.d = d
    assert t.d == {1: 'one', 2: 'two', 'e': {3: 'three', 4: ['four']}}

def test_dict_setitem_hash():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    old_hash = hash(t.d)

    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t.d[1] = 'blerg'
    new_hash = hash(t.d)

    assert old_hash != new_hash
    assert len(t._flyweight_cache[ProxyDict]) == 1
    assert new_hash in t._flyweight_cache[ProxyDict]

def test_dict_popitem_hash():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    old_hash = hash(t.d)

    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t.d.popitem()
    new_hash = hash(t.d)

    assert old_hash != new_hash
    assert len(t._flyweight_cache[ProxyDict]) == 1
    assert new_hash in t._flyweight_cache[ProxyDict]

def test_dict_values():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert list(t.d.values()) == ['test', 'test2']

def test_dict_update():
    t = MyClass()

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
    t = MyClass()

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
    t = MyClass()

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
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.pop(1) == 'test'
    assert t.d == {2: 'test2'}

def test_dict_keys():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.keys() == set([1, 2])

def test_dict_items():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.items() == set([(1, 'test'), (2, 'test2')])

def test_dict_get():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.get(1) == 'test'

def test_dict_copy():
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d
    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

    assert t.d.copy() == t.d

def test_dict_clear():
    t = MyClass()

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
    t = MyClass()

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
    t = MyClass()

    d = {1: 'test', 2: 'test2'}
    t.d = d
    assert t.d == d

    assert len(t._flyweight_cache[ProxyDict]) == 1

    t2 = copy(t)
    assert t2.d == t.d

