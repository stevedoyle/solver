

class Cell(object):
    """A Cell in a grid

    """

    def __init__(self, maxValue):
        self.candidates = list(range(1, maxValue+1))
        self.value = None

    def __str__(self):
        return str(self.value) if self.value is not None else ' '

    def setValue(self, value):
        self.value = value
        self.candidates = []

    def eliminate(self, value):
        try:
            self.candidates.remove(value)
        except ValueError:
            pass

    def eliminateHigherThan(self, value):
        self.candidates = [x for x in self.candidates if x <= value]

    def eliminateLessThan(self, value):
        self.candidates = [x for x in self.candidates if x >= value]


class Grid(object):
    """A Grid of cells

    """

    def __init__(self, size):
        self.nrows = size
        self.ncols = size
        self.cells = [None] * self.nrows
        for row in range(self.nrows):
            self.cells[row] = [Cell(size) for x in range(self.ncols)]

    def row(self, idx):
        return [(idx, c) for c in range(self.ncols)]

    def col(self, idx):
        return [(r, idx) for r in range(self.nrows)]

    def candidates(self, row, col):
        return self.cells[row][col].candidates

    def value(self, row, col):
        return self.cells[row][col].value

    def setValue(self, row, col, value):
        self.cells[row][col].setValue(value)
        for r in range(self.nrows):
            if r == row:
                continue
            self.cells[r][col].eliminate(value)
        for c in range(self.ncols):
            if c == col:
                continue
            self.cells[row][c].eliminate(value)

    def fill(self, values):
        for r, row in enumerate(values):
            for c, val in enumerate(row):
                if val != 0:
                    self.setValue(r, c, val)

    def solved(self):
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.value(r, c) is None:
                    return False

        for r in range(self.nrows):
            values = [self.value(r, c) for c in range(self.ncols)]
            if sorted(values) != list(range(1, self.nrows+1)):
                return False

        for c in range(self.ncols):
            values = [self.value(r, c) for r in range(self.nrows)]
            if sorted(values) != list(range(1, self.ncols+1)):
                return False

        return True

    def solve(self):
        for x in range(10):
            self.reduce()
            if self.solved():
                return True
        return False

    def reduce(self):
        self.reduceRows()
        self.reduceCols()

    def reduceRows(self):
        for i in range(self.nrows):
            self.reduceCellGrp(self.row(i))

    def reduceCols(self):
        for i in range(self.ncols):
            self.reduceCellGrp(self.col(i))

    def reduceCellGrp(self, cellGrp):
        for x in range(1, 10):
            count = 0
            pos = 0
            for (r, c) in cellGrp:
                if x in self.candidates(r, c):
                    count += 1
                    pos = (r, c)
            if count == 1:
                self.setValue(pos[0], pos[1], x)

    def __str__(self):
        result = ''
        for r in range(self.nrows):
            result += '\n|'
            for c in range(self.ncols):
                result += '%s|' % self.cells[r][c]
        return result


class SudokuGrid(Grid):
    """A Sudoku grid.

    Standard 9x9 size.

    """

    def __init__(self):
        super(SudokuGrid, self).__init__(9)

    def setValue(self, row, col, value):
        super(SudokuGrid, self).setValue(row, col, value)
        (minr, minc) = self.subgridBounds(row, col)
        for r in range(minr, minr+3):
            for c in range(minc, minc+3):
                self.cells[r][c].eliminate(value)

    def subgridBounds(self, row, col):
        minr = 3 * int(row / 3)
        minc = 3 * int(col / 3)
        return (minr, minc)

    def subgrid(self, idx):
        minr = 3 * int(idx / 3)
        minc = 3 * (idx % 3)
        grp = []
        for r in range(minr, minr+3):
            for c in range(minc, minc+3):
                grp.append((r, c))
        return grp

    def solved(self):
        if not super(SudokuGrid, self).solved():
            return False

        for i in range(self.nrows):
            values = [self.value(r, c) for (r, c) in self.subgrid(i)]
            if sorted(values) != list(range(1, self.nrows+1)):
                return False

        return True

    def reduce(self):
        super(SudokuGrid, self).reduce()
        self.reduceSubgrids()

    def reduceSubgrids(self):
        for i in range(self.nrows):
            self.reduceCellGrp(self.subgrid(i))


class FutosjikiGrid(Grid):

    def __init__(self, size):
        super(FutosjikiGrid, self).__init__(size)
        self.rules = []

    def addRule(self, hi, lo):
        self.rules.append((hi, lo))

    def eliminateHigherThan(self, row, col, value):
        self.cells[row][col].eliminate(set(range(value+1, self.size+1)))

    def eliminateLessThan(self, row, col, value):
        self.cells[row][col].eliminate(set(range(1, value+1)))

    def reduce(self):
        super(FutosjikiGrid, self).reduce()
        self.reduceRules()

    def reduceRules(self):
        for (hi, lo) in self.rules:
            hiCell = self.cells[hi[0]][hi[1]]
            loCell = self.cells[lo[0]][lo[1]]
            # Low cell can't have candidates higher than the high cell value -1
            # or higher than the high cell lowest candidate - 1
            val = hiCell.value if hiCell.value else max(hiCell.candidates)
            loCell.eliminateHigherThan(val - 1)

            # High cell can't have candidates lower than the low cell value +1
            # or lower than the low cells highest candidate + 1
            val = loCell.value if loCell.value else min(loCell.candidates)
            hiCell.eliminateLessThan(val + 1)

            if len(hiCell.candidates) == 1:
                self.setValue(hi[0], hi[1], hiCell.candidates[0])

            if len(loCell.candidates) == 1:
                self.setValue(lo[0], lo[1], loCell.candidates[0])
