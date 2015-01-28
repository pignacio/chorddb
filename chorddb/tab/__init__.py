'''
Created on May 10, 2014

@author: ignacio
'''
import collections
import logging
import re
import StringIO

from .parser import parse_tablature


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _transpose_line(line, interval):
    if line.type == 'chord':
        new_chords = [c._replace(chord=c.chord.transpose(interval))
                      for c in line.chords]
        return line._replace(chords=new_chords)
    else:
        return line

def transpose_tablature(tablature, interval):
    new_lines = [_transpose_line(line, interval) for line in tablature.lines]
    return tablature._replace(lines=new_lines)
