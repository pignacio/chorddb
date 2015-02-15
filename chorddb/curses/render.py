#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import curses
import logging

from .color import DEFAULT_COLOR, CHORD_COLOR, FINGERING_COLOR, init_colors
from .state import RenderState
from .chord_drawer import draw_chord


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


CursesBlit = collections.namedtuple('CursesBlit', ['xpos', 'ypos', 'text',
                                                   'color', 'attr'])


def render_tablature(tablature, instrument):
    from . import wrapper
    wrapper(lambda s: _render(s, tablature, instrument))


def _render(screen, tablature, instrument):
    init_colors()
    chordpad_width, chordpad_height = _get_chordpad_dimensions(screen)
    vertical_division = screen.width - chordpad_width

    lyrics_pad = screen.subpad(
        0, 0,
        vertical_division - 1, len(tablature.lines),
        display_height=screen.height
    )
    chord_pad = screen.subpad(
        vertical_division + 1, 0,  # + 1 for left margin
        chordpad_width - 1, chordpad_height,  # -1 because of left margin
    )
    instructions_pad = screen.subpad(
        vertical_division + 1, chordpad_height + 2,  # +1/+2 for left/top margin
        chordpad_width - 1,  # -1 because of top margin
        screen.height - chordpad_height - 2,  # -2 because of left margin
    )

    state = RenderState.initial_state(tablature, instrument, screen)
    while state.running:
        screen.write_all(_get_division_blits(vertical_division, chordpad_width,
                                             chordpad_height, state))
        _update_lyrics_pad(lyrics_pad, state)
        _update_instructions_pad(instructions_pad, state)
        _update_chord_pad(chord_pad, state)
        screen.refresh()
        lyrics_pad.refresh(state.lyrics_position)
        instructions_pad.refresh()
        chord_pad.refresh()
        key = screen.get_input_key()
        logging.debug("Got key: '%s'", key)
        state = _process_input_key(key, state)
    logging.info("Im freeeee")


def _get_chordpad_dimensions(screen):
    width = min(36, screen.width / 2)
    height = min(15, screen.height / 2)
    return width, height


def _get_division_blits(vertical_division, chordpad_width, chordpad_height,
                        state):
    for ypos in xrange(0, state.screen_height):
        size = chordpad_width + 1 if ypos == chordpad_height else 1
        yield CursesBlit(
            xpos=vertical_division - 1,
            ypos=ypos,
            text="X" * size,
            color=DEFAULT_COLOR,
            attr=0,
        )


def _update_chord_pad(chord_pad, state):
    chord_pad.clear()
    chord = state.current_indexed_chord().chord
    version = state.get_chord_version(chord)
    version_count = len(state.chord_versions.get(chord, []))
    version_index = state.current_chord_version_index[chord] % version_count + 1
    if version:
        chord_pad.write(0, 0, "{} ({})".format(chord, version), DEFAULT_COLOR)
        chord_pad.write(0, 1, "Version {} of {}".format(version_index,
                                                        version_count),
                        DEFAULT_COLOR)
        lines = draw_chord(version, reverse=state.chord_drawing_is_reversed)
        for line_index, line in enumerate(lines):
            chord_pad.write(0, line_index + 3, line, DEFAULT_COLOR)
            to_paint = ((i, c) for (i, c) in enumerate(line) if c in "xo")
            for index, char in to_paint:
                chord_pad.write(index, line_index + 3, char, FINGERING_COLOR,
                                attr=curses.A_BOLD)
    else:
        chord_pad.write(0, 0, "{}".format(chord), DEFAULT_COLOR)
        chord_pad.write(0, 2, "No fingering available :'(", DEFAULT_COLOR)

def _update_instructions_pad(instructions_pad, dummy_state):
    for line_index, line in enumerate(INSTRUCTIONS):
        instructions_pad.write(0, line_index, line, DEFAULT_COLOR)


def _update_lyrics_pad(lyrics_pad, state):
    lyrics_pad.clear()
    blits = []
    for line_index, line in enumerate(state.tablature.lines):
        current_chord = state.current_indexed_chord()
        selected_chords = ({current_chord.position}
                           if current_chord.line == line_index
                           else {})
        blits.extend(_get_line_blits(line, line_index, state, selected_chords))
    lyrics_pad.write_all(blits)


def _center_at_current_chord(state):
    chord = state.current_indexed_chord()
    return state.center_lyrics_line(chord.line)


def _process_input_key(key, state):
    if key == ord('q'):
        state = state._replace(running=False)
    elif key == curses.KEY_DOWN:
        state = state.move_lyrics(1)
    elif key == curses.KEY_UP:
        state = state.move_lyrics(-1)
    elif key == ord('j'):
        state = state.move_current_chord(-1)
        state = _center_at_current_chord(state)
    elif key == ord('k'):
        state = state.move_current_chord(1)
        state = _center_at_current_chord(state)
    elif key == ord('h'):
        state = state.move_current_chord_version(-1)
    elif key == ord('l'):
        state = state.move_current_chord_version(1)
    elif key == ord('r'):
        state = state.reverse_chord_drawing()
    return state


def _get_line_blits(line, ypos, state, selected_chord_indexes=None):
    selected_chord_indexes = selected_chord_indexes or {}
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


INSTRUCTIONS = """
 INSTRUCTIONS/KEYBINDINGS


 k - move to next chord in song
 j - move to previous chord in song
 l - move to next current chord
     version
 h - move to previous current chord
     version
 up/down - navigate
 q - quit
 r - reverse chord orientation
""".strip().splitlines()
