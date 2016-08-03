from __future__ import absolute_import

from .contract import LazyContract, LazyContractValidationError, LazyContractDeserializationError
from .properties import (ObjectProperty, ListProperty, SetProperty,
                         DictProperty, StringProperty, IntegerProperty,
                         FloatProperty, BooleanProperty, EnumerationProperty)


def test_basic_properties():
    class TestContract(LazyContract):
        a = StringProperty()
        b = IntegerProperty()
        c = FloatProperty()
        d = BooleanProperty()

    expected = dict(a='foo', b=1, c=2.3, d=False)
    t1 = TestContract(a='foo', b=1, c=2.3, d=False)
    t2 = TestContract(a='foo', b='1', c='2.3', d='false')
    assert t1.to_dict() == expected
    assert t2.to_dict() == expected


def test_object_property():
    class TestContract(LazyContract):
        a = StringProperty()
        b = IntegerProperty()
        c = FloatProperty()

    class ObjectPropertyContract(LazyContract):
        a = ObjectProperty(TestContract)
        b = ObjectProperty(TestContract)

    x = ObjectPropertyContract(a=dict(a='foo', b=1, c=2.3),
                               b=TestContract(a='bar', b=4, c=5.6))
    assert x.to_dict() == dict(a=dict(a='foo', b=1, c=2.3),
                               b=dict(a='bar', b=4, c=5.6))


def test_list_property():
    class TestContract(LazyContract):
        a = StringProperty()
        b = IntegerProperty()
        c = FloatProperty()

    class ListPropertyContract(LazyContract):
        a = ListProperty()
        i = ListProperty(IntegerProperty())
        t = ListProperty(ObjectProperty(TestContract))

    x = ListPropertyContract(
        a=[1, 'foo'],
        i=[1, 2, '3'],
        t=[dict(a='foo', b=2, c=3.4), TestContract(a='bar', b=4, c=5.6)])

    expected = dict(a=[1, 'foo'],
                    i=[1, 2, 3],
                    t=[dict(a='foo', b=2, c=3.4),
                       dict(a='bar', b=4, c=5.6)])

    assert x.to_dict() == expected


def test_dict_property():
    class TestContract(LazyContract):
        a = StringProperty()
        b = IntegerProperty()
        c = FloatProperty()

    class DictPropertyContract(LazyContract):
        a = DictProperty()
        i = DictProperty(IntegerProperty())
        t = DictProperty(ObjectProperty(TestContract))

    x = DictPropertyContract(
        a={1: 'foo'},
        i={1: '2'},
        t={'t': TestContract(a='bar', b=4, c=5.6)})

    assert x.to_dict() == dict(a={1: 'foo'},
                               i={1: 2},
                               t={'t': dict(a='bar', b=4, c=5.6)})


def test_set_property():

    class TestContract(LazyContract):
        a = StringProperty()

        def __eq__(self, other):
            return self.a == other.a

        def __hash__(self):
            return hash(self.a)

    class SetPropertyContract(LazyContract):
        a = SetProperty()
        i = SetProperty(IntegerProperty())
        t = SetProperty(ObjectProperty(TestContract))

    x = SetPropertyContract(
        a={1, 'foo'},
        i={1, '2', 2, '1', '2'},
        t=[{'a': 'aa'}, {'a': 'aa'}])

    assert x.to_dict() == dict(a=[1, 'foo'],
                               i=[1, 2],
                               t=[{'a': 'aa'}])


def test_enum_property():

    class TestContract(LazyContract):
        x = EnumerationProperty(['a', 'b', 'c'])
        y = EnumerationProperty(['a', 'b', 'c'], not_none=True)
        z = EnumerationProperty(['a', 'b', 'c'], default='c')

    t = TestContract(x='a', y='b')
    assert t.x == 'a'
    assert t.y == 'b'
    assert t.z == 'c'

    t = TestContract(y='b')
    assert t.x is None
    assert t.y == 'b'
    assert t.z == 'c'

    t = TestContract(y='b', z=None)
    assert t.x is None
    assert t.y == 'b'
    assert t.z is None

    try:
        TestContract(x=1, y='b')
        assert 'Expected LazyContractDeserializationError' == False
    except LazyContractDeserializationError:
        pass

    try:
        TestContract(y='d')
        assert 'Expected LazyContractDeserializationError' == False
    except LazyContractDeserializationError:
        pass

    try:
        TestContract(b=None)
        assert 'Expected LazyContractValidationError' == False
    except LazyContractValidationError:
        pass
