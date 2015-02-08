import colorama
import collections
import StringIO

# colorama.init()


TerminalColor = collections.namedtuple('TerminalColor', ['fore', 'back'])


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

NULL = TerminalColor('', '')

STYLE_DIM = colorama.Style.DIM  # pylint: disable=no-member
STYLE_NORMAL = colorama.Style.NORMAL  # pylint: disable=no-member
STYLE_BRIGHT = colorama.Style.BRIGHT  # pylint: disable=no-member
RESET_ALL = colorama.Style.RESET_ALL  # pylint: disable=no-member


def colorize(text, fore=NULL, back=NULL, style=STYLE_NORMAL):
    res = StringIO.StringIO()
    # Apply style
    res.write("".join([x or '' for x in [fore.fore, back.back,
                                         style]]))

    # Write message
    res.write(text)

    # Reset style
    res.write("".join([WHITE.fore, BLACK.back, STYLE_NORMAL]))
    return res.getvalue()
