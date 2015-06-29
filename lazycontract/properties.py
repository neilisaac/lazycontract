from __future__ import absolute_import

from .contract import LazyProperty

import six


class StringProperty(LazyProperty):

    _type = six.string_types


class IntProperty(LazyProperty):

    _type = six.integer_types


class FloatProperty(LazyProperty):

    _type = float
