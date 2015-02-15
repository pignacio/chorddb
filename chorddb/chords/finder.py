'''
Created on May 17, 2014

@author: ignacio
'''

import collections

from .variations import VARIATIONS_NOTES


PositionedNote = collections.namedtuple('PositionedNote', ['position', 'note'])


def find_fingerings(instrument, keys):
    for positions in search(instrument, keys):
        start = positions.count(None)
        fingering = [x.position for x in positions[start:]]
        yield Fingering(fingering, instrument, start)


BactrackState = collections.namedtuple('BactrackState', ['keys', 'valid_notes',
                                                         'current', 'res'])


def search(instrument, keys):
    return _backtrack(BactrackState(
        keys=set(keys),
        valid_notes=_get_valid_notes(instrument, keys),
        current=[],
        res=[]
    ))


def _backtrack(state):
    if set(c.note.key for c in state.current if c) == state.keys:  # is valid
        state.res.append(list(state.current))  # make a copy
    if len(state.current) == len(state.valid_notes):  # no childs
        return

    used = sorted([c.position for c in state.current if c and c.position])
    maxi = used[-1] if used else 0
    mini = used[0] if used else 10000

    for posnote in state.valid_notes[len(state.current)]:
        if maxi - posnote.position > 4 or posnote.position - mini > 4:
            # Stretch basic test
            continue
        state.current.append(posnote)
        _backtrack(state)
        state.current.pop()

    # Consider empty start:
    if all(c is None for c in state.current):
        state.current.append(None)
        _backtrack(state)
        state.current.pop()

    return state.res

def _get_valid_notes(instrument, keys):
    keys = set(keys)
    valid_notes = []
    for keyoctave in instrument.keyoctaves:
        keyoctaves = (keyoctave.transpose(t) for t in xrange(instrument.frets))
        valid_keyoctaves = (PositionedNote(position=i, note=ko)
                            for i, ko in enumerate(keyoctaves)
                            if ko.key in keys)
        valid_notes.append(list(valid_keyoctaves))
    return valid_notes


def get_fingerings(chord, instrument):
    return list(_get_fingerings(chord, instrument))


def _get_fingerings(chord, instrument):
    if not instrument.has_bass:
        chord = chord.bassless()  # Remove bass if present

    variations = instrument.variation_overrides.get(
        chord.variation, VARIATIONS_NOTES[chord.variation])
    for variation in variations:
        keys = set(chord.key.transpose(v) for v in variation)
        bass_not_in_variation = False
        if instrument.has_bass and not chord.bass in keys:
            keys.add(chord.bass)
            bass_not_in_variation = True

        for fingering in find_fingerings(instrument, keys):
            if instrument.has_bass:
                if fingering.bass().key != chord.bass:
                    continue
                if bass_not_in_variation:
                    bass_count = len([ko for ko in fingering.keyoctaves()
                                      if ko.key == chord.bass])
                    if bass_count > 1:
                        continue
            yield fingering


def _max(fingering):
    return max(x.position for x in fingering if x.position > 0)


def _min(fingering):
    return min(x.position for x in fingering if x.position > 0)


class Fingering(object):
    def __init__(self, positions, instrument, start=None):
        self._instrument = instrument
        self._positions = positions
        self._start = start or 0
        if not 0 <= self._start < instrument.size():
            raise ValueError("Invalid start")
        if instrument.size() < self._start + len(positions):
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

    def full_positions(self):
        res = ["x"] * self._instrument.size()
        res[self._start:self._start] = self._positions
        return res[:self._instrument.size()]

    def __str__(self):
        return "".join(str(x) for x in self.full_positions())


def get_fingering_penalty(fingering):
    try:
        bar = min(x for x in fingering.positions if x)
    except ValueError:
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
        'end': (fingering.instrument.size() - fingering.start -
                len(fingering.positions)) * 8 ** 2,
        'positions': sum((p - bar + 2) ** 2 for p in fingering.positions),
        'bar': bar * fingering.instrument.size() * 3 if bar else 0,
        'consecutive_diffs': sum((a - b) ** 2 for a, b in
                                 zip(fingering.positions,
                                     fingering.positions[1:])
                                 if a and b),
        'four_fingers': 50 if fingers == 4 else 0
    }
    return penalty
