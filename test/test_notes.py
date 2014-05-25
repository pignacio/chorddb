'''
Created on May 25, 2014

@author: ignacio
'''

from nose.tools import raises, eq_, ok_

from notes import Key

_NOTES = "ABCDEFG"
_KEYS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


# Helpers


@raises(ValueError, TypeError)
def invalid_key_parse(key):
    ''' Helper for expenting to fail parses '''
    Key.parse(key)


# / Helpers
# Key tests


def note_parse_test():
    ''' Basic note parsing test '''
    for note in _NOTES:
        parsed = Key.parse(note)
        eq_(parsed.note, note)
        eq_(parsed.accidental, None)


def invalid_key_value_parse_test():
    ''' Check' we don't parse invalid stuff '''
    for note in ["H", "a", "b", 1, [], {}, None]:
        yield invalid_key_parse, note


def sharp_parse_test():
    ''' Check sharp parsing '''
    for note in _NOTES:
        Key.parse(note + "#")


def flat_parse_test():
    ''' Check flat parsing '''
    for note in _NOTES:
        Key.parse(note + "b")


def key_normalization_test():
    ''' Check equal keys are parsed to equal Keys '''
    for skey, fkey in [('A#', 'Bb'), ('C#', 'Db'), ('D#', 'Eb'),
                       ('F#', 'Gb'), ('G#', 'Ab'), ]:
        return Key.parse(skey) == Key.parse(fkey)


def key_ord_test():
    ''' Key.ord/Key.from_ord consistency test '''
    for skey in _KEYS:
        key = Key.parse(skey)
        eq_(key, Key.from_ord(key.ord()))


def key_eq_test():
    ''' Check different parses of the same key are equal '''
    for key in _KEYS:
        eq_(Key.parse(key), Key.parse(key))


def key_order_test():
    ''' Checks key ordering '''
    keys = [Key.parse(k) for k in _KEYS]
    for index, key in enumerate(keys):
        for okey in keys[index + 1:]:
            ok_(key < okey)
            ok_(key.ord() < okey.ord())


def key_transpose_test():
    ''' Check transpositions work '''
    keys = [Key.parse(k) for k in _KEYS]
    for index, key in enumerate(keys):
        for interval in xrange(25):
            nindex = (interval + index) % len(keys)
            eq_(key.transpose(interval), keys[nindex])


# / Key tests
