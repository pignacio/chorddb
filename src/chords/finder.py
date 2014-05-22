'''
Created on May 17, 2014

@author: ignacio
'''
from notes import KeyOctave, Key
from chords.variations import VARIATIONS_NOTES
import itertools
from utils.decorators import memoize


class ChordFinder():

    def __init__(self, instrument, chord):
        self._instrument = instrument
        self._chord = chord
        self._keys = chord.variation_keys()
        self._res = []
        self._string_notes = self._get_string_notes()
        self._search()

    def _search(self):
        self._backtrack([])

    def _backtrack(self, current):
        if set(c[1].key for c in current if c) == self._keys:  # is valid
            self._res.append(list(current))
        if len(current) == len(self._string_notes):  # no childs
            return

        used = sorted([c[0] for c in current if c and c[0]])
        maxi = used[-1] if used else 0
        mini = used[0] if used else 10000

        for pos, note in self._string_notes[len(current)]:
            if maxi - pos > 4 or pos - mini > 4:  # Stretch basic test
                continue
            current.append((pos, note))
            self._backtrack(current)
            current.pop()

        # Consider empty:
        if all(c is None for c in current):
            current.append(None)
            self._backtrack(current)
            current.pop()

    def _fingerings(self):
        for positions in self._res:
            start = positions.count(None)
            fingering = [x[0] for x in positions[start:]]
            yield Fingering(fingering, self._instrument, start)

    def _get_string_notes(self):
        string_notes = []
        for keyoctave in self._instrument.keyoctaves:
            string_notes.append([])
            for index in xrange(self._instrument.frets):
                key = keyoctave.transpose(index)
                if key.key in self._keys:
                    string_notes[-1].append((index, key))
        return string_notes

    @classmethod
    def find(cls, instrument, chord):
        return cls(instrument, chord)._fingerings()


def get_fingerings(chord, instrument):
    for fingering in ChordFinder.find(instrument, chord):
        if instrument.has_bass and fingering.bass().key != chord.key:
            continue
        yield fingering


def _max(fingering):
    return max(x[0] for x in fingering if x[0] > 0)


def _min(fingering):
    return min(x[0] for x in fingering if x[0] > 0)


class Fingering():

    def __init__(self, positions, instrument, start=None):
        self._instrument = instrument
        self._positions = positions
        self._start = start or 0
        if not 0 <= self._start < len(instrument):
            raise ValueError("Invalid start")
        if len(instrument) < self._start + len(positions):
            raise ValueError("Invalid positions for instrument")
        if not all(0 <= p < instrument.frets for p in positions):
            raise ValueError("Invalid positions for instrument")

    @property
    def positions(self):
        return self._positions

    @property
    def instrument(self):
        return self._instrument

    @property
    def start(self):
        return self._start

    def keyoctaves(self):
        return [ko.transpose(interval) for ko, interval in
                zip(self._instrument.keyoctaves[self._start:],
                    self._positions)]

    def bass(self):
        return min(self.keyoctaves())

    def _repr(self):
        res = ["x"] * len(self._instrument)
        res[self._start:self._start] = self._positions
        return res[:len(self._instrument)]

    def __str__(self):
        return "".join(map(str, self._repr()))


def get_fingering_penalty(fingering):
    try:
        bar = min(x for x in fingering.positions if x)
    except Exception:
        bar = 0

    indexed_poss = sorted(enumerate(x - bar for x in fingering.positions
                                    if x > bar),
                          key=lambda (string, pos): (pos, string),
                          reverse=True)
    fingers = len(indexed_poss)
    if fingers > 4 or (bar and fingers > 3):
        return {'too many fingers': 10000}
    penalty = {
        'start': fingering.start * 5 ** 2,
        'end': (len(fingering.instrument) - fingering.start -
                len(fingering.positions)) * 8 ** 2,
        'positions': sum((p - bar + 2) ** 2 for p in fingering.positions),
        'bar': bar * len(fingering.instrument) * 3 if bar else 0,
        'consecutive_diffs': sum((a - b) ** 2 for a, b in
                                 zip(fingering.positions,
                                     fingering.positions[1:])
                                 if a and b),
        'four_fingers': 50 if fingers == 4 else 0
    }
    return penalty
