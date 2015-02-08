#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import curses
import logging

from .pad import CursesPad


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class CursesScreen(object):
    def __init__(self, screen):
        self._screen = screen

    def get_dimensions(self):
        size_y, size_x = self._screen.getmaxyx()
        return size_x, size_y

    @property
    def width(self):
        return self.get_dimensions()[0]

    @property
    def height(self):
        return self.get_dimensions()[1]

    def write(self, xpos, ypos, text, color, attr=0):
        if not 0 <= ypos < self.height:
            logger.warning("Writing outside screen: ypos=%s not in [0,%s)]",
                           ypos, self.height)
            return
        if xpos >= self.width:
            logger.warning("Writing outside screen: xpos=%s > width=%s",
                           xpos, self.width)
            return
        if xpos < 0:
            logger.warning("Writing outside screen: xpos=%s < 0", xpos)
            text = text[abs(xpos):]
            xpos = 0
        if xpos + len(text) > self.width:
            logger.warning("Writing outside screen: text '%s' is too large "
                           "(len=%s + xpos=%s > width=%s)", text, len(text),
                           xpos, self.width)
            text = text[:self.width - xpos]
        self._screen.addstr(ypos, xpos, text, curses.color_pair(color) | attr)

    def write_all(self, blits):
        for blit in blits:
            self.write(blit.xpos, blit.ypos, blit.text, blit.color, blit.attr)

    def clear(self):
        self._screen.clear()

    def refresh(self):
        self._screen.refresh()

    def get_input_key(self):
        return self._screen.getch()

    def subpad(self, xpos, ypos, width, height, display_width=None,
               display_height=None):
        display_width = display_width or width
        display_height = display_height or height
        if xpos < 0:
            raise ValueError("xpos must be non-negative")
        if ypos < 0:
            raise ValueError("ypos must be non-negative")
        if width <= 0:
            raise ValueError("width must be positive")
        if height <= 0:
            raise ValueError("height must be positive")
        if xpos + display_width > self.width:
            logger.warning("Creating out of bounds pad: xpos=%s + "
                           "display_width=%s > %s", xpos, display_width,
                           self.width)
            display_width -= self.width - xpos
        if ypos + display_height > self.height:
            logger.warning("Creating out of bounds pad: xpos=%s + "
                           "display_height=%s > %s", xpos, display_height,
                           self.height)
            display_height -= self.height - ypos

        return CursesPad(
            # Extra 1 width, because fuck you curses, thats why
            curses.newpad(height, width + 1),
            xpos,
            ypos,
            width,
            height,
            display_width,
            display_height,
        )
