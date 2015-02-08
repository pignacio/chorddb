#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from mock import create_autospec, patch, call
from nose.tools import eq_

from chorddb.chords import Chord
from chorddb.tab import transpose_tablature, transpose_line
from chorddb.tab.objects import (
    Tablature, TabLine, ChordLineData, LyricLineData, TabChord)

from test.utils import mock_namedtuple, Sentinels

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@patch('chorddb.tab.transpose_line')
def tanspose_tablature_test(mock_transpose_line):
    one_line = object()
    other_line = object()
    transposed = {
        one_line: object(),
        other_line: object(),
    }
    tab = mock_namedtuple(Tablature, lines=[one_line, other_line])
    mock_transpose_line.side_effect = lambda l, i: transposed[l]
    expected_calls = [call(one_line, 5), call(other_line, 5)]

    res = transpose_tablature(tab, 5)

    eq_(mock_transpose_line.call_args_list, expected_calls)
    eq_(res.lines, [transposed[one_line], transposed[other_line]])


def transpose_lyrics_line_test():
    line = mock_namedtuple(TabLine, type='lyric')
    eq_(transpose_line(line, 5), line)


def transpose_chord_line_test():
    sentinels = Sentinels()
    chord = create_autospec(Chord)
    other_chord = create_autospec(Chord)

    line = mock_namedtuple(
        TabLine,
        type='chord',
        data=mock_namedtuple(
            ChordLineData,
            chords=[mock_namedtuple(TabChord, chord=c)
                    for c in [chord, other_chord]]
        )
    )

    chord.transpose.return_value = sentinels.transposed_chord
    other_chord.transpose.return_value = sentinels.transposed_other_chord

    transposed = transpose_line(line, 5)

    chord.transpose.assert_called_once_with(5)
    other_chord.transpose.assert_called_once_with(5)
    eq_(transposed.type, 'chord')
    new_chords = [c.chord for c in transposed.data.chords]
    eq_(new_chords,
        [sentinels.transposed_chord, sentinels.transposed_other_chord])
