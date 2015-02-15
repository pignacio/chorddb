from .notes import KeyOctave, Key
from .chords.variations import map_variations_to_intervals, VARIATIONS_NOTES


class Instrument(object):
    def __init__(self, name, keyoctaves, frets, has_bass=True,
                 variation_overrides=None):
        self._name = name
        self._keyoctaves = keyoctaves
        self._frets = frets
        self._has_bass = has_bass
        self._variation_overrides = variation_overrides or {}

    @property
    def name(self):
        return self._name

    @property
    def keyoctaves(self):
        return self._keyoctaves

    @property
    def frets(self):
        return self._frets

    @property
    def has_bass(self):
        return self._has_bass

    @property
    def variation_overrides(self):
        return self._variation_overrides

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
        return Instrument(
            "{}(Capo: {})".format(self.name, capo_position),
            [ko.transpose(capo_position) for ko in self.keyoctaves],
            self.frets - capo_position,
            self.has_bass
        )

    def __str__(self):
        return "Instrument: {s.name}".format(s=self)

    def __len__(self):
        return len(self._keyoctaves)


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
