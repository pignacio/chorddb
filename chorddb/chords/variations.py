'''
Created on May 17, 2014

@author: ignacio
'''
from ..notes import Key


_VARIATIONS_NOTES = {
    None: ["A", "C#", "E"],
    "7": ["A", "C#", "E", "G"],
    "m": ["A", "C", "E"],
    "m7": ["A", "C", "E", "G"],
    "maj7": ["A", "C#", "E", "G#"],
    "dim": ["A", "C", "Eb"],
    "aug": ["A", "C#", "F"],
    "sus4": ["A", "D", "E"],
    "m7": ["A", "C", "E", "G"],
    "m7b5": ["A", "C", "Eb", "G"],
}
VARIATIONS_NOTES = {v: [Key.parse(n).ord() for n in ns]
                    for (v, ns) in _VARIATIONS_NOTES.items()}

VARIATIONS = sorted((v for v in _VARIATIONS_NOTES if v), reverse=True)
VARIATIONS_RE = "|".join(VARIATIONS)
