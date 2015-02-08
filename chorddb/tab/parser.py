#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re

from ..chords import CHORD_RE, Chord
from .objects import (
    Tablature, TabLine, ChordLineData, LyricLineData, TabChord)


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _parse_chord_line(line):
    ''' Parse a chord line into a `ChordLineData` object. '''
    chords = [
        TabChord(position=position, chord=chord)
        for chord, position in Chord.extract_chordpos(line)
    ]
    return ChordLineData(chords=chords)


def _parse_lyric_line(line):
    ''' Parse a lyric line into a LyricLineData object. '''
    return LyricLineData(lyrics=line)


_DATA_PARSERS = {
    'chord': _parse_chord_line,
    'lyric': _parse_lyric_line,
    'empty': lambda l: None,
}


def _get_line_type(line):
    ''' Decide the line type in function of its contents '''
    stripped = line.strip()
    if not stripped:
        return 'empty'
    remainder = re.sub(r"\s+", " ", re.sub(CHORD_RE, "", stripped))
    if len(remainder) * 2 < len(re.sub(r"\s+", " ", stripped)):
        return 'chord'
    return 'lyric'


def parse_line(line):
    ''' Parse a line into a `TabLine` object. '''
    line = line.rstrip()
    line_type = _get_line_type(line)
    return TabLine(
        type=line_type,
        data=_DATA_PARSERS[line_type](line),
        original=line,
    )


def parse_tablature(lines):
    ''' Parse a list of lines into a `Tablature`. '''
    lines = [parse_line(l) for l in lines]
    return Tablature(lines=lines)
