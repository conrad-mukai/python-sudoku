"""
lib.solver
Solver class definition.
"""

# system imports
import sys

# project imports
from lib.board import Board


class Move(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.val = 0


class Solver(object):
    """
    Class that implements backtrack. See the backtrack method for details.
    """

    def __init__(self, puzzle, verbose=False, rating=False):
        """
        Constructor for the Solver class. The key members of this class are:
          finished: Flag to track if solution is found.
          board: Board object. This enforces the rules of Sudoku.
          moves: Track what moves have been tried so that they can be rolled
                 back.
        The remaining members support display options.
        """
        self.iteration = 0
        self.finished = False
        self.verbose = verbose
        self.rating = rating
        self.board = Board.factory(puzzle)
        self.moves = [Move() for i in xrange(82)]

    def backtrack(self, k):
        """
        The backtrack algorithm. This is a recursive algorithm. The algorithm
        does the following:
          1. Selects a series of candidate solutions. The candidate solutions
             are the possible values for some empty cell in the Sudoku board.
          2. Each value is assigned and backtrack is recursively called.
          3. If there is no solution upon return from backtrack the trial
             solution is undone and the next candidate is tried.
        If the end condition is met (see the _is_a_solution method), the
        _process_solution method is called. This will set the finished flag to
        terminate the recursion.
        """
        if self._is_a_solution():
            self._process_solution()
        else:
            self.iteration += 1
            k += 1
            candidates = self._construct_candidates(k)
            for val in candidates:
                self.moves[k].val = val
                self._make_move(k)
                self.backtrack(k)
                if self.finished:
                    return
                self._unmake_move(k)

    def _is_a_solution(self):
        """
        Checks the Sudoku board to see if there are any more free cells.
        """
        return self.board.freecount == 0

    def _process_solution(self):
        """
        This is called when a solution has been found. This routine displays the
        solution and sets the finished flag to unwind the backtrack recursion.
        """
        self.board.display('SOLUTION')
        if self.rating:
            sys.stdout.write("\nRATING: %d\n" % self.iteration)
        self.finished = True

    def _construct_candidates(self, k):
        """
        Find an empty cell by calling the _next_square method. Assign the cell
        to the next move and return a list of possible values.
        """
        x, y = self._next_square()
        if x == 0 and y == 0:
            raise RuntimeError("no moves possible")
        self.moves[k].x = x
        self.moves[k].y = y
        return self._possible_values(x, y)

    def _next_square(self):
        """
        Find the next cell to try. All cells in the board are examined. The one
        returned is one with no assigned value and the least number of possible
        values (maximum number of constraints).
        """
        next_x = 0
        next_y = 0
        nconstraints = 0
        for x in xrange(1, 10):
            for y in xrange(1, 10):
                if self.board.m[x][y] != 0:
                    continue
                xy_constraints = self.board.get_num_constraints(x, y)
                if xy_constraints > nconstraints:
                    nconstraints = xy_constraints
                    next_x = x
                    next_y = y
        return next_x, next_y

    def _possible_values(self, x, y):
        """
        This is called by _construct_candidates to return all possible values
        for a cell. As an optimization, the look_ahead function is used to make
        sure that any value will not lead to failures.
        """
        return [val for val in self.board.get_possible_values(x, y)
                if self.board.look_ahead(x, y, val)]

    def _make_move(self, k):
        """
        Assign the current move to the Sudoku board.
        """
        if self.verbose:
            sys.stdout.write("try: iteration: %d, k: %d, x: %d, y: %d, "
                             "value: %d\n"
                             % (self.iteration, k, self.moves[k].x,
                                self.moves[k].y, self.moves[k].val))
        self.board.set(self.moves[k].x, self.moves[k].y, self.moves[k].val)

    def _unmake_move(self, k):
        """
        Undo the current move.
        """
        if self.verbose:
            sys.stdout.write("undo: iteration: %d, k: %d, x: %d, y: %d, "
                             "value: %d\n"
                             % (self.iteration, k, self.moves[k].x,
                                self.moves[k].y, self.moves[k].val))
        self.board.unset(self.moves[k].x, self.moves[k].y, self.moves[k].val)
