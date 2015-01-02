#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from nose.tools import eq_

from chorddb.instrument import Instrument
from chorddb.notes import KeyOctave


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def basic_capo_test():
    """ Basic check for `Instrument.capo` """
    capo_position = 2
    keyoctaves = [KeyOctave.parse(x + "0") for x in "ABCDEFG"]
    transposed = [ko.transpose(capo_position) for ko in keyoctaves]
    with_bass = Instrument(keyoctaves, 30, True)
    without_bass = Instrument(keyoctaves, 30, False)
    for original in [with_bass, without_bass]:
        capoed = original.capo(capo_position)
        eq_(capoed.has_bass, original.has_bass)
        eq_(capoed.keyoctaves, transposed)

