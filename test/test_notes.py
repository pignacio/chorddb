'''
Created on May 25, 2014

@author: ignacio
'''

import itertools
from nose.tools import raises, eq_, ok_

from chorddb.notes import Key, KeyOctave


_NOTES = "ABCDEFG"
_KEYS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
_KEYOCTAVES = ["{}{}".format(__key, __octave)
               for __octave in xrange(6) for __key in _KEYS]

_INVALID_NOTES = ["H", "a", "b", 1, [], {}, None]
_INVALID_ACCIDENTALS = ['.', '!', 'B', '*', '%']

# Helpers


def _keys():
    ''' Parse all valid keys '''
    return [Key.parse(k) for k in _KEYS]


def _keyoctaves():
    return [KeyOctave.parse(ko) for ko in _KEYOCTAVES]


@raises(ValueError, TypeError)
def invalid_key_parse(key):
    ''' Helper for expenting to fail parses '''
    Key.parse(key)


@raises(ValueError)
def invalid_key_construct(note, accidental=None):
    Key(note, accidental=accidental)


def _check_key_str_parse(key):
    eq_(key, Key.parse(key.text()))


# / Helpers
# Key tests


def note_parse_test():
    ''' Basic note parsing test '''
    for note in _NOTES:
        parsed = Key.parse(note)
        eq_(parsed.note, note)
        eq_(parsed.accidental, None)
        _check_key_str_parse(parsed)


def invalid_key_value_parse_test():
    ''' Check we don't parse invalid Keys '''
    for note in _INVALID_NOTES:
        yield invalid_key_parse, note


def invalid_key_construct_test():
    ''' Check we cant't construct invalid Keys '''
    for note in _INVALID_NOTES:
        yield invalid_key_construct, note
    for accidental in _INVALID_ACCIDENTALS:
        yield invalid_key_construct, "A", accidental


def sharp_parse_test():
    ''' Check sharp parsing '''
    for note in _NOTES:
        parsed = Key.parse(note + "#")
        eq_(Key.parse(note).transpose(1), parsed)
        _check_key_str_parse(parsed)


def flat_parse_test():
    ''' Check flat parsing '''
    for note in _NOTES:
        parsed = Key.parse(note + "b")
        eq_(Key.parse(note).transpose(-1), parsed)
        _check_key_str_parse(parsed)


def key_normalization_test():
    ''' Check equal keys are parsed to equal Keys '''
    for skey, fkey in [('A#', 'Bb'), ('C#', 'Db'), ('D#', 'Eb'),
                       ('F#', 'Gb'), ('G#', 'Ab'), ]:
        return Key.parse(skey) == Key.parse(fkey)


def key_ord_test():
    ''' Check Key.ord/Key.from_ord consistency '''
    for key in _keys():
        eq_(key, Key.from_ord(key.ord()))


def key_eq_test():
    ''' Check different parses of the same key are equal '''
    for key in _KEYS:
        eq_(Key.parse(key), Key.parse(key))


def key_order_test():
    ''' Check Key ordering '''
    for key, okey in itertools.combinations(_keys(), 2):
        ok_(key < okey)
        ok_(key != okey)
        ok_(key.ord() < okey.ord())


def key_transpose_test():
    ''' Check Key transpositions work '''
    keys = _keys()
    for index, key in enumerate(keys):
        for interval in xrange(25):
            nindex = (interval + index) % len(keys)
            eq_(key.transpose(interval), keys[nindex])


# / Key tests
# KeyOctave tests


def keyoctave_parse_test():
    ''' Check valid KeyOctave parses '''
    for key in _KEYS:
        for octave in xrange(10):
            keyoctave = KeyOctave.parse("{}{}".format(key, octave))
            eq_(keyoctave.key, Key.parse(key))
            eq_(keyoctave.octave, octave)


def keyoctave_eq_test():
    ''' Check different parses of the same keyoctave are equal '''
    for keyoctave in _KEYOCTAVES:
        eq_(KeyOctave.parse(keyoctave), KeyOctave.parse(keyoctave))


def keyoctave_ord_test():
    ''' Check Keyoctave's ord/from_ord consistency '''
    for keyoctave in _keyoctaves():
        eq_(keyoctave, KeyOctave.from_ord(keyoctave.ord()))


def keyoctave_order_test():
    ''' Check KeyOctave ordering '''
    for keyoctave, okeyoctave in itertools.combinations(_keyoctaves(), 2):
        ok_(keyoctave < okeyoctave)
        ok_(keyoctave != okeyoctave)
        ok_(keyoctave.ord() < okeyoctave.ord())


def keyoctave_transpose_test():
    ''' Check KeyOctave transpositions work '''
    ikeyoctaves = list(enumerate(_keyoctaves()))
    pairs = itertools.product(ikeyoctaves, ikeyoctaves)

    for (index, keyoctave), (oindex, okeyoctave) in pairs:
        eq_(keyoctave.transpose(oindex - index), okeyoctave)


#  / KeyOctave tests
