#!/usr/bin/env python
# encoding: utf-8

import collections

from .notes import KeyOctave, Key
from .chords.variations import map_variations_to_intervals, VARIATIONS_NOTES


_Instrument = collections.namedtuple('Instrument', [
    'name', 'keyoctaves', 'frets', 'has_bass', 'variation_overrides'], verbose=True)


class Instrument(_Instrument):
    def __new__(cls, *args, **kwargs):
        defaults = {
            'has_bass': False,
            'variation_overrides': {},
        }
        fields_in_args = set(_Instrument._fields[:len(args)])
        kwvalues = {f: kwargs.get(f, defaults[f]) for f in _Instrument._fields
                    if f not in fields_in_args}
        return _Instrument.__new__(cls, *args, **kwvalues)  # pylint: disable=star-args

    @classmethod
    def parse(cls, name, keys, frets, **kwargs):
        keyoctaves = []
        for key in keys:
            if not keyoctaves:
                keyoctaves.append(KeyOctave(key, 0))
            else:
                current = keyoctaves[-1]
                if key <= current.key:
                    keyoctaves.append(KeyOctave(key, current.octave + 1))
                else:
                    keyoctaves.append(KeyOctave(key, current.octave))
        return cls(name, keyoctaves, frets, **kwargs)

    @classmethod
    def from_name(cls, name, default=None):
        try:
            return INSTRUMENTS[name]
        except KeyError:
            if default:
                return default
            raise

    def capo(self, capo_position):
        kwds = {
            'name':"{}(Capo: {})".format(self.name, capo_position),
            'keyoctaves':[ko.transpose(capo_position) for ko in self.keyoctaves],
            'frets':self.frets - capo_position,
        }
        return self._replace(
            name="{}(Capo: {})".format(self.name, capo_position),
            keyoctaves=[ko.transpose(capo_position) for ko in self.keyoctaves],
            frets=self.frets - capo_position,
        )

    def __str__(self):
        return "Instrument: {s.name}".format(s=self)

    def size(self):
        return len(self.keyoctaves)


LOOG_VARIATION_OVERRIDES = {
    '7': map_variations_to_intervals([['G', 'C#', 'E'], ["A", "C#", "G"]]),
    'm7': VARIATIONS_NOTES['m'],
}


GUITAR = Instrument.parse('guitar', [Key(k) for k in list("EADGBE")], 10,
                          has_bass=True)
LOOG = Instrument.parse('loog', [Key(k) for k in list("GBE")], 10,
                        has_bass=False,
                        variation_overrides=LOOG_VARIATION_OVERRIDES)
UKELELE = Instrument('ukelele',
                     [KeyOctave.parse(k) for k in ["G0", "C0", "E0", "A1"]],
                     10, has_bass=False)


INSTRUMENTS = {i.name: i for i in [GUITAR, LOOG, UKELELE]}
