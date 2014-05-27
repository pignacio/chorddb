'''
Created on May 10, 2014

@author: ignacio
'''
from chords import CHORD_RE, Chord
import StringIO
import colors
import logging
import re
from chords.library import ChordLibrary

LOGGER = logging.getLogger(__name__)


class Tablature(object):

    def __init__(self, lines):
        self._lines = lines

    def render(self, debug=False, instrument=None):
        res = StringIO.StringIO()
        for line in self._lines:
            print >> res, line.render(debug=debug, instrument=instrument)
        return res.getvalue()

    @classmethod
    def parse(cls, lines):
        return cls([TablatureLine.from_line(l.rstrip("\n")) for l in lines])

    @property
    def lines(self):
        return self._lines


class TablatureLine(object):

    def render(self, debug=False, instrument=None):
        contents = []
        if debug:
            contents.append(colors.terminal.ColoredOutput.colored(
                "{}:".format(self.__class__.__name__),
                fore=colors.terminal.GREEN, style=colors.terminal.BRIGHT
            ))
        contents.append(self._render(instrument=instrument))
        return "".join(contents)

    def _render(self, **kwargs):
        raise NotImplementedError()

    def contents(self):
        raise NotImplementedError()

    @classmethod
    def from_line(cls, line):
        return cls._autodetect_line_class(line).from_line(line)

    @staticmethod
    def _autodetect_line_class(line):
        stripped = line.strip()
        if not stripped:
            return EmptyLine
        remainder = re.sub(r"\s+", " ", re.sub(CHORD_RE, "", stripped))
        if len(remainder) * 2 < len(re.sub(r"\s+", " ", stripped)):
            return ChordLine
        return LyricLine


class ChordLine(TablatureLine):

    def __init__(self, chords, positions):
        if len(chords) != len(positions):
            raise ValueError("Different number of chords and positions: "
                             "{} != {}".format(len(chords), len(positions)))
        self._chords = chords
        self._positions = positions
        self._contents = LineContents(chords=zip(chords, positions))

    def _render(self, instrument=None, **kwargs):
        if len(self._positions) < len(self._chords):
            self._positions += [-1] * \
                (len(self._chords) - len(self._positions))
        buff = colors.terminal.ColoredOutput(fore=colors.terminal.CYAN)
        for pos, chord in zip(self._positions, self._chords):
            if buff.tell() < pos:
                buff.write(" " * (pos - buff.tell()))
            buff.write(chord.text(), style=colors.terminal.BRIGHT)
            fingering = ChordLibrary(instrument).get(chord)
            if fingering:
                buff.write("({})".format(fingering), fore=colors.terminal.RED)
            buff.write(" ")
        return buff.getvalue().rstrip()

    def contents(self):
        return self._contents

    @classmethod
    def from_line(cls, line):
        chordpos = Chord.extract_chordpos(line)
        chords, positions = (list(x) for x in zip(*chordpos))
        return cls(chords, positions)


class LyricLine(TablatureLine):

    def __init__(self, line):
        self._line = line
        self._contents = LineContents(line=line)

    def _render(self, **kwargs):
        return self._line

    def contents(self):
        return self._contents

    @classmethod
    def from_line(cls, line):
        return cls(line)


class EmptyLine(TablatureLine):

    def contents(self):
        return LineContents()

    def _render(self, **kwargs):
        return ""

    @classmethod
    def from_line(cls, line):
        return cls()


class LineContents(object):

    def __init__(self, line=None, chords=None):
        self._line = line or ""
        self._chords = chords or []

    @property
    def line(self):
        return self._line

    @property
    def chords(self):
        return self._chords


class TerminalRenderer(object):

    def render(self, tablature, chord_library=None):
        for line in tablature.lines:
            self._render_line(line, chord_library=chord_library)

    def _render_line(self, line, chord_library):
        contents = line.contents()
        if contents.chords:
            print self._render_chords(contents, chord_library)
        else:
            print self._render_text(contents)

    @staticmethod
    def _render_text(contents):
        return contents.line

    @staticmethod
    def _render_chords(contents, chord_library):
        buff = colors.terminal.ColoredOutput(fore=colors.terminal.CYAN)
        for chord, pos in contents.chords:
            if buff.tell() < pos:
                buff.write(" " * (pos - buff.tell()))
            buff.write(chord.text(), style=colors.terminal.BRIGHT)
            if chord_library:
                fingering = chord_library.get(chord)
            else:
                fingering = None
            if fingering:
                buff.write("({})".format(fingering), fore=colors.terminal.RED)
            buff.write(" ")
        return buff.getvalue().rstrip()
