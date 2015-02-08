#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from nose.tools import eq_

from chorddb.tab import parser
from chorddb.chords import Chord

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def parse_chord_line_test():
    parsed = parser.parse_line('A7    Cm    Fm7')
    eq_(parsed.type, 'chord')
    chords = parsed.data.chords
    eq_(len(chords), 3)
    eq_(chords[0].chord, Chord.parse('A7'))
    eq_(chords[0].position, 0)
    eq_(chords[1].chord, Chord.parse('Cm'))
    eq_(chords[1].position, 6)
    eq_(chords[2].chord, Chord.parse('Fm7'))
    eq_(chords[2].position, 12)


def parse_lyric_line_test():
    lyrics = 'This is a lyrics line'
    parsed = parser.parse_line(lyrics)
    eq_(parsed.type, 'lyric')
    eq_(parsed.data.lyrics, lyrics)


def parse_empty_line_test():
    parsed = parser.parse_line('')
    eq_(parsed.type, 'empty')


def parse_tab_test():
    parsed = parser.parse_tablature([
        'A',
        'A line',
        '',
    ])
    lines = parsed.lines
    eq_(len(lines), 3)
    eq_(lines[0].type, 'chord')
    eq_(len(lines[0].data.chords), 1)
    eq_(lines[0].data.chords[0].position, 0)
    eq_(lines[0].data.chords[0].chord, Chord.parse("A"))
    eq_(lines[1].type, 'lyric')
    eq_(lines[1].data.lyrics, 'A line')
    eq_(lines[2].type, 'empty')
