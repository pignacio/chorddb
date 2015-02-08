#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import curses
import logging

from .render import render_tablature
from .screen import CursesScreen


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


__all__ = ['wrapper', 'render_tablature']


def wrapper(func):
    def func_wrap(curses_screen):
        screen = CursesScreen(curses_screen)
        try:
            return func(screen)
        except:
            logger.exception("Ooppps!")
            raise
    curses.wrapper(func_wrap)
