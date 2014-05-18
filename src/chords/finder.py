'''
Created on May 17, 2014

@author: ignacio
'''
from notes import KeyOctave
from chords.variations import VARIATIONS_NOTES
import itertools
from utils.decorators import memoize


class Keyoctave(object):

    def __init__(self, key, octave):
        pass


class Instrument():

    def __init__(self, keyoctaves, frets):
        self._keyoctaves = keyoctaves
        self._frets = frets

    @property
    def keyoctaves(self):
        return self._keyoctaves

    @property
    def frets(self):
        return self._frets


    @classmethod
    def parse(cls, keys, frets):
        keyoctaves = []
        for i, key in enumerate(keys):
            if not keyoctaves:
                keyoctaves.append(KeyOctave(key, 0))
            else:
                current = keyoctaves[-1]
                if key <= current.key:
                    keyoctaves.append(KeyOctave(key, current.octave + 1))
                else:
                    keyoctaves.append(KeyOctave(key, current.octave))
        return cls(keyoctaves, frets)

    def __len__(self):
        return len(self._keyoctaves)

def _all_start_ends(size):
    for start in xrange(size):
        for end in xrange(start, size):
            yield start, end + 1

def get_fingerings(chord, instrument, bass_check=True):
    keys = set([chord.key.transpose(interval) for interval in VARIATIONS_NOTES[chord.variation]])
    string_notes = []
    for keyoctave in instrument.keyoctaves:
        string_notes.append([])
        for index in xrange(instrument.frets):
            key = keyoctave.transpose(index)
            if key.key in keys:
                string_notes[-1].append(index)
    for positions in itertools.product(*string_notes):
        for start, end in _all_start_ends(len(instrument)):
            if end - start < len(keys):
                continue
            fingering = Fingering(positions, instrument, start=start, end=end)
            if max(fingering.positions()) - min(fingering.positions()) > 4:  # basic stretch test
                continue
            if len(set(ko.key for ko in fingering.keyoctaves())) != len(keys):  # full chord test
                continue
            if bass_check and fingering.bass().key != chord.key:  # bass note test
                continue
            yield fingering

def _max(fingering):
    return max(x[0] for x in fingering if x[0] > 0)

def _min(fingering):
    return min(x[0] for x in fingering if x[0] > 0)


class Fingering():
    def __init__(self, positions, instrument, start=None , end=None):
        self._instrument = instrument
        self._positions = positions
        self._start = start or 0
        self._end = end or len(positions)
        if not 0 <= self._start < len(positions):
            raise ValueError("Invalid start")
        if not start < self._end <= len(positions):
            raise ValueError("Invalid end")
        if len(instrument) != len(positions):
            raise ValueError("Invalid positions for instrument")
        if not all(0 <= p < instrument.frets for p in positions):
            raise ValueError("Invalid positions for instrument")

    @memoize
    def positions(self):
        return [self._positions[index] for index in xrange(self._start, self._end)]

    def keyoctaves(self):
        return [ko.transpose(interval) for ko, interval in zip(self._instrument.keyoctaves, self._positions)[self._start:self._end]]

    def bass(self):
        return min(self.keyoctaves())

    def penalty(self):
        bar = min(self.positions())
        indexed_poss = sorted(enumerate(x - bar for x in self.positions() if x > bar), key=lambda (string, pos): (pos, string), reverse=True)
        fingers = len(indexed_poss)
        if len(indexed_poss) > 4 or (bar and fingers > 3):
            return 10000
        penalty = self._start * 7 ** 2
        penalty += (len(self._instrument) - self._end) * 8 ** 2
        penalty += sum((p - bar + 2) ** 2 for p in self.positions())
        if bar:
            penalty += len(self._instrument) * 3 ** 2 + bar * 10
        return penalty


    def _repr(self):
        res = ["x"] * len(self._instrument)
        res[self._start:self._end] = self.positions()
        return res

    def __str__(self):
        return "".join(map(str, self._repr()))


