'''
Unit tests for utils.decorators module
'''
import itertools

from nose.tools import eq_

from chorddb.utils.decorators import memoize


class CallCounter(object):
    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self._call_count = 0

    @property
    def call_count(self):
        return self._call_count

    def __call__(self, *args, **kwargs):
        self._call_count += 1
        return self._func(*args, **kwargs)


def noarg_memoize_test():
    ''' Tests memoize on a 0-ary function '''
    value = [1, 2, 3]

    def func():
        return value

    counter = CallCounter(func)
    func = memoize(counter)

    for dummy in xrange(5):
        eq_(func(), value)

    eq_(counter.call_count, 1)


def arg_memoize_test():
    ''' Single arg memoize test '''
    def double(val):
        return 2 * val

    counter = CallCounter(double)
    double = memoize(counter)

    values = [1, 2, 3, 4]
    for val in values:
        for dummy in xrange(5):
            eq_(double(val), 2 * val)
    eq_(counter.call_count, len(values))


def kwarg_memoize_test():
    ''' kwarg memoize test '''
    def multiply(vala, valb):
        return vala * valb

    counter = CallCounter(multiply)
    multiply = memoize(counter)

    values = [1, 2, 3, 4]
    for vala, valb in itertools.product(values, values):
        for dummy in xrange(5):
            eq_(multiply(vala=vala, valb=valb), vala * valb)
            eq_(multiply(valb=valb, vala=vala), vala * valb)
    eq_(counter.call_count, len(values) ** 2)


def unhashable_memoize_test():
    ''' Unhashable arg memoize check '''
    def sort(thing):
        return sorted(thing)

    counter = CallCounter(sort)
    sort = memoize(counter)

    values = [4, 2, 3, 1]
    for dummy in xrange(5):
        eq_(sort(values), sorted(values))


def memoize_cache_immutability_test():
    ''' Test if @memoize cache is immutable '''
    numbers = set([1,2,3,4])
    resp = set(numbers)

    @memoize
    def func():
        return resp

    for _x in xrange(2):
        cached = func()
        eq_(cached, numbers)
        cached.add(5)

    eq_(func(), numbers)
