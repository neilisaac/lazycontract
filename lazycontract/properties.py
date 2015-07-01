from __future__ import absolute_import

from .contract import LazyProperty, LazyContract

import six


class StringProperty(LazyProperty):

    _type = six.string_types

    def deserialize(self, obj):
        return obj if isinstance(obj, self._type) else six.u(obj)


class BooleanProperty(LazyProperty):

    _type = bool


class IntegerProperty(LazyProperty):

    _type = six.integer_types

    def deserialize(self, obj):
        return obj if isinstance(obj, self._type) else int(obj)


class FloatProperty(LazyProperty):

    _type = float


class ObjectProperty(LazyProperty):

    _type = LazyContract

    def __init__(self, kind, *args, **kwargs):
        assert issubclass(kind, LazyContract)
        super(ObjectProperty, self).__init__(*args, **kwargs)
        self._kind = kind

    def serialize(self, obj):
        return obj.to_dict()

    def deserialize(self, obj):
        return obj if isinstance(obj, self._kind) else self._kind(obj)


class ContainerProperty(LazyProperty):

    def __init__(self, lazyproperty=None, *args, **kwargs):
        assert lazyproperty is None or isinstance(lazyproperty, LazyProperty)
        super(ContainerProperty, self).__init__(*args, **kwargs)
        self._property = lazyproperty


class ListProperty(ContainerProperty):

    _type = list

    def serialize(self, obj):
        return obj if self._property is None else [self._property.serialize(e) for e in obj]

    def deserialize(self, obj):
        return obj if self._property is None else [self._property.deserialize(e) for e in obj]


class DictProperty(ContainerProperty):

    _type = dict

    def serialize(self, obj):
        return obj if self._property is None else {k: self._property.serialize(e) for k, e in six.iteritems(obj)}

    def deserialize(self, obj):
        return obj if self._property is None else {k: self._property.deserialize(e) for k, e in six.iteritems(obj)}


class SetProperty(ContainerProperty):

    _type = set

    def serialize(self, obj):
        return obj if self._property is None else {self._property.serialize(e) for e in obj}

    def deserialize(self, obj):
        return obj if self._property is None else {self._property.deserialize(e) for e in obj}
