'''
Created on May 10, 2014

@author: ignacio
'''
from functools import total_ordering

from .utils.decorators import memoize
from .utils.regexp import strict, re_search

# Some definitions for posterity:
# - Note: ABCDEFG
# - Accidental: # and b
# - Key: note + accidental. e.g Ab
# - variation: major, minor, seventh, maj7, etc

NOTES = list("ABCDEFG")
NOTES_RE = "[{}]".format("".join(NOTES))

ACCIDENTALS = ["b", "#"]
ACCIDENTALS_RE = "[{}]".format("".join(ACCIDENTALS))

KEY_RE = "{}(?:{})?".format(NOTES_RE, ACCIDENTALS_RE)
_CAPTURING_KEY_RE = "({})({})?".format(NOTES_RE, ACCIDENTALS_RE)

KEY_OCTAVE_RE = r"{}\d+".format(KEY_RE)
_CAPTURING_KEY_OCTAVE_RE = r"({})(\d+)".format(KEY_RE)

_NOTE_ACCIDENTALS = {
    "A": "b#",
    "B": "b",
    "C": "#",
    "D": "b#",
    "E": "b",
    "F": "#",
    "G": "b#",
}

NOTE_ACCIDENTALS = dict((k, list(v)) for (k, v) in _NOTE_ACCIDENTALS.items())
KEY_NORMALIZATIONS = {
    "Ab": "G#",
    "Bb": "A#",
    "B#": "C",
    "Cb": "B",
    "Db": "C#",
    "Eb": "D#",
    "E#": "F",
    "Fb": "E",
    "Gb": "F#",
}


@total_ordering
class Key(object):

    def __init__(self, note, accidental=None):
        if note not in NOTES:
            raise ValueError("Invalid note: '{}'".format(note))
        if accidental and accidental not in ACCIDENTALS:
            raise ValueError("Invalid accidental: '{}'".format(accidental))
        note, accidental = _normalize(note, accidental)
        self._note = note
        self._accidental = accidental

    @property
    def note(self):
        return self._note

    @property
    def accidental(self):
        return self._accidental

    def ord(self):
        return self.all().index(self)

    def transpose(self, interval):
        index = (self.all().index(self) + interval) % len(self.all())
        return self.all()[index]

    def __eq__(self, okey):
        return self.note == okey.note and self.accidental == okey.accidental

    def __ne__(self, okey):
        return not self == okey

    def __lt__(self, okey):
        return (self.note < okey.note or
                (self.note == okey.note and
                 self._accidental_lt(self.accidental, okey.accidental)))

    def __str__(self):
        return "Key:{}".format(self.text())

    def text(self):
        return self.note + self.accidental if self.accidental else self.note

    def __hash__(self):
        return hash((self._note, self._accidental,))

    @classmethod
    def parse(cls, key):
        note, accidental = re_search(strict(_CAPTURING_KEY_RE), key).groups()
        return cls(note, accidental)

    @classmethod
    def from_ord(cls, index):
        return cls.all()[index]

    @classmethod
    @memoize
    def all(cls):
        res = set()
        for note, accidentals in NOTE_ACCIDENTALS.items():
            for accidental in accidentals:
                res.add(cls(note, accidental))
            res.add(cls(note))
        return sorted(res)

    @staticmethod
    def _accidental_lt(accidental, oaccidental):
        if accidental == 'b':
            return oaccidental is None or oaccidental == '#'
        elif accidental is None:
            return oaccidental == "#"
        return False


@total_ordering
class KeyOctave(object):

    def __init__(self, key, octave):
        self._key = key
        self._octave = octave

    @property
    def key(self):
        return self._key

    @property
    def octave(self):
        return self._octave

    def transpose(self, interval):
        return self.from_ord(self.ord() + interval)

    @classmethod
    def from_ord(cls, value):
        keys = Key.all()
        octave, index = divmod(value, len(keys))
        return cls(keys[index], octave)

    def ord(self):
        keys = Key.all()
        return self._octave * len(keys) + keys.index(self._key)

    def __eq__(self, okey):
        return self.key == okey.key and self.octave == okey.octave

    def __ne__(self, okey):
        return not self == okey

    def __lt__(self, okey):
        return (self.octave < okey.octave or
                (self.octave == okey.octave and self.key < okey.key))

    def __str__(self):
        return "KeyOctave:{}".format(self.text())

    def text(self):
        return "{}{}".format(self._key.text(), self._octave)

    def __hash__(self):
        return hash((self._key, self._octave,))

    @classmethod
    def parse(cls, key_octave):
        key, octave = re_search(strict(_CAPTURING_KEY_OCTAVE_RE),
                                key_octave).groups()
        return cls(Key.parse(key), int(octave))


def _normalize(note, accidental):
    if accidental:
        key = note + accidental
        nkey = KEY_NORMALIZATIONS.get(key, key)
        note, accidental = nkey if len(nkey) > 1 else (nkey, None)
    return note, accidental
