"""
board.py
Board class definition.
"""

# system imports
import sys


class Point(object):

    def __init__(self):
        self.x = 0
        self.y = 0


class Board(object):

    _all_values = set(range(1, 10))

    def __init__(self):
        self.m = [[0]*10 for i in range(10)]
        self.freecount = 81
        self.move = [Point() for i in range(82)]
        self.rowsets = [set() for i in range(10)]
        self.colsets = [set() for i in range(10)]
        self.secsets = [set() for i in range(10)]

    def set(self, x, y, val, check=False):
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
        assert 1 <= x and x <= 9 and 1 <= y and y <= 9 \
               and self.freecount <= 81 and self.m[x][y] == val
        self.m[x][y] = 0
        self.freecount += 1
        self.rowsets[x].remove(val)
        self.colsets[y].remove(val)
        self.secsets[self._rowcol_to_sector(x, y)].remove(val)

    def get_num_constraints(self, x, y):
        return len(self.rowsets[x] | self.colsets[y] |
                   self.secsets[self._rowcol_to_sector(x, y)])

    def get_possible_values(self, x, y):
        return self._all_values - self.rowsets[x] - self.colsets[y] - \
               self.secsets[self._rowcol_to_sector(x, y)]

    def look_ahead(self, x, y, val):
        self.set(x, y, val)
        try:
            for xx in range(1, 10):
                for yy in range(1, 10):
                    if self.m[xx][yy] != 0:
                        continue
                    if len(self.get_possible_values(xx, yy)) == 0:
                        return False
        finally:
            self.unset(x, y, val)
        return True

    def _rowcol_to_sector(self, x, y):
        return 3 * ((x - 1) / 3) + (y - 1) / 3 + 1

    def display(self, label):
        sys.stdout.write("\n%s:\n" % label)
        self._horiz_line()
        self._sector_row(1)
        self._horiz_line()
        self._sector_row(2)
        self._horiz_line()
        self._sector_row(3)
        self._horiz_line()

    def _horiz_line(self):
        sys.stdout.write('-' * 25 + '\n')

    def _sector_row(self, s):
        for i in range(3*(s-1)+1, 3*s+1):
            self._row(i)

    def _row(self, i):
        sys.stdout.write('| ' + ' '.join(self._subrow(i, 1, 3))
                         + ' | ' + ' '.join(self._subrow(i, 4, 6))
                         + ' | ' + ' '.join(self._subrow(i, 7, 9)) + ' |\n')

    def _subrow(self, i, j1, j2):
        return [v==0 and ' ' or str(v) for v in self.m[i][j1:j2+1]]
