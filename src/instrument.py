from notes import KeyOctave, Key


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

GUITAR = Instrument.parse([Key(k) for k in list("EADGBE")], 10)
LOOG = Instrument.parse([Key(k) for k in list("GBE")], 10)
UKELELE = Instrument([KeyOctave.parse(k) for k in ["G0", "C0", "E0", "A1"]],
                     10)
