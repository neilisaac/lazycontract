from __future__ import absolute_import

from .contract import (LazyContract, StrictContract, DynamicContract, LazyContractValidationError,
                       LazyContractDeserializationError)
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


def test_strict_contract_invalid_deserialize_attribute():
    class TestContract(StrictContract):
        a = StringProperty()
        b = IntegerProperty()
        c = FloatProperty()

    try:
        TestContract({'x': 'foo'})
        assert 'expected LazyContractValidationError' == False
    except LazyContractValidationError as e:
        assert type(e) == LazyContractValidationError
        assert LazyContractValidationError.INVALID_ATTR_FMT.format(
                'TestContract', 'x') in str(e)


def test_required():
    class TestContract(LazyContract):
        a = StringProperty(required=True)

    try:
        TestContract()
        assert 'LazyContractValidationError expected' == False
    except LazyContractValidationError as e:
        assert LazyContractValidationError.REQUIRED_FMT.format(
                'TestContract', 'a', '') in str(e)


def test_not_none():
    class TestContract(LazyContract):
        a = StringProperty(not_none=True)

    try:
        TestContract()
        assert 'LazyContractValidationError expected' == False
    except LazyContractValidationError as e:
        assert LazyContractValidationError.NOT_NONE_FMT.format(
                'TestContract', 'a') in str(e)

    try:
        TestContract(a=None)
        assert 'LazyContractValidationError expected' == False
    except LazyContractValidationError as e:
        assert LazyContractValidationError.NOT_NONE_FMT.format(
                'StringProperty', 'a') in str(e)

    t = TestContract(a='foobar')
    try:
        t.a = None
        assert 'LazyContractValidationError expected' == False
    except LazyContractValidationError as e:
        assert LazyContractValidationError.NOT_NONE_FMT.format(
                'StringProperty', 'a') in str(e)


def test_hidden_property():
    class TestContract(LazyContract):
        _a = StringProperty()

    assert TestContract(_a='foobar').to_dict() == dict()


def test_exclude_if_none():
    class TestContract(LazyContract):
        a = StringProperty(exclude_if_none=False)

    assert TestContract().to_dict() == dict(a=None)


def test_deserialization_error():
    class TestContract(LazyContract):
        a = IntegerProperty()

    reason = None
    try:
        int('3.2')
    except Exception as e:
        reason = e

    try:
        TestContract(a='3.2')
        assert 'expected LazyContractDeserializationError' == False
    except LazyContractDeserializationError as e:
        assert LazyContractDeserializationError.FMT.format(
                'TestContract', 'a', repr('3.2'), reason) in str(e)


def test_serialization_name():
    class TestContract(LazyContract):
        a = StringProperty(name='b')

    t = TestContract(a='a1')
    assert t.to_dict() == dict(b='a1')

    t.a = 'a2'
    assert t.to_dict() == dict(b='a2')

    t = TestContract(b='b1')
    assert t.to_dict() == dict(b='b1')

    t.b = 'b2'
    assert t.to_dict() == dict(b='b2')


def test_inheritence():
    class TestContract1(LazyContract):
        a = StringProperty()

    class TestContract2(TestContract1):
        b = StringProperty()

    t = TestContract2(a='foo', b='bar')
    assert t.to_dict() == dict(a='foo', b='bar')


def test_lazy_contract_ignores_attribute():
    class TestContract(LazyContract):
        a = StringProperty()

    t = TestContract(a='foo', b='bar')
    assert t.to_dict() == dict(a='foo')
    try:
        t.b
        assert 'Expected AttributeError' == False
    except AttributeError:
        pass


def test_dynamic_contract():
    class TestContract(DynamicContract):
        a = StringProperty()

    t = TestContract(a='foo', b='bar')
    assert t.to_dict() == dict(a='foo')
    assert t.b == 'bar'

def test_equals():
    class TestContract(LazyContract):
        a = StringProperty()
        b = StringProperty()

    t1 = TestContract(a='foo')
    t2 = TestContract(a='foo')
    t3 = TestContract(a='foo', b='bar')

    assert t1 == t2
    assert not t1 != t2
    assert t1 != t3
