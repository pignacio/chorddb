import colorama
import StringIO

colorama.init()


class TerminalColor(object):
    def __init__(self, fore, back):
        self._fore = fore
        self._back = back

    @property
    def fore(self):
        return self._fore

    @property
    def back(self):
        return self._back


BLACK = TerminalColor(colorama.Fore.BLACK,  # pylint: disable=no-member
                      colorama.Back.BLACK)  # pylint: disable=no-member
RED = TerminalColor(colorama.Fore.RED,  # pylint: disable=no-member
                    colorama.Back.RED)  # pylint: disable=no-member
GREEN = TerminalColor(colorama.Fore.GREEN,  # pylint: disable=no-member
                      colorama.Back.GREEN)  # pylint: disable=no-member
YELLOW = TerminalColor(colorama.Fore.YELLOW,  # pylint: disable=no-member
                       colorama.Back.YELLOW)  # pylint: disable=no-member
BLUE = TerminalColor(colorama.Fore.BLUE,  # pylint: disable=no-member
                     colorama.Back.BLUE)  # pylint: disable=no-member
MAGENTA = TerminalColor(colorama.Fore.MAGENTA,  # pylint: disable=no-member
                        colorama.Back.MAGENTA)  # pylint: disable=no-member
CYAN = TerminalColor(colorama.Fore.CYAN,  # pylint: disable=no-member
                     colorama.Back.CYAN)  # pylint: disable=no-member
WHITE = TerminalColor(colorama.Fore.WHITE,  # pylint: disable=no-member
                      colorama.Back.WHITE)  # pylint: disable=no-member
RESET = TerminalColor(colorama.Fore.RESET,  # pylint: disable=no-member
                      colorama.Back.RESET)  # pylint: disable=no-member


DIM = colorama.Style.DIM  # pylint: disable=no-member
NORMAL = colorama.Style.NORMAL  # pylint: disable=no-member
BRIGHT = colorama.Style.BRIGHT  # pylint: disable=no-member
RESET_ALL = colorama.Style.RESET_ALL  # pylint: disable=no-member


class ColoredOutput(object):

    def __init__(self, fore=WHITE, back=BLACK, style=NORMAL):
        self._buffer = StringIO.StringIO()
        self._fore = self._back = self._style = None
        self.switch(fore, back, style)
        self._tell = 0

    def write(self, msg, fore=None, back=None, style=None):
        # Apply style
        self._reset()
        self._buffer.write("".join([x or '' for x in [fore, back, style]]))

        # Write message
        self._buffer.write(msg)
        self._tell += len(msg)

        # Reset style
        self._reset()

    def line(self, msg, fore=None, back=None, style=None):
        return self.write(msg + "\n", fore=fore, back=back, style=style)

    def switch(self, fore=None, back=None, style=None):
        self._fore = fore.fore if fore is not None else self._fore
        self._back = back.back if back is not None else self._back
        self._style = style if style is not None else self._style
        self._buffer.write("".join([self._fore, self._back, self._style]))

    def _reset(self):
        self._buffer.write("".join([self._fore, self._back, self._style]))

    def getvalue(self):
        self._buffer.write(RESET_ALL)
        return self._buffer.getvalue()

    def tell(self):
        """Does not count color characters"""
        return self._tell

    @classmethod
    def colored(cls, msg, fore=WHITE, back=BLACK,
                style=NORMAL):
        output = cls(fore=fore, back=back, style=style)
        output.write(msg)
        return output.getvalue()

