#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


Tablature = collections.namedtuple('Tablature', ['lines'])
TabLine = collections.namedtuple('TabLine', ['type', 'data', 'original'])
ChordLineData = collections.namedtuple('ChordLineData', ['chords'])
LyricLineData = collections.namedtuple('LyricLineData', ['lyrics'])
TabChord = collections.namedtuple('TabChord', ['position', 'chord'])
