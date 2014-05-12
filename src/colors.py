'''
Created on May 11, 2014

@author: ignacio
'''
from colorama import Fore, Back, Style, init
import StringIO

class ColoredOutput():
    __INIT = init()
    def __init__(self, fore=Fore.WHITE, back=Back.BLACK, style=Style.NORMAL):
        self._buffer = StringIO.StringIO()
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
        self._fore = fore if fore is not None else self._fore
        self._back = back if back is not None else self._back
        self._style = style if style is not None else self._style
        self._buffer.write("".join([self._fore, self._back, self._style]))

    def _reset(self):
        self._buffer.write("".join([self._fore, self._back, self._style]))

    def getvalue(self):
        self._buffer.write(Style.RESET_ALL)
        return self._buffer.getvalue()

    def tell(self):
        """Does not count color characters"""
        return self._tell

    @classmethod
    def colored(cls, msg, fore=Fore.WHITE, back=Back.BLACK, style=Style.NORMAL):
        output = cls(fore=fore, back=back, style=style)
        output.write(msg)
        return output.getvalue()

