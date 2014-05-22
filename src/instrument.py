from notes import KeyOctave, Key


class Instrument():

    def __init__(self, keyoctaves, frets, has_bass=True):
        self._keyoctaves = keyoctaves
        self._frets = frets
        self._has_bass = has_bass

    @property
    def keyoctaves(self):
        return self._keyoctaves

    @property
    def frets(self):
        return self._frets

    @property
    def has_bass(self):
        return self._has_bass

    @classmethod
    def parse(cls, keys, frets, **kwargs):
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
        return cls(keyoctaves, frets, **kwargs)

    def __len__(self):
        return len(self._keyoctaves)

GUITAR = Instrument.parse([Key(k) for k in list("EADGBE")], 10, has_bass=True)
LOOG = Instrument.parse([Key(k) for k in list("GBE")], 10, has_bass=False)
UKELELE = Instrument([KeyOctave.parse(k) for k in ["G0", "C0", "E0", "A1"]],
                     10, has_bass=False)

INSTRUMENTS = {
    'guitar': GUITAR,
    'loog': LOOG,
    'ukelele': UKELELE,
}
