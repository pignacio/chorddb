#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from mock import patch, create_autospec, Mock
from nose.tools import eq_
from unittest import TestCase

from chorddb.curses.state import RenderState, IndexedChord, _get_indexed_chords_versions, ChordLibrary, _get_indexed_chords, wrap_get
from ..test_tab.mock_objects import MockTablature, MockTabLine, MockChordLineData, MockTabChord
from ..utils import (
    Sentinels, make_namedtuple as make_nt, mock_namedtuple as mock_nt)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class RenderStateInitialTests(TestCase):
    ''' Tests for RenderState.initial_state '''
    def setUp(self):
        self.sentinels = Sentinels()

        # Patches
        self.get_chords_patch = patch(
            'chorddb.curses.state._get_indexed_chords')
        self.get_versions_patch = patch(
            'chorddb.curses.state._get_indexed_chords_versions')
        # mocks
        self.get_chords_mock = self.get_chords_patch.start()
        self.get_versions_mock = self.get_versions_patch.start()
        # return values
        self.get_chords_mock.return_value = self.sentinels.indexed_chords
        self.get_versions_mock.return_value = self.sentinels.chord_versions

        self.screen = make_nt(
            width=self.sentinels.screen_width,
            height=self.sentinels.screen_height,
        )

        self.state = RenderState.initial_state(
            self.sentinels.tablature,
            self.sentinels.instrument,
            self.screen,
        )

    def tearDown(self):
        self.get_chords_patch.stop()
        self.get_versions_patch.stop()

    def test_initial_chord_versions(self):
        self.get_chords_mock.assert_called_once_with(self.sentinels.tablature)
        self.get_versions_mock.assert_called_once_with(
            self.sentinels.indexed_chords, self.sentinels.instrument)
        eq_(self.state.indexed_chords, self.sentinels.indexed_chords)
        eq_(self.state.chord_versions, self.sentinels.chord_versions)

    def test_initial_lyrics_position(self):
        eq_(self.state.lyrics_position, 0)

    def test_initial_current_chord_index(self):
        eq_(self.state.current_chord_index, 0)

    def test_initial_running(self):
        eq_(self.state.running, True)

    def test_initial_tablature(self):
        eq_(self.state.tablature, self.sentinels.tablature)

    def test_initial_instrument(self):
        eq_(self.state.instrument, self.sentinels.instrument)

    def test_initial_screen_width(self):
        eq_(self.state.screen_width, self.sentinels.screen_width)

    def test_initial_current_chord_version_index(self):
        non_zero_values = [v for v in self.state.current_chord_version_index.values()
                           if v != 0]
        eq_(len(non_zero_values), 0)

    def test_initial_chord_drawing_is_reversed(self):
        eq_(self.state.chord_drawing_is_reversed, False)


@patch('chorddb.curses.state.ChordLibrary')
def test_get_indexed_chords_versions(mock_chord_library):
    sentinels = Sentinels()
    indexed_chords = [
        mock_nt(IndexedChord, chord=sentinels.first_chord),
        mock_nt(IndexedChord, chord=sentinels.second_chord),
        mock_nt(IndexedChord, chord=sentinels.first_chord),
    ]
    chord_versions = {
        sentinels.first_chord: sentinels.first_versions,
        sentinels.second_chord: sentinels.second_versions,
    }

    mock_library = create_autospec(ChordLibrary)
    mock_library.get_all.side_effect = lambda c: chord_versions[c]
    mock_chord_library.return_value = mock_library

    versions = _get_indexed_chords_versions(indexed_chords,
                                            sentinels.instrument)

    mock_chord_library.assert_called_once_with(sentinels.instrument)
    eq_(versions[sentinels.first_chord], sentinels.first_versions)
    eq_(versions[sentinels.second_chord], sentinels.second_versions)


def test_get_indexed_chords():
    sentinels = Sentinels()
    tablature_mock = MockTablature(
        lines=[
            MockTabLine(
                type='chord',
                data=MockChordLineData(
                    chords=[
                        MockTabChord(chord=sentinels.chord00),
                        MockTabChord(chord=sentinels.chord01),
                    ]
                )
            ),
            MockTabLine(type='lyrics'),
            MockTabLine(type='empty'),
            MockTabLine(
                type='chord',
                data=MockChordLineData(
                    chords=[
                        MockTabChord(chord=sentinels.chord30)
                    ]
                )

            )
        ]
    )
    indexed_chords = _get_indexed_chords(tablature_mock)
    eq_(len(indexed_chords), 3)
    eq_(indexed_chords[0].line, 0)
    eq_(indexed_chords[0].position, 0)
    eq_(indexed_chords[0].chord, sentinels.chord00)
    eq_(indexed_chords[1].line, 0)
    eq_(indexed_chords[1].position, 1)
    eq_(indexed_chords[1].chord, sentinels.chord01)
    eq_(indexed_chords[2].line, 3)
    eq_(indexed_chords[2].position, 0)
    eq_(indexed_chords[2].chord, sentinels.chord30)


class RenderStateMoveLyricsTests(TestCase):
    def setUp(self):
        lines = Mock()
        lines.__len__ = Mock(return_value=100)
        self.state = mock_nt(
            RenderState,
            tablature=MockTablature(
                lines=lines
            ),
            lyrics_position=0,
            screen_height=20,
        )

    def test_simple_move(self):
        state = self.state.move_lyrics(1)
        eq_(state.lyrics_position, 1)

    def test_negative_move_is_in_range(self):
        state = self.state.move_lyrics(-1)
        eq_(state.lyrics_position, 0)

    def test_out_of_screen_move_is_in_range(self):
        state = self.state.move_lyrics(100)
        eq_(state.lyrics_position, 80)

    def test_big_screen_move_is_in_range(self):
        state = self.state._replace(screen_height=120)
        state = state.move_lyrics(-1)
        eq_(state.lyrics_position, 0)
        state = state.move_lyrics(1)
        eq_(state.lyrics_position, 0)


class WrapGetTests(TestCase):
    def setUp(self):
        self.sentinels = Sentinels()
        self.array = [self.sentinels.first, self.sentinels.second,
                      self.sentinels.third]

    def test_normal_lookup(self):
        eq_(wrap_get(self.array, 0), self.sentinels.first)
        eq_(wrap_get(self.array, 1), self.sentinels.second)
        eq_(wrap_get(self.array, 2), self.sentinels.third)

    def test_negative_in_range_lookup(self):
        eq_(wrap_get(self.array, -3), self.sentinels.first)
        eq_(wrap_get(self.array, -2), self.sentinels.second)
        eq_(wrap_get(self.array, -1), self.sentinels.third)

    def test_negative_wrapping_lookup(self):
        eq_(wrap_get(self.array, -6), self.sentinels.first)
        eq_(wrap_get(self.array, -5), self.sentinels.second)
        eq_(wrap_get(self.array, -4), self.sentinels.third)

    def test_wrapping_lookup(self):
        eq_(wrap_get(self.array, 3), self.sentinels.first)
        eq_(wrap_get(self.array, 4), self.sentinels.second)
        eq_(wrap_get(self.array, 5), self.sentinels.third)


@patch('chorddb.curses.state.wrap_get')
def test_renderstate_current_chord(mock_wrap_get):
    sentinels = Sentinels()
    mock_wrap_get.return_value = sentinels.current_chord

    current_chord = mock_nt(
        RenderState,
        indexed_chords=sentinels.indexed_chords,
        current_chord_index=sentinels.current_chord_index
    ).current_indexed_chord()

    eq_(current_chord, sentinels.current_chord)
    mock_wrap_get.assert_called_once_with(sentinels.indexed_chords,
                                          sentinels.current_chord_index)

