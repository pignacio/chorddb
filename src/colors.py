'''
Created on May 11, 2014

@author: ignacio
'''
from colorama import Fore, Back, Style, init
import StringIO

class Bold():
    BOLD = '\033[1m'
    NOBOLD = ''

class ColoredOutput():
    __INIT = init()
    def __init__(self, fore=Fore.WHITE, back=Back.BLACK, style=Style.NORMAL, bold=Bold.NOBOLD):
        self._buffer = StringIO.StringIO()
        self.switch(fore, back, style, bold)
        self._tell = 0

    def write(self, msg, fore=None, back=None, style=None, bold=None):
        # Apply style
        self._reset()
        self._buffer.write("".join([x or '' for x in [fore, back, style, bold]]))

        # Write message
        self._buffer.write(msg)
        self._tell += len(msg)

        # Reset style
        self._reset()

    def line(self, msg, fore=None, back=None, style=None, bold=None):
        return self.write(msg + "\n", fore=fore, back=back, style=style, bold=bold)

    def switch(self, fore=None, back=None, style=None, bold=None):
        self._fore = fore if fore is not None else self._fore
        self._back = back if back is not None else self._back
        self._style = style if style is not None else self._style
        self._bold = bold if bold is not None else self._bold
        self._buffer.write("".join([self._fore, self._back, self._style, self._bold]))

    def _reset(self):
        self._buffer.write(Style.RESET_ALL)
        self._buffer.write("".join([self._fore, self._back, self._style, self._bold]))

    def getvalue(self):
        self._buffer.write(Style.RESET_ALL)
        return self._buffer.getvalue()

    def tell(self):
        """Does not count color characters"""
        return self._tell

    @classmethod
    def colored(cls, msg, fore=Fore.WHITE, back=Back.BLACK, style=Style.NORMAL, bold=Bold.NOBOLD):
        output = cls(fore=fore, back=back, style=style, bold=bold)
        output.write(msg)
        return output.getvalue()

