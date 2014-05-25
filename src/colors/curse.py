import curses


class CursesColors(object):
    CURSES_DEFAULT_COLOR = 0
    CURSES_CHORD_COLOR = 1
    CURSES_FINGERING_COLOR = 2

    _INITED = False

    _COLORS_DEFINITIONS = {
        CURSES_CHORD_COLOR: [curses.COLOR_CYAN, curses.COLOR_BLACK],
        CURSES_FINGERING_COLOR: [curses.COLOR_RED, curses.COLOR_BLACK],
    }

    @classmethod
    def init(cls):
        if not cls._INITED:
            for color_id, color_pair in cls._COLORS_DEFINITIONS.items():
                curses.init_pair(color_id, color_pair[0], color_pair[1])
            cls._INITED = True
