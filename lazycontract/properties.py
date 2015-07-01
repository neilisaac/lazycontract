from __future__ import absolute_import

from .contract import LazyProperty, LazyContract

import six


class StringProperty(LazyProperty):

    _type = six.string_types



class IntegerProperty(LazyProperty):
    _type = six.integer_types


class FloatProperty(LazyProperty):

    _type = float


class ObjectProperty(LazyProperty):

    _type = LazyContract

    def __init__(self, kind, *args, **kwargs):
        super(ObjectProperty, self).__init__(*args, **kwargs)
        self.__kind = kind

    def serialize(self, obj):
        return obj.to_dict()

    def deserialize(self, obj):
        return obj if isinstance(obj, self.__kind) else self.__kind(obj)
