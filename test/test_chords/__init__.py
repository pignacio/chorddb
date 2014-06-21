from chords import Chord
import random

_KEYS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
_VARIATIONS = ["m", "7", "m7", "maj7"]


def _parse_chord(chord):
    Chord.parse(chord)


def no_variation_chord_parse_test():
    """ Parse chords with no variations """
    for key in _KEYS:
        yield _parse_chord, key


def variation_chord_parse_test():
    """ Parse chords with variations """
    for key in _KEYS:
        for variation in _VARIATIONS:
            yield _parse_chord, key + variation


def bass_chord_parse_test():
    ''' Parse chords with bass '''
    for variation in _VARIATIONS + ['']:
        for bass in _KEYS:
            yield _parse_chord, random.choice(_KEYS) + variation + "/" + bass
