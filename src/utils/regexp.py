'''
Created on May 16, 2014

@author: ignacio
'''
import re


def strict(regexp):
    if regexp.startswith("^") or regexp.endswith("$"):
        raise ValueError("Regexp '{}' is already (semi)strict".format(regexp))
    return "^{}$".format(regexp)


class NoMatchError(ValueError):

    def __init__(self, pattern, string):
        ValueError.__init__(self, "Could not match pattern:'{}' "
                            "to string:'{}'".format(pattern, string))
        self._pattern = pattern
        self._string = string

    @property
    def pattern(self):
        return self._pattern

    @property
    def string(self):
        return self._string


def re_search(pattern, string, flags=0):
    mobj = re.search(pattern, string, flags=flags)
    if not mobj:
        raise NoMatchError(pattern, string)
    return mobj
