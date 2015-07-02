from __future__ import absolute_import

import six


class LazyContractError(RuntimeError):
    pass


class LazyContractValidationError(LazyContractError):
    ATTR_FMT = '{}.{} value \'{}\' is not of type {}'


class LazyProperty(object):

    _type = type(None)

    def __init__(self, required=False, default=None):
        if required and default is not None:
            raise LazyContractError('default specified for required property')

        self.name = 'anonymous'
        self.required = required
        self.default = default

    def __get__(self, obj, objtype=None):
        value = obj.__dict__.get(self.name, self.default)
        self.validate(value)
        return value

    def __set__(self, obj, value):
        self.validate(value)
        obj.__dict__[self.name] = value

    def validate(self, obj):
        if not isinstance(obj, self._type) and \
                (obj is not None or self.required):
            raise LazyContractValidationError(
                    LazyContractValidationError.ATTR_FMT.format(
                            type(self).__name__, self.name, obj, self._type))

    def serialize(self, obj):
        return obj

    def deserialize(self, obj):
        return obj if isinstance(obj, self._type) else self._type(obj)


class LazyContract(object):

    def __init__(self, _obj=None, **kwargs):
        if _obj is not None and kwargs:
            raise LazyContractError('both _obj and kwargs provided')

        self.__properties = dict()

        self.__discover_properties()
        self.__populate_properties(_obj or kwargs)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={}'.format(name, repr(value))
                      for name, _, value in self.__iter_properties()))

    def __discover_properties(self):
        for name, inst in six.iteritems(type(self).__dict__):
            if isinstance(inst, LazyProperty):
                inst.name = name
                self.__properties[name] = inst

    def __populate_properties(self, obj):
        for key, value in six.iteritems(obj):
            if key in self.__properties:
                setattr(self, key, self.__properties[key].deserialize(value))
            else:
                raise LazyContractValidationError(
                        """LazyContract '{}' has no attribute '{}'""".format(
                                type(self).__name__, key))

    def __iter_properties(self):
        for name, prop in six.iteritems(type(self).__dict__):
            if isinstance(prop, LazyProperty):
                yield name, prop, getattr(self, name)

    def to_dict(self):
        return {name: prop.serialize(value) for name, prop, value
                in self.__iter_properties() if value is not None}
