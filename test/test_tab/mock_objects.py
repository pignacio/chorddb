#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from ..utils import mock_namedtuple_class
from chorddb.tab.objects import (
    Tablature, TabLine, ChordLineData, LyricLineData, TabChord)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


MockTablature = mock_namedtuple_class(Tablature)  # pylint: disable=invalid-name
MockTabLine = mock_namedtuple_class(TabLine)  # pylint: disable=invalid-name
MockChordLineData = mock_namedtuple_class(ChordLineData)  # pylint: disable=invalid-name
MockLyricLineData = mock_namedtuple_class(LyricLineData)  # pylint: disable=invalid-name
MockTabChord = mock_namedtuple_class(TabChord)  # pylint: disable=invalid-name


