from __future__ import absolute_import

from .contract import LazyContract
from .properties import StringProperty, IntegerProperty, FloatProperty


def test_to_dict():
    class TestContract(LazyContract):
        a = StringProperty()

    x = TestContract(a='foo')
    x.y = 4
    s = x.to_dict()
    assert type(s) == dict
    assert s['a'] == 'foo'
    assert len(s) == 1
    assert 'y' not in s


def test_kwargs_deserialization():
    class TestContract(LazyContract):
        a = StringProperty()

    x = TestContract(a='foo')
    assert x.a == 'foo'
    assert repr(x) == 'TestContract(a=\'foo\')'


def test_dict_deserialization():
    class TestContract(LazyContract):
        a = StringProperty()

    x = TestContract({'a': 'foo'})
    assert x.a == 'foo'
    assert repr(x) == 'TestContract(a=\'foo\')'


def test_invalid_deserialize_attribute():
    class TestContract(LazyContract):
        a = StringProperty()
        b = IntegerProperty()
        c = FloatProperty()

    exc = None
    try:
        TestContract({'x': 'foo'})
    except AttributeError as e:
        exc = e

    assert type(exc) == AttributeError
    assert 'LazyContract \'TestContract\' has no attribute \'x\'' in str(exc)
