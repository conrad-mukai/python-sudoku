"""
lib.sudoku

CLI for the sudoku script. This module defines the following command line
syntax:

    usage: sudoku [-h] [-t] [puzzle]

    Sudoku puzzle solver.

    positional arguments:
      puzzle           puzzle file

    optional arguments:
      -h, --help       show this help message and exit
      -t, --traceback  display call stack when exceptions are raised

The lib.solver.Solver class is loaded and the backtrack method is called to
solve the puzzle in the input file.
"""

# system imports
import argparse
import sys

# project imports
from lib.solver import Solver
from lib.display import Display


def main(argv=sys.argv):
    try:
        args = _parse_cmdline(argv)
        try:
            Display.draw_screen(args.debug)
            try:
                _loop(args.puzzle, args.slow)
            finally:
                Display.close_screen()
        finally:
            _close_args(args)
    except SystemExit, e:
        return e
    except Exception, e:
        if 'args' in locals() and args.traceback:
            import traceback
            traceback.print_exc()
        else:
            sys.stderr.write("[error]: %s\n" % e)
        return 1
    return 0


def _parse_cmdline(argv):
    parser = argparse.ArgumentParser(description="Sudoku puzzle solver.")
    parser.add_argument('-s', '--slow', action='store_true',
                        help="slow mode: show puzzle being solved")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="don't use curses to run in a debugger")
    parser.add_argument('-t', '--traceback', action='store_true',
                        help="display call stack when exceptions are raised")
    parser.add_argument('puzzle', type=argparse.FileType('r'), nargs='?',
                        default=None, help="puzzle file")
    return parser.parse_args(argv[1:])


def _close_args(args):
    if args.puzzle:
        args.puzzle.close()


def _loop(puzzle, slow):
    solver = Solver(puzzle, slow)
    Display.prompt("press any key to continue")
    solver.backtrack(0)
    Display.prompt("%d iterations, press any key to exit" % solver.iteration)
