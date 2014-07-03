import random
from nose.tools import eq_

from chords import Chord
from notes import Key

__KEYS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
_KEYS = [Key.parse(k) for k in __KEYS]
_VARIATIONS = ["m", "7", "m7", "maj7"]


def _check_text_parsing(chord):
    eq_(Chord.parse(chord.text()), chord)


def basic_chord_parse_test():
    """ Parse chords with no variations """
    for key in _KEYS:
        parsed = Chord.parse(str(key))
        eq_(parsed.key, key)
        eq_(parsed.variation, None)
        eq_(parsed.bass, key)
        _check_text_parsing(parsed)


def variation_chord_parse_test():
    """ Parse chords with variations """
    for key in _KEYS:
        for variation in _VARIATIONS:
            parsed = Chord.parse(str(key) + variation)
            eq_(parsed.key, key)
            eq_(parsed.variation, variation)
            eq_(parsed.bass, key)
            _check_text_parsing(parsed)


def bass_chord_parse_test():
    ''' Parse chords with bass '''
    for key in _KEYS:
        for variation in _VARIATIONS + ['']:
            for bass in _KEYS:
                parsed = Chord.parse(str(key) + variation + "/" + str(bass))
                eq_(parsed.key, key)
                eq_(parsed.variation, variation if variation else None)
                eq_(parsed.bass, bass)