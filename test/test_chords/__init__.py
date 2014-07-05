import random
from nose.tools import eq_

from chorddb.chords import Chord
from chorddb.notes import Key

__KEYS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
_KEYS = [Key.parse(k) for k in __KEYS]
_VARIATIONS = ["m", "7", "m7", "maj7"]


def _check_text_parsing(chord):
    eq_(Chord.parse(chord.text()), chord)


def basic_chord_parse_test():
    """ Parse chords with no variations """
    for key in _KEYS:
        parsed = Chord.parse(key.text())
        eq_(parsed.key, key)
        eq_(parsed.variation, None)
        eq_(parsed.bass, key)
        _check_text_parsing(parsed)


def variation_chord_parse_test():
    """ Parse chords with variations """
    for key in _KEYS:
        for variation in _VARIATIONS:
            parsed = Chord.parse(key.text() + variation)
            eq_(parsed.key, key)
            eq_(parsed.variation, variation)
            eq_(parsed.bass, key)
            _check_text_parsing(parsed)


def bass_chord_parse_test():
    ''' Parse chords with bass '''
    for key in _KEYS:
        for variation in _VARIATIONS + ['']:
            for bass in _KEYS:
                text = key.text() + variation + "/" + bass.text()
                parsed = Chord.parse(text)
                eq_(parsed.key, key)
                eq_(parsed.variation, variation if variation else None)
                eq_(parsed.bass, bass)
