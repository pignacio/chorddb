'''
Created on May 17, 2014

@author: ignacio
'''
from ..notes import Key


def map_variations_to_intervals(variations):
    return[
        [Key.parse(note).ord() for note in variation]
        for variation in variations]



_VARIATIONS_NOTES = {
    None: [["A", "C#", "E"]],
    "7": [["A", "C#", "E", "G"]],
    "m": [["A", "C", "E"]],
    "m7": [["A", "C", "E", "G"]],
    "maj7": [["A", "C#", "E", "G#"]],
    "dim": [["A", "C", "Eb"]],
    "aug": [["A", "C#", "F"]],
    "sus4": [["A", "D", "E"]],
    "m7b5": [["A", "C", "Eb", "G"]],
}
VARIATIONS_NOTES = {v: map_variations_to_intervals(nss)
                    for (v, nss) in _VARIATIONS_NOTES.items()}

VARIATIONS = sorted((v for v in _VARIATIONS_NOTES if v), reverse=True)
VARIATIONS_RE = "|".join(VARIATIONS)
