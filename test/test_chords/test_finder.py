#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from nose.tools import ok_


from chorddb.instrument import GUITAR, UKELELE, LOOG
from chorddb.chords.finder import get_fingerings
from chorddb.chords import Chord
from chorddb.notes import Key


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


_TEST_VARIATIONS = [None, "m", "7", "m7"]


def _test_variation_has_fingerings(variation, instrument):
    chord = Chord(Key.parse("C"), variation=variation)
    ok_(len(get_fingerings(chord, instrument)) > 0,
        "Variation has no fingerings! variation={}, instrument={}".format(
            variation, instrument))


def test_variation_have_fingerings():
    for instrument in [GUITAR, UKELELE, LOOG]:
        for variation in _TEST_VARIATIONS:
            yield _test_variation_has_fingerings, variation, instrument


