"""
sudoku.board
Board class definition.
"""

# system imports
import re

# project imports
from sudoku.display import Display


class Board(object):
    """
    Class to enforce the Sudoku rules. The rules are maintained through 3 groups
    of sets:
      1. Set of values in each row.
      2. Set of values in each column.
      3. Set of values in each sector (the 3x3 square).
    """

    _all_values = set(xrange(1, 10))

    @classmethod
    def factory(cls, puzzle, slow):
        """
        Factory method to create a Board object from a puzzle file.
        """
        board = cls(slow)
        rowregex = re.compile(r'([1-9 ])' * 9 + r'$')
        if puzzle:
            i = 0
            for row in puzzle:
                if i > 8:
                    raise SyntaxError("too many rows")
                m = rowregex.match(row)
                if not m:
                    raise SyntaxError("invalid row: %s" % row)
                for j in xrange(9):
                    v = m.group(j+1)
                    if v == ' ':
                        continue
                    board.set(i, j, int(v), loading=True)
                i += 1
            if i < 9:
                raise SyntaxError("not enough rows")
        board.refresh()
        return board

    def __init__(self, slow):
        """
        Constructor for the Board class. The following members are created here:
          1. m: the Sudoku board.
          2. freecount: number of cells with no value.
          3. rowsets: group of sets for values in each row.
          4. colsets: group of sets for values in each column.
          5. secsets: group of sets for values in each sector.
        """
        self.display = Display(slow)
        self.m = [[0]*9 for i in xrange(9)]
        self.freecount = 81
        self.rowsets = [set() for i in xrange(9)]
        self.colsets = [set() for i in xrange(9)]
        self.secsets = [set() for i in xrange(9)]

    def set(self, x, y, val, loading=False, display=True):
        """
        Set a cell. The loading flag is True when reading values from the puzzle
        file. It checks the inputs and disables refresh in the display. It also
        forces values to be displayed in bold.
        """
        assert 0 <= x and x < 9 and 0 <= y and y < 9 and self.freecount > 0 \
               and 1 <= val and val <= 9 and self.m[x][y] == 0
        if loading:
            if val in self.rowsets[x]:
                raise RuntimeError("duplicate %d in row %d, found in column "
                                   "%d" % (val, x+1, y+1))
            if val in self.colsets[y]:
                raise RuntimeError("duplicate %d in column %d, found in row "
                                   "%d" % (val, y+1, x+1))
            if val in self.secsets[self._rowcol_to_sector(x, y)]:
                raise RuntimeError("duplicate %d in sector %d, found in row "
                                   "%d/column %d" %
                                   (val, self._rowcol_to_sector(x, y)+1, x+1,
                                    y+1))
        self.m[x][y] = val
        self.freecount -= 1
        self.rowsets[x].add(val) 
        self.colsets[y].add(val)
        self.secsets[self._rowcol_to_sector(x, y)].add(val)
        if display:
            self.display.set(x, y, val, loading=loading)

    def unset(self, x, y, val, display=True):
        """
        Unset a cell.
        """
        assert 0 <= x and x < 9 and 0 <= y and y < 9 \
               and self.freecount < 81 and self.m[x][y] == val
        self.m[x][y] = 0
        self.freecount += 1
        self.rowsets[x].remove(val)
        self.colsets[y].remove(val)
        self.secsets[self._rowcol_to_sector(x, y)].remove(val)
        if display:
            self.display.set(x, y, 0)

    def get_num_constraints(self, x, y):
        """
        Return the number of values that are unavailable for a cell.
        """
        return len(self.rowsets[x] | self.colsets[y] |
                   self.secsets[self._rowcol_to_sector(x, y)])

    def get_possible_values(self, x, y):
        """
        Return the allowed values for a cell.
        """
        return self._all_values - self.rowsets[x] - self.colsets[y] - \
               self.secsets[self._rowcol_to_sector(x, y)]

    def look_ahead(self, x, y, val):
        """
        Test a value. Check that setting the value will have solutions in all
        remaining open cells.
        """
        self.set(x, y, val, display=False)
        try:
            for xx in xrange(9):
                for yy in xrange(9):
                    if self.m[xx][yy] != 0:
                        continue
                    if len(self.get_possible_values(xx, yy)) == 0:
                        return False
        finally:
            self.unset(x, y, val, display=False)
        return True

    @staticmethod
    def _rowcol_to_sector(x, y):
        return 3 * (x / 3) + y / 3

    def refresh(self):
        self.display.refresh()
