#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import curses
import logging

from .color import DEFAULT_COLOR, CHORD_COLOR, FINGERING_COLOR, init_colors
from .state import RenderState


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


CursesBlit = collections.namedtuple('CursesBlit', ['xpos', 'ypos', 'text',
                                                   'color', 'attr'])


def render_tablature(tablature, instrument):
    from . import wrapper
    wrapper(lambda s: _render(s, tablature, instrument))


def _render(screen, tablature, instrument):
    init_colors()
    lyrics_pad = screen.subpad(0, 0, screen.width, len(tablature.lines),
                               screen.width, screen.height)
    state = RenderState.initial_state(tablature, instrument, screen)
    while state.running:
        lyrics_pad.clear()
        blits = []
        for line_index, line in enumerate(tablature.lines):
            current_chord = state.current_indexed_chord()
            selected_chords = ({current_chord.position}
                               if current_chord.line == line_index
                               else {})
            blits.extend(_get_line_blits(line, line_index, state, selected_chords))
        lyrics_pad.write_all(blits)
        screen.refresh()
        lyrics_pad.refresh(state.lyrics_position)
        key = screen.get_input_key()
        logging.debug("Got key: '%s'", key)
        state = _process_input_key(key, state)
    logging.info("Im freeeee")


def _process_input_key(key, state):
    if key == ord('q'):
        state = state._replace(running=False)
    elif key == curses.KEY_DOWN:
        state = state.move_lyrics(1)
    elif key == curses.KEY_UP:
        state = state.move_lyrics(-1)
    elif key == ord('b'):
        state = state.move_current_chord(-1)
    elif key == ord('n'):
        state = state.move_current_chord(1)
    elif key == ord('j'):
        state = state.move_current_chord_version(-1)
    elif key == ord('k'):
        state = state.move_current_chord_version(1)
    return state


def _get_line_blits(line, ypos, state, selected_chord_indexes={}):
    res = []
    if line.type == 'lyric':
        res.append(CursesBlit(
            xpos=0,
            ypos=ypos,
            text=line.data.lyrics,
            color=DEFAULT_COLOR,
            attr=0,
        ))
    elif line.type == 'chord':
        position = 0
        for index, (chord_position, chord) in enumerate(line.data.chords):
            attr = (curses.A_STANDOUT | curses.A_BOLD
                    if index in selected_chord_indexes
                    else 0)
            this_pos = max(position, chord_position)
            res.append(CursesBlit(
                xpos=this_pos,
                ypos=ypos,
                text=chord.text(),
                color=CHORD_COLOR,
                attr=attr,
            ))
            position = this_pos + len(chord.text())
            version = state.get_chord_version(chord)
            if version:
                text = "({})".format(version)
                res.append(CursesBlit(
                    xpos=position,
                    ypos=ypos,
                    text=text,
                    color=FINGERING_COLOR,
                    attr=attr,
                ))
                position += len(text)
            position += 1
    return res

