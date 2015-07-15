lazycontract
============

### Status

[![TravisCI](https://travis-ci.org/neilisaac/lazycontract.svg)](https://travis-ci.org/neilisaac/lazycontract)
[![Code Climate](https://codeclimate.com/github/neilisaac/lazycontract/badges/gpa.svg)](https://codeclimate.com/github/neilisaac/lazycontract)

Fork the [GitHub project](https://github.com/neilisaac/lazycontract) to contribute!


### Get it

Available on [PyPI](https://pypi.python.org/pypi/lazycontract):

```
pip install lazycontract
```


### Example

```
import json
import lazycontract


# custom property

class SloppyCSVProperty(lazycontract.LazyProperty):

    _type = list

    def deserialize(self, obj):
        return obj.split(",") if isinstance(obj, (str, unicode)) else obj

    def serialize(self, obj):
        return ",".join(str(item) for item in obj)


# custom contract

class SloppyDocument(lazycontract.LazyContract):

    title = lazycontract.StringProperty(default="new document")
    header = SloppyCSVProperty()
    body = lazycontract.ListProperty(SloppyCSVProperty())


# serialization

test1 = SloppyDocument(title="hello world", header=["first", "second"], body=[])
test1.body.append([1, 2])
test1.body.append([3, 4])

print json.dumps(test1.to_dict()) # {"body": ["1,2", "3,4"], "header": "first,second", "title": "hello world"}


# deserialization

data = json.loads('{"body": ["1,2", "3,4"], "header": "first,second", "title": "hello world"}')
test2 = SloppyDocument(data)

print test2.title  # hello world
print test2.header # [u'first', u'second']
print test2.body   # [[u'1', u'2'], [u'3', u'4']]

print type(test2)           # <class '__main__.SloppyDocument'>
print type(test2.header)    # <type 'list'>
print type(test2.header[0]) # <type 'unicode'>

```

See `lazycontract/test_properties.py` for more examples of property usage.


### Goals and inspiration

 * Provide a simple means to express data contracts in code.
 * Blatantly inspired by [jsonobject](https://github.com/dimagi/jsonobject)'s API
 * Attribute serialization, de-serialization and validation should be trivial to understand and implement
 * Errors in the data or contract should be easy to debug
 * Don't impose a wire format or encoder/decoder


### TODO

 * lazy deserialization
 * timestamp properties
