from __future__ import absolute_import

from argparse import ArgumentParser
import curses
import logging
import os

from . import colors
from .tab import Tablature, TerminalRenderer
from .window import CursesRenderer
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
    parser.add_argument("--curses",
                        action='store_true', dest='use_curses', default=False,
                        help="Use curses to show tablature")
    parser.set_defaults(func=_parse_tablature)


def _parse_tablature(filename, instrument, use_curses):
    if not os.path.isfile(filename):
        raise ValueError("'{}' is not a valid file".format(filename))
    instrument = Instrument.from_name(instrument, UKELELE)
    tab = Tablature.parse(open(filename).readlines())
    if use_curses:
        render = lambda s: _render_tablature_with_curses(s, tab, instrument)
        curses.wrapper(render)
    else:
        TerminalRenderer().render(tab, instrument)


def _render_tablature_with_curses(stdscr, tab, instrument):
    colors.curse.init()
    CursesRenderer(stdscr, tab, instrument).run()


def _extract_from_options(key, options):
    res = getattr(options, key)
    delattr(options, key)
    return res


def main():
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = _get_arg_parser()
    options = parser.parse_args()

    subparser = _extract_from_options("subparser", options)

    try:
        func = _extract_from_options("func", options)
    except AttributeError:
        raise Exception("Missing 'func' attribute. Maybe subparser '{}' didnt "
                        "correctly set_defaults()?".format(subparser))

    func(**options.__dict__)

if __name__ == "__main__":
    main()
