from __future__ import absolute_import

from .contract import LazyProperty

import uuid


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
