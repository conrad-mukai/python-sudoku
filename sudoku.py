# program for solving sudoku using backtrack

# system imports
import sys
import os
import re
import argparse

# project imports
from board import Board

# globals
_args = None
finished = False
_iteration = 0


def main(argv=sys.argv):
    try:
        _parse_cmdline(argv)
        board = _parse_file()
        board.display('PUZZLE')
        if _args.verbose:
            sys.stdout.write('\n')
        a = [0] * 82
        backtrack(a, 0, board)
    except SystemExit, e:
        return e
    except Exception, e:
        if _args.traceback:
            import traceback
            traceback.print_exc()
        else:
            sys.stderr.write("[error]: %s\n" % e)
        return 1
    return 0


def _parse_cmdline(argv):
    global _args
    parser = argparse.ArgumentParser(description="Sudoku puzzle solver.")
    parser.add_argument('-r', '--rating', action='store_true',
                        help="provide difficulty rating of puzzle")
    parser.add_argument('-t', '--traceback', action='store_true',
                        help="display call stack when exceptions are raised")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="run in verbose mode, show solution progress")
    parser.add_argument('puzzle', type=file, help="puzzle file")
    _args = parser.parse_args(argv[1:])


def _parse_file():
    rowregex = re.compile(r'([1-9 ])'*9 + r'$')
    board = Board()
    i = 1
    for row in _args.puzzle:
        if i > 9:
            raise SyntaxError("too many rows")
        m = rowregex.match(row)
        if not m:
            raise SyntaxError("invalid row: %s" % row)
        for j in range(1, 10):
            v = m.group(j)
            if v == ' ':
                continue
            board.set(i, j, int(v), check=True)
        i += 1
    if i < 10:
        raise SyntaxError("not enough rows")
    return board


def backtrack(a, k, board):
    if is_a_solution(a, k, board):
        process_solution(a, k, board)
    else:
        c = [0] * 9
        k += 1
        ncandidates = construct_candidates(a, k, board, c)
        for i in range(ncandidates):
            a[k] = c[i]
            make_move(a, k, board)
            backtrack(a, k, board)
            unmake_move(a, k, board)
            if finished:
                return


def is_a_solution(a, k, board):
    global _iteration
    _iteration += 1
    return board.freecount == 0


def process_solution(a, k, board):
    global finished
    board.display('SOLUTION')
    if _args.rating:
        sys.stdout.write("\nRATING: %d\n" % _iteration)
    finished = True


def construct_candidates(a, k, board, c):
    possible = [False] * 10
    x, y = next_square(board)
    if x == 0 and y == 0:
        raise RuntimeError("no moves possible")
    board.move[k].x = x
    board.move[k].y = y
    ncandidates = 0
    possible_values(x, y, board, possible)
    for i in range(1, 10):
        if possible[i]:
            c[ncandidates] = i
            ncandidates = ncandidates + 1
    return ncandidates


def next_square(board):
    next_x = 0
    next_y = 0
    nconstraints = 0
    for x in range(1, 10): 
        for y in range(1, 10):
            if board.m[x][y] != 0:
                continue
            xy_constraints = board.get_num_constraints(x, y)
            if xy_constraints > nconstraints:
                nconstraints = xy_constraints
                next_x = x
                next_y = y
    return next_x, next_y


def possible_values(x, y, board, possible):
    for i in board.get_possible_values(x, y):
        if not board.look_ahead(x, y, i):
            continue
        possible[i] = True


def make_move(a, k, board):
    if _args.verbose:
        sys.stdout.write("iteration: %d, k: %d, x: %d, y: %d, value: %d\n" %
                         (_iteration, k, board.move[k].x, board.move[k].y,
                          a[k]))
    board.set(board.move[k].x, board.move[k].y, a[k])


def unmake_move(a, k, board):
    board.unset(board.move[k].x, board.move[k].y, a[k])


if __name__ == '__main__':
    sys.exit(main())
