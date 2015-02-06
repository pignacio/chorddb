#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import logging

from ..chords.library import ChordLibrary


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _get_chord_versions(chords, instrument):
    library = ChordLibrary(instrument)
    return {
        c: library.get_all(c) for c in chords
    }


def _wrap_get(array, index):
    return array[index % len(array)]


IndexedChord = collections.namedtuple('IndexedChord', ['line', 'position',
                                                       'chord'])


def _get_indexed_chords(tablature):
    chords = []
    for line_index, line in enumerate(tablature.lines):
        if line.type == 'chord':
            for chord_index, chord in enumerate(line.data.chords):
                chords.append(IndexedChord(
                    line=line_index, position=chord_index, chord=chord.chord))
    return chords


_RenderState = collections.namedtuple('RenderState', [
    'tablature',
    'instrument',
    'running',
    'screen_width',
    'screen_height',
    'lyrics_position',
    'indexed_chords',
    'current_chord_index',
    'chord_versions',
    'current_chord_version_index',
    'chord_drawing_is_reversed',
])


class RenderState(_RenderState):
    def move_lyrics(self, interval):
        new_position = self.lyrics_position + interval
        return self._replace(
            lyrics_position=self._to_lyrics_position_range(new_position))

    def move_current_chord(self, interval):
        new_chord_index = self.current_chord_index + interval
        return self._replace(current_chord_index=new_chord_index)

    def move_current_chord_version(self, interval):
        current_chord = self.current_indexed_chord().chord
        current_version = dict(self.current_chord_version_index)
        current_version[current_chord] += interval
        return self._replace(current_chord_version_index=current_version)

    def _to_lyrics_position_range(self, lyrics_position):
        # max_position might be negative
        max_position = len(self.tablature.lines) - self.screen_height
        if lyrics_position > max_position:
            lyrics_position = max_position
        if lyrics_position < 0:  # No elif. Fixes the case max_position < 0
            lyrics_position = 0
        return lyrics_position

    def reverse_chord_drawing(self):
        return self._replace(
            chord_drawing_is_reversed=not self.chord_drawing_is_reversed)

    def center_lyrics_line(self, line_index):
        new_position = self._to_lyrics_position_range(
            line_index - self.screen_height / 2)
        return self._replace(lyrics_position=new_position)

    def current_indexed_chord(self):
        return _wrap_get(self.indexed_chords, self.current_chord_index)

    def get_chord_version(self, chord):
        versions = self.chord_versions.get(chord, [])
        return (_wrap_get(versions, self.current_chord_version_index[chord])
                if versions else None)

    @classmethod
    def initial_state(cls, tablature, instrument, screen):
        indexed_chords = _get_indexed_chords(tablature)
        chord_versions = _get_chord_versions(
            set(c.chord for c in indexed_chords), instrument)
        return cls(
            lyrics_position=0,
            current_chord_index=0,
            running=True,
            tablature=tablature,
            instrument=instrument,
            indexed_chords=indexed_chords,
            screen_width=screen.width,
            screen_height=screen.height,
            chord_versions=chord_versions,
            current_chord_version_index=collections.defaultdict(int),
            chord_drawing_is_reversed=False,
        )
