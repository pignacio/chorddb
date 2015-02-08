from __future__ import absolute_import

from argparse import ArgumentParser
import logging
import os

from . import terminal, curses
from .tab import parse_tablature, transpose_tablature
from .instrument import UKELELE, Instrument


def _get_arg_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')
    add_parsers(subparsers)
    return parser


def add_parsers(subparsers):
    parser = subparsers.add_parser("parse")
    parser.add_argument('filename',
                        help='file to parse tablature from')
    parser.add_argument('-i', '--instrument', action='store', default=None,
                        help='Instrument to fetch chords for')
    parser.add_argument('-t', '--transpose', action='store', type=int,
                        default=0, help=('Number of steps to transpose the tab.'
                                         ' Defaults to 0'))
    parser.add_argument('-c', '--capo', action='store', type=int, default=0,
                        help='Capo position for the instrument. Defaults to 0')
    parser.add_argument("--curses",
                        action='store_true', dest='use_curses', default=False,
                        help="Use curses to show tablature")
    parser.add_argument("--debug",
                        action="store_true", dest="debug", default=False,
                        help="Sets logging level to DEBUG")
    parser.set_defaults(func=_parse_tablature)


def _parse_tablature(filename, instrument, use_curses, transpose, capo):
    with open(filename) as fin:
        lines = fin.readlines()
    tablature = parse_tablature(lines)
    if transpose:
        tablature = transpose_tablature(tablature, transpose)
    instrument = Instrument.from_name(instrument, UKELELE)
    if capo:
        instrument = instrument.capo(capo)
    if use_curses:
        curses.render_tablature(tablature, instrument)
    else:
        terminal.render_tablature(tablature, instrument)


def _extract_from_options(key, options):
    res = getattr(options, key)
    delattr(options, key)
    return res


def main():
    parser = _get_arg_parser()
    options = parser.parse_args()

    logging.basicConfig(filename='chorddb.log', filemode="w",
                        level=(logging.DEBUG
                               if _extract_from_options("debug", options)
                               else logging.INFO))
    subparser = _extract_from_options("subparser", options)

    try:
        func = _extract_from_options("func", options)
    except AttributeError:
        raise Exception("Missing 'func' attribute. Maybe subparser '{}' didnt "
                        "correctly set_defaults()?".format(subparser))

    func(**options.__dict__)

if __name__ == "__main__":
    main()
