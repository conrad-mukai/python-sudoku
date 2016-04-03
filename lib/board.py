"""
lib.board
Board class definition.
"""

# system imports
import sys
import re


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
    def factory(cls, puzzle):
        """
        Factory method to create a Board object from a puzzle file.
        """
        rowregex = re.compile(r'([1-9 ])' * 9 + r'$')
        board = cls()
        i = 1
        for row in puzzle:
            if i > 9:
                raise SyntaxError("too many rows")
            m = rowregex.match(row)
            if not m:
                raise SyntaxError("invalid row: %s" % row)
            for j in xrange(1, 10):
                v = m.group(j)
                if v == ' ':
                    continue
                board.set(i, j, int(v), check=True)
            i += 1
        if i < 10:
            raise SyntaxError("not enough rows")
        board.display('PUZZLE')
        return board

    def __init__(self):
        """
        Constructor for the Board class. The following members are created here:
          1. m: the Sudoku board.
          2. freecount: number of cells with no value.
          3. rowsets: group of sets for values in each row.
          4. colsets: group of sets for values in each column.
          5. secsets: group of sets for values in each sector.
        """
        self.m = [[0]*10 for i in xrange(10)]
        self.freecount = 81
        self.rowsets = [set() for i in xrange(10)]
        self.colsets = [set() for i in xrange(10)]
        self.secsets = [set() for i in xrange(10)]

    def set(self, x, y, val, check=False):
        """
        Set a cell. The check flag is True when loading values from the puzzle
        file.
        """
        assert 1 <= x and x <= 9 and 1 <= y and y <= 9 and self.freecount > 0 \
               and 1 <= val and val <= 9 and self.m[x][y] == 0
        if check:
            if val in self.rowsets[x]:
                raise RuntimeError("duplicate %d in row %d, found in column "
                                   "%d" % (val, x, y))
            if val in self.colsets[y]:
                raise RuntimeError("duplicate %d in column %d, found in row "
                                   "%d" % (val, y, x))
            if val in self.secsets[self._rowcol_to_sector(x, y)]:
                raise RuntimeError("duplicate %d in sector %d, found in row "
                                   "%d/column %d" %
                                   (val, self._rowcol_to_sector(x, y), x, y))
        self.m[x][y] = val
        self.freecount -= 1
        self.rowsets[x].add(val) 
        self.colsets[y].add(val)
        self.secsets[self._rowcol_to_sector(x, y)].add(val)

    def unset(self, x, y, val):
        """
        Unset a cell.
        """
        assert 1 <= x and x <= 9 and 1 <= y and y <= 9 \
               and self.freecount <= 81 and self.m[x][y] == val
        self.m[x][y] = 0
        self.freecount += 1
        self.rowsets[x].remove(val)
        self.colsets[y].remove(val)
        self.secsets[self._rowcol_to_sector(x, y)].remove(val)

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
        self.set(x, y, val)
        try:
            for xx in xrange(1, 10):
                for yy in xrange(1, 10):
                    if self.m[xx][yy] != 0:
                        continue
                    if len(self.get_possible_values(xx, yy)) == 0:
                        return False
        finally:
            self.unset(x, y, val)
        return True

    @staticmethod
    def _rowcol_to_sector(x, y):
        return 3 * ((x - 1) / 3) + (y - 1) / 3 + 1

    def display(self, label):
        """
        Display the contents of the Sudoku board.
        """
        sys.stdout.write("\n%s:\n" % label)
        self._horiz_line()
        self._sector_row(1)
        self._horiz_line()
        self._sector_row(2)
        self._horiz_line()
        self._sector_row(3)
        self._horiz_line()

    @staticmethod
    def _horiz_line():
        sys.stdout.write('-' * 25 + '\n')

    def _sector_row(self, s):
        for i in xrange(3*(s-1)+1, 3*s+1):
            self._row(i)

    def _row(self, i):
        sys.stdout.write('| ' + ' '.join(self._subrow(i, 1, 3))
                         + ' | ' + ' '.join(self._subrow(i, 4, 6))
                         + ' | ' + ' '.join(self._subrow(i, 7, 9)) + ' |\n')

    def _subrow(self, i, j1, j2):
        return [v==0 and ' ' or str(v) for v in self.m[i][j1:j2+1]]
