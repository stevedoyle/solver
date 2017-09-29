
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
        if row == 0 and col == 7 and value == 4:
            print(self.cells[4][6].candidates)

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

    def solve(self):
        for x in range(10):
            self.reduce()
            if self.solved():
                break

    def solved(self):
        if not super(SudokuGrid, self).solved():
            return False

        for i in range(self.nrows):
            values = [self.value(r, c) for (r, c) in self.subgrid(i)]
            if sorted(values) != list(range(1, self.nrows+1)):
                return False

        return True

    def reduce(self):
        self.reduceRows()
        self.reduceCols()
        self.reduceSubgrids()

    def reduceRows(self):
        for i in range(self.nrows):
            self.reduceCellGrp(self.row(i))

    def reduceCols(self):
        for i in range(self.ncols):
            self.reduceCellGrp(self.col(i))

    def reduceSubgrids(self):
        for i in range(self.nrows):
            self.reduceCellGrp(self.subgrid(i))

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
