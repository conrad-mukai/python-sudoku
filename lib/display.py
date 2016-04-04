"""
lib.display
Curses based display class.
"""

# system imports
import curses


class Display(object):
    """
    Class for handling curses calls for displaying the Sudoku board.
    """

    height  = 13
    width   = 25
    bheight = 3
    bwidth  = 7

    def __init__(self, slow):
        self.slow = slow
        self._convert(1, 1)

    def set(self, x, y, val, loading=False):
        """
        Display a value in a cell. The inputs are in the coordinates of the
        Board class.
        """
        self._convert(x, y)
        if val == 0:
            ch = ' '
        else:
            ch = str(val)
        if loading:
            self.window.addch(self.x, self.y, ch, curses.A_BOLD)
        else:
            self.window.addch(self.x, self.y, ch)
            if self.slow:
                self.window.refresh()
                curses.napms(100)

    def _convert(self, x, y):
        """
        Convert from board coordinates to display coordinates.
        """
        self.x = x + (x - 1) / 3
        self.y = 2 * y + 2 * ((y - 1) / 3)

    def refresh(self):
        self.window.refresh()

    @classmethod
    def draw_screen(cls, stdscr):
        """
        Display the Sudoku frame.
        """
        cls.window = stdscr
        for x in xrange(cls.height):
            if x == 0:
                cls._draw_horizontal(x, curses.ACS_ULCORNER,
                                     curses.ACS_URCORNER, curses.ACS_TTEE)
            elif x == cls.height - 1:
                cls._draw_horizontal(x, curses.ACS_LLCORNER,
                                     curses.ACS_LRCORNER, curses.ACS_BTEE)
            elif x % (cls.bheight + 1) == 0:
                cls._draw_horizontal(x, curses.ACS_LTEE, curses.ACS_RTEE,
                                     curses.ACS_PLUS)
            else:
                cls._draw_horizontal(x, curses.ACS_VLINE, curses.ACS_VLINE,
                                     curses.ACS_VLINE, boundary=False)
        cls.window.refresh()

    @classmethod
    def _draw_horizontal(cls, x, lchar, rchar, mchar, boundary=True):
        """
        Drow one row of the framework
        """
        cls.window.addch(x, 0, lchar)
        cls.window.addch(x, cls.width - 1, rchar)
        for y in xrange(cls.bwidth + 1, cls.width - 1, cls.bwidth + 1):
            cls.window.addch(x, y, mchar)
        if boundary:
            for y in xrange(1, cls.width, cls.bwidth + 1):
                cls.window.hline(x, y, curses.ACS_HLINE, cls.bwidth)
