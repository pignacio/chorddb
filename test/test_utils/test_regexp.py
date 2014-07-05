'''
Unit tests for utils.regexp
'''

from nose.tools import ok_, raises, eq_

from chorddb.utils.regexp import NoMatchError, re_search, strict


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

@raises(ValueError)
def _failed_strict(pattern):
    strict(pattern)

def already_strict_error_test():
    ''' Check for expected error when stricting (semi)strict regexp '''
    for pattern in ['^test', 'test$', '^test$', strict('test')]:
        yield _failed_strict, pattern

def no_match_error_fields_test():
    ''' Test for presense of NoMatchError members '''
    pattern = r'\d{2,3}'
    string = 'this has no numbers'
    try:
        re_search(pattern, string)
    except NoMatchError as err:
        eq_(err.pattern, pattern)
        eq_(err.string, string)


