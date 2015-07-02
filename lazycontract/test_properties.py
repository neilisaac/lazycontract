from __future__ import absolute_import

from .contract import *
from .properties import *


class TestContract(LazyContract):
    a = StringProperty()
    b = IntegerProperty()
    c = FloatProperty()


def test_string_int_float():
    x = TestContract(a='foo', b=1, c=2.3)
    assert x.to_dict() == dict(a='foo', b=1, c=2.3)


def test_object_property():
    class ObjectPropertyContract(LazyContract):
        a = ObjectProperty(TestContract)
        b = ObjectProperty(TestContract)

    x = ObjectPropertyContract(a=dict(a='foo', b=1, c=2.3), b=TestContract(a='bar', b=4, c=5.6))
    assert x.to_dict() == dict(a=dict(a='foo', b=1, c=2.3), b=dict(a='bar', b=4, c=5.6))


def test_list_property():
    class ListPropertyContract(LazyContract):
        a = ListProperty()
        i = ListProperty(IntegerProperty())
        t = ListProperty(ObjectProperty(TestContract))

    x = ListPropertyContract(
        a=[1, 'foo'],
        i=[1, 2, '3'],
        t=[dict(a='foo', b=2, c=3.4), TestContract(a='bar', b=4, c=5.6)])

    assert x.to_dict() == dict(a=[1, 'foo'], i=[1, 2, 3], t=[dict(a='foo', b=2, c=3.4), dict(a='bar', b=4, c=5.6)])


def test_dict_property():
    class DictPropertyContract(LazyContract):
        a = DictProperty()
        i = DictProperty(IntegerProperty())
        t = DictProperty(ObjectProperty(TestContract))

    x = DictPropertyContract(
        a={1: 'foo'},
        i={1: '2'},
        t={'t': TestContract(a='bar', b=4, c=5.6)})

    assert x.to_dict() == dict(a={1: 'foo'}, i={1: 2}, t={'t': dict(a='bar', b=4, c=5.6)})


def test_set_property():
    class SetPropertyContract(LazyContract):
        a = SetProperty()
        i = SetProperty(IntegerProperty())
        t = SetProperty(ObjectProperty(TestContract))

    x = SetPropertyContract(
        a={1, 'foo'},
        i={1, '2'})

    assert x.to_dict() == dict(a={1, 'foo'}, i={1, 2})


def test_kwargs_deserialization():
    x = TestContract(a='foo')
    assert x.a == 'foo'
    assert repr(x) == 'TestContract(a=\'foo\')'


def test_dict_deserialization():
    x = TestContract({'a': 'foo'})
    assert x.a == 'foo'
    assert repr(x) == 'TestContract(a=\'foo\')'


def test_stringcontract_serialization():
    x = TestContract(a='foo')
    x.y = 4
    s = x.to_dict()
    assert type(s) == dict
    assert s['a'] == 'foo'
    assert len(s) == 1
    assert 'y' not in s


def test_invalid_deserialize_attribute():
    exc = None
    try:
        x = TestContract({'x': 'foo'})
    except AttributeError as e:
        exc = e

    assert type(exc) == AttributeError
    assert 'LazyContract \'TestContract\' has no attribute \'x\'' in str(exc)
