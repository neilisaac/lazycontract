from __future__ import absolute_import

from .contract import LazyContract
from .extra import AliasProperty, UUIDProperty, UUIDStringProperty

import uuid


def test_uuid_property():
    class TestUUIDContract(LazyContract):
        g = UUIDProperty()

    example = '14d0a7b5-33c5-439b-a66b-2d464f4e7d1b'
    expected = dict(g=example)

    assert TestUUIDContract(g=example).to_dict() == expected
    assert TestUUIDContract(g=example.upper()).g == uuid.UUID(example)
    assert type(TestUUIDContract(g=example.upper()).g) == uuid.UUID
    assert TestUUIDContract(g=uuid.UUID(example)).to_dict() == expected


def test_uuid_string_property():
    class TestUUIDStringContract(LazyContract):
        g = UUIDStringProperty()

    example = '14d0a7b5-33c5-439b-a66b-2d464f4e7d1b'
    expected = dict(g=example)

    assert TestUUIDStringContract(g=example).to_dict() == expected
    assert TestUUIDStringContract(g=example.upper()).g == example
    assert type(TestUUIDStringContract(g=example.upper()).g) == type(example)
    assert TestUUIDStringContract(g=uuid.UUID(example)).to_dict() == expected


def test_alias_property():
    class TestAliasContract(LazyContract):
        a = UUIDStringProperty()
        b = AliasProperty('a')

    example = '14d0a7b5-33c5-439b-a66b-2d464f4e7d1b'
    expected = dict(a=example, b=example)

    assert TestAliasContract(a=example).to_dict() == expected

    t = TestAliasContract()
    t.b = example
    assert t.to_dict() == expected
