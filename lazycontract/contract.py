from __future__ import absolute_import

import six


class LazyContractError(Exception):
    pass


class LazyContractDeserializationError(LazyContractError):
    FMT = 'failed to deserialize {}.{} from {} due to: {}'


class LazyContractValidationError(LazyContractError):
    INVALID_ATTR_FMT = '{} has no attribute \'{}\''
    NOT_NONE_FMT = '{} {} must not be None'
    REQUIRED_FMT = '{}.{} is required'
    ATTR_TYPE_FMT = '{}.{} value {} is not of type {}'


class LazyProperty(object):

    _type = type(None)

    _default_name = '(anonymous)'

    def __init__(self, name=None, default=None,
                 required=False, not_none=False, exclude_if_none=True):
        if required and default is not None:
            raise LazyContractError('default specified for required property')

        self.name = name or self._default_name
        self.required = required
        self.default = default
        self.not_none = not_none
        self.exclude_if_none = exclude_if_none

    def __get__(self, obj, objtype=None):
        value = obj.__dict__.get(self.name, self.default)
        self.validate(value)
        return value

    def __set__(self, obj, value):
        self.validate(value)
        obj.__dict__[self.name] = value

    def validate(self, obj):
        if obj is None and self.not_none:
            raise LazyContractValidationError(
                    LazyContractValidationError.NOT_NONE_FMT.format(
                            type(self).__name__, self.name))

        if not isinstance(obj, self._type) and obj is not None:
            raise LazyContractValidationError(
                    LazyContractValidationError.ATTR_TYPE_FMT.format(
                            type(self).__name__, self.name, repr(obj), self._type))

    def serialize(self, obj):
        return obj

    def deserialize(self, obj):
        return obj if isinstance(obj, self._type) else self._type(obj)


class LazyContract(object):

    def __init__(self, _obj=None, **kwargs):
        if _obj is not None and kwargs:
            raise LazyContractError('both _obj and kwargs provided')

        self.__properties = dict()
        self.__mappings = dict()

        self.__discover_properties(_obj or kwargs)
        self.__populate_properties(_obj or kwargs)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={}'.format(name, repr(value))
                      for name, _, value in self.__iter_properties()))

    def __discover_properties(self, obj):
        for name, inst in six.iteritems(type(self).__dict__):
            if isinstance(inst, LazyProperty):
                self.__properties[name] = inst

                if inst.name == inst._default_name:
                    inst.name = name
                else:
                    self.__mappings[inst.name] = name

                if inst.name not in obj and name not in obj:
                    if inst.required:
                        raise LazyContractValidationError(
                                LazyContractValidationError.REQUIRED_FMT.format(
                                        type(self).__name__, inst.name))

                    if inst.not_none and inst.default is None:
                        raise LazyContractValidationError(
                                LazyContractValidationError.NOT_NONE_FMT.format(
                                        type(self).__name__, inst.name))

    def __populate_properties(self, obj):
        for key, value in six.iteritems(obj):
            if key in self.__mappings:
                key = self.__mappings[key]

            if key not in self.__properties:
                raise LazyContractValidationError(
                        LazyContractValidationError.INVALID_ATTR_FMT.format(
                                type(self).__name__, key))

            if value is not None:
                try:
                    value = self.__properties[key].deserialize(value)
                except Exception as e:
                    raise LazyContractDeserializationError(
                            LazyContractDeserializationError.FMT.format(
                                    type(self).__name__, key, repr(value), e))

            setattr(self, key, value)

    def __iter_properties(self):
        for name, prop in six.iteritems(type(self).__dict__):
            if isinstance(prop, LazyProperty):
                yield name, prop, getattr(self, name)

    def to_dict(self):
        return {prop.name: prop.serialize(value) for name, prop, value
                in self.__iter_properties()
                if not prop.name.startswith('_') and
                (value is not None or not prop.exclude_if_none)}
