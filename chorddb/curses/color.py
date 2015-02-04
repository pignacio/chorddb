#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import curses
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


BOLD = curses.A_BOLD
STANDOUT = curses.A_STANDOUT

DEFAULT_COLOR = 0
CHORD_COLOR = 1
FINGERING_COLOR = 2

_COLORS_DEFINITIONS = {
    CHORD_COLOR: [curses.COLOR_CYAN, curses.COLOR_BLACK],
    FINGERING_COLOR: [curses.COLOR_RED, curses.COLOR_BLACK],
}


def init_colors():
    for color_id, color_pair in _COLORS_DEFINITIONS.items():
        curses.init_pair(color_id, color_pair[0], color_pair[1])
