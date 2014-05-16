import logging
from tab import Tablature
from argparse import ArgumentParser
import os


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
    parser.set_defaults(func=_parse_tablature)


def _parse_tablature(filename, instrument):
    if not os.path.isfile(filename):
        raise ValueError("'{}' is not a valid file".format(filename))
    tab = Tablature.parse(open(filename).readlines())
    print tab.render(instrument=instrument)


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
        raise Exception(
            "Missing 'func' attribute. Maybe subparser '{}' didnt correctly set_defaults()?".format(subparser))

    func(**options.__dict__)

if __name__ == "__main__":
    main()
