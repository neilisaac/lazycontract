#!/usr/bin/env python

from setuptools import setup

setup(name='lazycontract',
      version='0.9',
      description='Python library to define declarative contracts for serialization and deserialization',
      author='Neil Isaac',
      author_email='isaac.neil@gmail.com',
      license='MIT',
      url='https://github.com/neilisaac/lazycontract',
      packages=['lazycontract'],
      install_requires=['six'],
      tests_require=['pytest', 'tox'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries']
      )
