"""
lib.sudoku

CLI for the sudoku script. This module defines the following command line
syntax:

    Sudoku puzzle solver.

    positional arguments:
      puzzle           puzzle file

    optional arguments:
      -h, --help       show this help message and exit
      -r, --rating     provide difficulty rating of puzzle
      -t, --traceback  display call stack when exceptions are raised
      -v, --verbose    run in verbose mode, show solution progress

The lib.solver.Solver class is loaded and the backtrack method is called to
solve the puzzle in the input file.
"""

# system imports
import argparse
import sys

# project imports
from lib.solver import Solver


def main(argv=sys.argv):
    try:
        args = _parse_cmdline(argv)
        try:
            solver = Solver(args.puzzle, verbose=args.verbose,
                            rating=args.rating)
            solver.backtrack(0)
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
    parser.add_argument('-r', '--rating', action='store_true',
                        help="provide difficulty rating of puzzle")
    parser.add_argument('-t', '--traceback', action='store_true',
                        help="display call stack when exceptions are raised")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="run in verbose mode, show solution progress")
    parser.add_argument('puzzle', type=argparse.FileType('r'), help="puzzle file")
    return parser.parse_args(argv[1:])


def _close_args(args):
    args.puzzle.close()
