'''
Created on May 10, 2014

@author: ignacio
'''
import re
import yaml
import notes
from notes import Key
from utils.decorators import memoize
from utils.regexp import strict
from chords.variations import VARIATIONS_RE, VARIATIONS


CHORD_RE = "(({})({})?({})?)".format(notes.NOTES_RE, notes.ACCIDENTALS_RE,
                                     VARIATIONS_RE)


class Chord():

    def __init__(self, key, variation=None):
        self._key = key
        self._variation = variation

    @property
    def key(self):
        return self._key

    @property
    def note(self):
        return self._key.note

    @property
    def accidental(self):
        return self._key.accidental

    @property
    def variation(self):
        return self._variation

    def text(self):
        return "{}{}".format(self._key,
                             self._variation if self._variation else "")

    def __str__(self):
        return "Chord:{}".format(self.text())

    def transpose(self, interval):
        return Chord(self._key.transpose(interval), self._variation)

    @classmethod
    def parse(cls, text):
        mobj = re.search(strict(CHORD_RE), text)
        if mobj:
            note, accidental, chord = mobj.groups()[1:]
            return cls(Key(note, accidental), chord)
        else:
            raise ValueError("Couldn't parse Chord from '{}', "
                             "CHORD_RE={}".format(text, CHORD_RE))

    @classmethod
    def extract_chordpos(cls, line):
        index = 0
        remainder = line
        res = []
        while True:
            mobj = re.search(CHORD_RE, remainder)
            if not mobj:
                break
            chord = mobj.group(1)
            chordpos = remainder.index(chord)
            res.append((Chord.parse(chord), chordpos + index))
            movement = chordpos + len(chord)
            remainder = remainder[movement:]
            index += movement
        return res

    @classmethod
    @memoize
    def all(cls):
        for key in Key.all():
            yield Chord(key)
            for variation in VARIATIONS:
                yield Chord(key, variation)


class ChordLibrary():
    _LIBRARY = None

    @classmethod
    def _init(cls, fname=None):
        if cls._LIBRARY is not None:
            return
        fname = fname or "chord_library.yaml"
        with open(fname) as fin:
            cls._LIBRARY = yaml.load(fin)

    @classmethod
    def get(cls, chord, instrument):
        cls._init()
        try:
            ichords = cls._LIBRARY[instrument]
        except KeyError:
            raise ValueError("Invalid instrument '{}'".format(instrument))

        try:
            chord = ichords[chord.note][str(chord.key)][chord.text()]
        except KeyError:
            raise ValueError(
                "Could not find {} in variation library".format(chord))

        if not chord:
            raise ValueError("Chord is missing from library: {}".format(chord))

        if isinstance(chord, basestring):
            return chord
        elif isinstance(chord, list):
            return chord[0]
        else:
            raise ValueError("Invalid variation container type for {}: '{}'. "
                             "Should be string or list".format(chord,
                                                               type(chord)))
