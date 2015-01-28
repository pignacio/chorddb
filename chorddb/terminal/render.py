#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from StringIO import StringIO
import collections
import logging

from ..chords.library import ChordLibrary

from .color import colorize
from . import color

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


FingeredChord = collections.namedtuple('Fingeredchord', ['chord', 'fingering'])


def _get_fingerings(chords, instrument):
    return [(chord.position,
             FingeredChord(chord=chord.chord,
                           fingering=ChordLibrary(instrument).get(chord.chord)))
            for chord in chords]

def _write_to_buff(buff, text, fore=color.WHITE, back=color.BLACK,
                   style=color.STYLE_NORMAL):
    buff.write(colorize(text, fore, back, style))
    return len(text)

def _render_chord_line(line, instrument):
    chords = _get_fingerings(line.data.chords, instrument)
    buff = StringIO()
    size = 0
    for position, chord in chords:
        if position > size:
            size += _write_to_buff(buff, " " * (position - size))
        _write_to_buff(buff, chord.chord.text(), color.CYAN,
                       style=color.STYLE_BRIGHT)
        if chord.fingering:
            size += _write_to_buff(buff, "({})".format(chord.fingering),
                                   color.RED)
    return buff.getvalue()


def _render_line(line, instrument, debug=False):
    if debug:
        print colorize("{:8s}:".format(line.type), color.GREEN,
                       style=color.STYLE_BRIGHT),
    if line.type == 'empty':
        print
    elif line.type == 'lyric':
        print line.data.lyrics
    elif line.type == 'chord':
        print _render_chord_line(line, instrument)
    else:
        print colorize("Unknown line type: '{}'".format(line.type), fore=RED,
                       style=STYLE_BRIGHT)
        print line.original


def render_tablature(tablature, instrument, debug=False):
    for line in tablature.lines:
        _render_line(line, instrument, debug=debug)
