#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from StringIO import StringIO


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name



"""
    3
 ||-o-|---|---|---|
 ||-o-|---|---|---|
 ||---|-o-|---|---|
 ||---|---|-o-|---|
 ||---|---|-o-|---|
 ||-o-|---|---|---|

"""


def draw_chord(fingering, reverse=True):
    positions = fingering.positions
    try:
        start = min(p for p in positions if p)
    except ValueError:
        start = 1

    if start <= 2:
        start = 1

    end = max(p for p in positions) - start
    if end < 3:
        end = 3

    lines = []

    lines.append("         {}".format(start))

    keyoctaves = [ko.key for ko in fingering.instrument.keyoctaves]

    values = zip(fingering.full_positions(), keyoctaves)
    if reverse:
        values.reverse()

    for position, keyoctave in values:
        line = StringIO()
        char = 'o' if position == 0 else 'x' if position == 'x' else ' '
        line.write(_line_start(char, keyoctave))
        for fret in xrange(0, end + 1):
            line.write(_fret(position == fret + start))
        lines.append(line.getvalue())

    return lines


def _line_start(char, keyoctave):
    return " {:3} {}||".format(keyoctave.text(), char)


def _fret(touched):
    return "-{}-|".format("o" if touched else "-")
