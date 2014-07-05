'''
Created on May 21, 2014

@author: ignacio
'''
from .finder import get_fingering_penalty, get_fingerings
from ..utils.decorators import memoize


class ChordLibrary(object):

    def __init__(self, instrument):
        self._instrument = instrument

    def get(self, chord):
        try:
            return self.get_all(chord)[0]
        except IndexError:
            return None

    @memoize
    def get_all(self, chord):
        fingerings = get_fingerings(chord, self._instrument)
        return sorted(fingerings, key=self._get_penalty)

    @staticmethod
    def _get_penalty(fingering):
        return sum(get_fingering_penalty(fingering).values())
