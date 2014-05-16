'''
Created on May 10, 2014

@author: ignacio
'''
import re
import yaml
import notes

NOTES = list("ABCDEFG")
NOTES_RE = "[{}]".format("".join(NOTES))

ACCIDENTALS = ["b", "#"]
ACCIDENTALS_RE = "{}".format("|".join(ACCIDENTALS))

VARIATIONS = ["maj7", "m7", "m", "7", "dim", "aug", "sus4"]
VARIATIONS_RE = "{}".format("|".join(VARIATIONS))

CHORD_RE = "(({})({})?({})?)".format(NOTES_RE, ACCIDENTALS_RE, VARIATIONS_RE)
STRICT_CHORD_RE = "^{}$".format(CHORD_RE)


class Chord():

    def __init__(self, note, accidental, variation):
        note, accidental = notes.normalize(note, accidental)
        self._note = note
        self._accidental = accidental
        self._variation = variation

    @property
    def note(self):
        return self._note

    @property
    def accidental(self):
        return self._accidental

    @property
    def variation(self):
        return self._variation

    def key(self):
        return self._note + (self._accidental if self._accidental else "")

    def text(self):
        return "".join(x if x else "" for x in (self._note, self._accidental, self._variation))

    def __str__(self):
        return "Chord:{}".format(self.text())

    @classmethod
    def parse(cls, text):
        mobj = re.search(STRICT_CHORD_RE, text)
        if mobj:
            note, accidental, chord = mobj.groups()[1:]
            return cls(note, accidental, chord)
        else:
            raise ValueError(
                "Couldn't parse Chord from '{}', CHORD_RE={}".format(text, CHORD_RE))

    @classmethod
    def extract_chordpos(cls, line):
        index = 0
        remainder = line
        res = []
        while True:
            mobj = re.search(CHORD_RE, remainder)
            if not mobj:
                break
            chord = mobj.group(1)
            chordpos = remainder.index(chord)
            res.append((Chord.parse(chord), chordpos + index))
            movement = chordpos + len(chord)
            remainder = remainder[movement:]
            index += movement
        return res

    @classmethod
    def all_chords(cls):
        for key in notes.all_keys():
            yield Chord.parse(key)
            for variation in VARIATIONS:
                yield Chord.parse(key + variation)


class ChordLibrary():
    _LIBRARY = None

    @classmethod
    def _init(cls, fname=None):
        if cls._LIBRARY is not None:
            return
        fname = fname or "chord_library.yaml"
        with open(fname) as fin:
            cls._LIBRARY = yaml.load(fin)

    @classmethod
    def get(cls, chord, instrument):
        cls._init()
        try:
            ichords = cls._LIBRARY[instrument]
        except KeyError:
            raise ValueError("Invalid instrument '{}'".format(instrument))

        try:
            chord = ichords[chord.note][chord.key()][chord.text()]
        except KeyError:
            raise ValueError(
                "Could not find {} in variation library".format(chord))

        if not chord:
            raise ValueError("Chord is missing from library: {}".format(chord))

        if isinstance(chord, basestring):
            return chord
        elif isinstance(chord, list):
            return chord[0]
        else:
            raise ValueError(
                "Invalid variation container type for {}: '{}'. should be string or list".format(chord, type(chord)))
