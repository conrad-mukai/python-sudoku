"""
lib.debug
Mocks for curses calls. This is for running the script in the debugger.
"""

# system imports
import curses


class MockCurses(object):

    def addch(self, *args, **kwargs):
        pass

    def addstr(self, *args, **kwargs):
        pass

    def hline(self, *args, **kwargs):
        pass

    def refresh(self):
        pass

    def getch(self):
        pass


def mock_curses():
    curses.napms = _mock_func
    curses.curs_set = _mock_func
    curses.nocbreak = _mock_func
    curses.echo = _mock_func
    curses.endwin = _mock_func
    curses.ACS_ULCORNER = 0
    curses.ACS_URCORNER = 0
    curses.ACS_TTEE = 0
    curses.ACS_HLINE = 0
    curses.ACS_LLCORNER = 0
    curses.ACS_LRCORNER = 0
    curses.ACS_BTEE = 0
    curses.ACS_LTEE = 0
    curses.ACS_RTEE = 0
    curses.ACS_PLUS = 0
    curses.ACS_VLINE = 0


def _mock_func(*args, **kwargs):
    pass
