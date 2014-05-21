'''
Created on May 21, 2014

@author: ignacio
'''

import curses


class SubPad():
    def __init__(self, xpos, ypos, width, height):
        self._pad = curses.newpad(1000, 1000)
        self._xpos = xpos
        self._ypos = ypos
        self._width = width
        self._height = height

    def refresh(self):
        self._pad.refresh(0, 0,
                          self._ypos, self._xpos,
                          self._ypos + self._height - 1,
                          self._xpos + self._width - 1)

    @property
    def pad(self):
        return self._pad


class MainWindow():
    def __init__(self, curses_screen):
        self._curses_screen = curses_screen
        self._subpads = []
        width, height = self._get_screen_dimensions()
        chord_w, chord_h = self._get_chord_pad_dimensions()
        self._lyrics_pad = self._subpad(width - chord_w - 1, height, 0, 0)
        self._chord_pad = self._subpad(chord_w, chord_h, width - chord_w, 0)
        self._instruction_pad = self._subpad(chord_w, height - chord_h - 1,
                                             width - chord_w, chord_h + 1)
        self._draw_borders()

    def _get_screen_dimensions(self):
        height, width = self._curses_screen.getmaxyx()
        return width, height

    def _get_chord_pad_dimensions(self):
        width, height = self._get_screen_dimensions()
        pad_width = min(30, width / 2)
        pad_height = min(15, height / 2)
        return pad_width, pad_height

    def _subpad(self, width, height, xpos, ypos):
        subpad = SubPad(xpos, ypos, width, height)
        self._subpads.append(subpad)
        return subpad.pad

    def _draw_borders(self):
        width, height = self._get_screen_dimensions()
        chord_w, chord_h = self._get_chord_pad_dimensions()
        for ypos in xrange(height):
            xpos = width - chord_w - 1
            self._curses_screen.addstr(ypos, xpos, "x")
        for subxpos in xrange(chord_w):
            ypos = chord_h
            xpos = width - chord_w + subxpos
            self._curses_screen.addstr(ypos, xpos,
                                       "x")

    def refresh(self):
        self._curses_screen.refresh()
        for subpad in self._subpads:
            subpad.refresh()

    @property
    def lyrics_pad(self):
        return self._lyrics_pad

    @property
    def chord_pad(self):
        return self._chord_pad

    @property
    def instruction_pad(self):
        return self._instruction_pad
