from __future__ import absolute_import

from .contract import LazyProperty

import uuid


class AliasProperty(LazyProperty):

    def __init__(self, aliased_property, *args, **kwargs):
        super(AliasProperty, self).__init__(*args, **kwargs)
        self.aliased_property = aliased_property

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.aliased_property)

    def __set__(self, obj, value):
        setattr(obj, self.aliased_property, value)


class UUIDProperty(LazyProperty):

    _type = uuid.UUID

    def deserialize(self, obj):
        return obj if isinstance(obj, self._type) else uuid.UUID(obj)

    def serialize(self, obj):
        return str(obj).lower()


class UUIDStringProperty(LazyProperty):

    _type = str

    def deserialize(self, obj):
        return str(obj if isinstance(obj, uuid.UUID) else uuid.UUID(obj)).lower()

    def serialize(self, obj):
        return obj.lower()
