'''
Unit tests for utils.regexp
'''

from nose.tools import ok_, raises

from utils.regexp import NoMatchError, re_search, strict


@raises(NoMatchError)
def failed_re_search(pattern, string, flags=0):
    return re_search(pattern, string, flags=flags)


def re_search_test():
    ''' Basic re_search test '''
    regexp = r'a\d'
    ok_(re_search(regexp, "a1"))
    ok_(re_search(regexp, "ba12"))


def invalid_re_search_test():
    ''' Basic invalid re_search test '''
    regexp = r'a\d'
    yield failed_re_search, regexp, "a"
    yield failed_re_search, regexp, "1"
    yield failed_re_search, regexp, "abcdefg"
    yield failed_re_search, regexp, ""


def strict_re_search_test():
    ''' Basic strict re_search test '''
    regexp = r'a\d'
    ok_(re_search(regexp, "a1"))
    ok_(re_search(strict(regexp), "a1"))
    yield failed_re_search, strict(regexp), "ba12"
    yield failed_re_search, strict(regexp), "ba1"
    yield failed_re_search, strict(regexp), "a12"
