'''
Created on May 10, 2014

@author: ignacio
'''

# Some definitions for posterity:
# - Note: ABCDEFG
# - Accidental: # and b
# - Key: note + accidental. e.g Ab
# - variation: major, minor, seventh, maj7, etc


_NOTE_ACCIDENTALS = {
    "A": "b#",
    "B": "b",
    "C": "#",
    "D": "b#",
    "E": "b",
    "F": "#",
    "G": "b#",
}
NOTE_ACCIDENTALS = dict((k, list(v)) for (k, v) in _NOTE_ACCIDENTALS.items())

KEY_NORMALIZATIONS = {
    "Ab": "G#",
    "Bb": "A#",
    "B#": "C",
    "Cb": "B",
    "Db": "C#",
    "Eb": "D#",
    "E#": "F",
    "Fb": "E",
    "Gb": "F#",
}


def normalize_key(key):
    return KEY_NORMALIZATIONS.get(key, key)


def normalize(note, accidental):
    if accidental:
        key = note + accidental
        nkey = normalize_key(key)
        note, accidental = nkey
    return note, accidental


def all_keys():
    res = set()
    for note, accidentals in NOTE_ACCIDENTALS.items():
        for accidental in accidentals:
            key = note + accidental
            res.add(normalize_key(key))
        res.add(note)
    return sorted(res)
