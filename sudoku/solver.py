"""
sudoku.solver
Solver class definition.
"""

# project imports
from sudoku.board import Board


class Move(object):

    def __init__(self):
        self.x = -1
        self.y = -1
        self.val = 0


class Solver(object):
    """
    Class that implements backtrack. See the backtrack method for details.
    """

    def __init__(self, puzzle, slow):
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
        self.slow = slow
        self.board = Board.factory(puzzle, slow)
        self.moves = [Move() for i in xrange(81)]

    def backtrack(self, k=-1):
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
        self.finished = True
        if not self.slow:
            self.board.refresh()

    def _construct_candidates(self, k):
        """
        Find an empty cell by calling the _next_square method. Assign the cell
        to the next move and return a list of possible values.
        """
        x, y = self._next_square()
        if x < 0 or y < 0:
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
        next_x = -1
        next_y = -1
        nconstraints = -1
        for x in xrange(9):
            for y in xrange(9):
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
        self.iteration += 1
        self.board.set(self.moves[k].x, self.moves[k].y, self.moves[k].val)

    def _unmake_move(self, k):
        """
        Undo the current move.
        """
        self.iteration += 1
        self.board.unset(self.moves[k].x, self.moves[k].y, self.moves[k].val)
