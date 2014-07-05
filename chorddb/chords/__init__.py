'''
Created on May 10, 2014

@author: ignacio
'''
import re
from ..notes import Key, KEY_RE
from ..utils.decorators import memoize
from ..utils.regexp import strict, re_search
from .variations import VARIATIONS_RE, VARIATIONS, VARIATIONS_NOTES


CHORD_RE = "{}(?:{})?(?:/{})?".format(KEY_RE, VARIATIONS_RE, KEY_RE)
_CAPTURING_CHORD_RE = "(({})({})?(?:/({}))?)".format(KEY_RE, VARIATIONS_RE,
                                                     KEY_RE)


class Chord(object):

    def __init__(self, key, variation=None, bass=None):
        self._key = key
        self._variation = variation
        self._bass = bass or self._key

    @property
    def key(self):
        return self._key

    @property
    def variation(self):
        return self._variation

    @property
    def bass(self):
        return self._bass

    @memoize
    def variation_keys(self):
        return set([self.key.transpose(interval)
                    for interval in VARIATIONS_NOTES[self.variation]])

    def text(self):
        bass = ('' if self._key == self._bass
                else "/{}".format(self._bass.text()))
        return "{}{}{}".format(self._key.text(),
                               self._variation if self._variation else "",
                               bass)

    def bassless(self):
        ''' The same chord, but without bass '''
        return Chord(self._key, self._variation)

    def __str__(self):
        return "Chord:{}".format(self.text())

    def transpose(self, interval):
        return Chord(self._key.transpose(interval), self._variation)

    def __hash__(self):
        return hash((self._key, self._variation, self.bass))

    def __eq__(self, ochord):
        return (isinstance(ochord, Chord) and
                self.key == ochord.key and
                self.variation == ochord.variation and
                self.bass == ochord.bass)

    def __ne__(self, ochord):
        return not self == ochord

    @classmethod
    def parse(cls, text):
        mobj = re_search(strict(_CAPTURING_CHORD_RE), text)
        key, variation, bass_key = mobj.groups()[1:4]
        return cls(Key.parse(key), variation,
                   Key.parse(bass_key) if bass_key else None)

    @classmethod
    def extract_chordpos(cls, line):
        index = 0
        remainder = line
        res = []
        while True:
            mobj = re.search(_CAPTURING_CHORD_RE, remainder)
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
