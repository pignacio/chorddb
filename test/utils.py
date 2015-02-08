#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def mock_namedtuple_class(tuple_class):
    class MockTuple(tuple_class):
        __EXCEPTION_SENTINEL = object()
        def __new__(cls, **kwargs):
            values = [kwargs.get(f, cls.__EXCEPTION_SENTINEL)
                      for f in tuple_class._fields]
            return tuple_class.__new__(cls, *values) #pylint: disable=star-args

        def __init__(self, **kwargs):
            for field in kwargs:
                if not field in self._fields:
                    raise ValueError("'{}' is not a valid field for {}".format(
                        field, tuple_class))
            kwargs = {f: kwargs.get(f, self.__EXCEPTION_SENTINEL)
                      for f in self._fields}
            tuple_class.__init__(self, **kwargs)

        def __getattribute__(self, attr):
            # Avoid recursion filtering _* lookups without doing self._* lookups
            value = tuple_class.__getattribute__(self, attr)
            if attr.startswith("_"):
                return value
            if value == self.__EXCEPTION_SENTINEL:
                raise AttributeError("Missing '{}' field in '{}' mock. (id={})"
                                     .format(attr, tuple_class.__name__,
                                             id(self)))
            return value
    return MockTuple


def mock_namedtuple(tuple_class, **kwargs):
    return mock_namedtuple_class(tuple_class)(**kwargs)


class _Sentinel(object):
    def __init__(self, parent, name):
        self._parent = parent
        self._name = name

    def __repr__(self):
        return "Sentinel({id}):{parent} @ {name}".format(
            id=hex(id(self)), parent=hex(id(self._parent)), name=self._name)


class Sentinels(object):
    def __init__(self):
        self._sentinels = {}

    def __getattribute__(self, attr):
        if attr.startswith('_'):
            return super(Sentinels, self).__getattribute__(attr)
        return self.__getitem__(attr)

    def __getitem__(self, key):
        try:
            return self._sentinels[key]
        except KeyError:
            sentinel = _Sentinel(self, key)
            self._sentinels[key] = sentinel
            return sentinel
