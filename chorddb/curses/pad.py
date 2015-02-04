#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import curses
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class CursesPad(object):
    def __init__(self, pad, xpos, ypos, width, height, display_width=None,
                 display_height=None):
        self._pad = pad
        self._xpos = xpos
        self._ypos = ypos
        self._width = width
        self._height = height
        self._display_width = display_width or width
        self._display_height = display_height or height
        logger.info("Creating new pad(%s) @%sx%s, size=%sx%s, display=%sx%s",
                    hex(id(self)), xpos, ypos, width, height,
                    self._display_width, self._display_height)

    def write(self, xpos, ypos, text, color, attr=0):
        if not 0 <= ypos < self.height:
            logger.warning("Writing outside pad: ypos=%s not in [0,%s)]",
                           ypos, self.height)
            return
        if xpos >= self.width:
            logger.warning("Writing outside pad: xpos=%s > width=%s",
                           xpos, self.width)
            return
        if xpos < 0:
            logger.warning("Writing outside pad: xpos=%s < 0", xpos)
            text = text[abs(xpos):]
            xpos = 0
        if xpos + len(text) > self.width:
            logger.warning("Writing outside pad: text '%s' is too large "
                           "(len=%s + xpos=%s > width=%s)", text, len(text),
                           xpos, self.width)
            text = text[:self.width - xpos]
        self._write(xpos, ypos, text, color, attr)

    def _write(self, xpos, ypos, text, color, attr=0):
        logger.debug("pad(%s):addstr@%sx%s '%s' color=%s, attr=%s",
                     hex(id(self)), xpos, ypos, text, color, attr)
        self._pad.addstr(ypos, xpos, text, curses.color_pair(color) | attr)

    def write_all(self, blits):
        for blit in blits:
            self.write(blit.xpos, blit.ypos, blit.text, blit.color, blit.attr)

    def clear(self):
        self._pad.clear()

    def refresh(self, vertical_scroll=0):
        self._pad.refresh(vertical_scroll, 0,
                          self._ypos, self._xpos,
                          self._ypos + self._display_height - 1,
                          self._xpos + self._display_width - 1)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
