'''
Created on May 10, 2014

@author: ignacio
'''
import re
import notes
from notes import Key
from utils.decorators import memoize
from utils.regexp import strict
from chords.variations import VARIATIONS_RE, VARIATIONS, VARIATIONS_NOTES


CHORD_RE = "(({})({})?({})?)".format(notes.NOTES_RE, notes.ACCIDENTALS_RE,
                                     VARIATIONS_RE)


class Chord(object):

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

    @memoize
    def variation_keys(self):
        return set([self.key.transpose(interval)
                    for interval in VARIATIONS_NOTES[self.variation]])

    def text(self):
        return "{}{}".format(self._key,
                             self._variation if self._variation else "")

    def __str__(self):
        return "Chord:{}".format(self.text())

    def transpose(self, interval):
        return Chord(self._key.transpose(interval), self._variation)

    def __hash__(self):
        return hash((self._key, self._variation))

    def __eq__(self, ochord):
        return (isinstance(ochord, Chord) and
                self.key == ochord.key and
                self.variation == ochord.variation)

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
