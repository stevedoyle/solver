import unittest
from sudoku import Grid


class TestGrid(unittest.TestCase):
    def test_init(self):
        grid = Grid(9)
        self.assertEqual(grid.nrows, 9)
        self.assertEqual(grid.ncols, 9)
        self.assertEqual(len(grid.cells), 9)
        self.assertEqual(len(grid.cells[0]), 9)

    def test_setValue(self):
        grid = Grid(4)
        grid.setValue(2, 3, 4)
        self.assertEqual(grid.cells[2][3].value, 4)
        self.assertNotIn(4, grid.candidates(2, 0))
        self.assertNotIn(4, grid.candidates(2, 1))
        self.assertNotIn(4, grid.candidates(2, 2))
        self.assertNotIn(4, grid.candidates(0, 3))
        self.assertNotIn(4, grid.candidates(1, 3))
        self.assertNotIn(4, grid.candidates(3, 3))

    def test_getValue(self):
        grid = Grid(9)
        grid.setValue(1, 5, 8)
        self.assertEqual(grid.value(1, 5), 8)

    def test_solved(self):
        grid = Grid(2)
        self.assertFalse(grid.solved())
        grid.fill([[1, 2], [2, 1]])
        self.assertTrue(grid.solved())
