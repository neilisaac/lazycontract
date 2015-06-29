#!/usr/bin/env python

from setuptools import setup

setup(name='lazycontract',
      version='1.0',
      description='Python library to define declarative contracts for serialization and (lazy) deserialization',
      author='Neil Isaac',
      author_email='isaac.neil@gmail.com',
      url='https://github.com/neilisaac/lazycontract',
      packages=['lazycontract'],
      install_requires=['six'],
      tests_require=['pytest', 'tox'],
      )
