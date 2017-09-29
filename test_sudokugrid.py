import unittest
from sudoku import SudokuGrid
import sys
import itertools
import logging


class TestSudokuGrid(unittest.TestCase):

    def test_init(self):
        grid = SudokuGrid()
        self.assertEqual(grid.nrows, 9)
        self.assertEqual(grid.ncols, 9)

    def test_subgridBounds(self):
        self.longMessage = True
        grid = SudokuGrid()
        for (r, c) in itertools.product([0, 1, 2], [0, 1, 2]):
            self.assertEqual(grid.subgridBounds(r, c), (0, 0))
        for (r, c) in itertools.product([0, 1, 2], [3, 4, 5]):
            self.assertEqual(grid.subgridBounds(r, c), (0, 3))
        for (r, c) in itertools.product([0, 1, 2], [6, 7, 8]):
            self.assertEqual(grid.subgridBounds(r, c), (0, 6))

        for (r, c) in itertools.product([3, 4, 5], [0, 1, 2]):
            self.assertEqual(grid.subgridBounds(r, c), (3, 0))
        for (r, c) in itertools.product([3, 4, 5], [3, 4, 5]):
            self.assertEqual(grid.subgridBounds(r, c), (3, 3))
        for (r, c) in itertools.product([3, 4, 5], [6, 7, 8]):
            self.assertEqual(grid.subgridBounds(r, c), (3, 6))

        for (r, c) in itertools.product([6, 7, 8], [0, 1, 2]):
            self.assertEqual(grid.subgridBounds(r, c), (6, 0))
        for (r, c) in itertools.product([6, 7, 8], [3, 4, 5]):
            self.assertEqual(grid.subgridBounds(r, c), (6, 3))
        for (r, c) in itertools.product([6, 7, 8], [6, 7, 8]):
            self.assertEqual(grid.subgridBounds(r, c), (6, 6))

    def test_setValue(self):
        grid = SudokuGrid()
        grid.setValue(1, 1, 2)
        self.assertEqual(grid.value(1, 1), 2)
        self.assertNotIn(2, grid.candidates(0, 0))
        self.assertNotIn(2, grid.candidates(0, 2))
        self.assertNotIn(2, grid.candidates(1, 0))
        self.assertNotIn(2, grid.candidates(1, 2))
        self.assertNotIn(2, grid.candidates(2, 0))
        self.assertNotIn(2, grid.candidates(2, 1))
        self.assertNotIn(2, grid.candidates(2, 2))

    def test_subgrid(self):
        grid = SudokuGrid()
        self.assertEqual(grid.subgrid(0), [(0, 0), (0, 1), (0, 2),
                                           (1, 0), (1, 1), (1, 2),
                                           (2, 0), (2, 1), (2, 2)])
        self.assertEqual(grid.subgrid(4), [(3, 3), (3, 4), (3, 5),
                                           (4, 3), (4, 4), (4, 5),
                                           (5, 3), (5, 4), (5, 5)])
        self.assertEqual(grid.subgrid(8), [(6, 6), (6, 7), (6, 8),
                                           (7, 6), (7, 7), (7, 8),
                                           (8, 6), (8, 7), (8, 8)])

    def test_fill(self):
        grid = SudokuGrid()
        grid.fill([
            [0, 0, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 9, 7, 0],
            [9, 6, 0, 0, 0, 0, 2, 8, 3],
            [8, 0, 0, 4, 7, 0, 0, 6, 0],
            [0, 0, 0, 8, 0, 9, 1, 0, 0],
            [5, 0, 0, 6, 2, 0, 0, 3, 0],
            [3, 5, 0, 0, 0, 0, 8, 2, 7],
            [0, 0, 0, 2, 0, 0, 3, 1, 0],
            [0, 0, 4, 0, 0, 0, 0, 0, 0]
        ])
        self.assertEqual(grid.value(0, 2), 7)
        self.assertEqual(grid.value(6, 8), 7)
        self.assertEqual(grid.value(8, 2), 4)
        self.assertNotIn(7, grid.candidates(1, 0))

    def test_reduceCellGrp(self):
        grid = SudokuGrid()
        for i in range(8):
            grid.setValue(0, i, i + 1)
        grid.reduceCellGrp(grid.row(0))
        self.assertEqual(grid.value(0, 8), 9)
        # TODO: Need to devise a better test

    def test_solve1(self):
        log = logging.getLogger('TestSudokuGrid.test_solve1')
        grid = SudokuGrid()
        grid.fill([
            [0, 0, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 9, 7, 0],
            [9, 6, 0, 0, 0, 0, 2, 8, 3],
            [8, 0, 0, 4, 7, 0, 0, 6, 0],
            [0, 0, 0, 8, 0, 9, 1, 0, 0],
            [5, 0, 0, 6, 2, 0, 0, 3, 0],
            [3, 5, 0, 0, 0, 0, 8, 2, 7],
            [0, 0, 0, 2, 0, 0, 3, 1, 0],
            [0, 0, 4, 0, 0, 0, 0, 0, 0]
        ])
        log.debug(grid)
        grid.solve()
        log.debug(grid)
        self.assertTrue(grid.solved())

    def test_solve2(self):
        log = logging.getLogger('TestSudokuGrid.test_solve2')
        grid = SudokuGrid()
        grid.fill([
            [0, 5, 0, 7, 2, 8, 0, 0, 1],
            [0, 7, 0, 0, 6, 9, 0, 0, 0],
            [8, 2, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 8, 0, 5, 6, 0, 0, 0],
            [0, 3, 0, 0, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 7, 0, 1, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 1, 4],
            [0, 0, 0, 2, 8, 0, 0, 7, 0],
            [6, 0, 0, 3, 4, 5, 0, 2, 0]
        ])
        log.debug(grid)
        grid.solve()
        log.debug(grid)
        self.assertTrue(grid.solved())

    def test_solve3(self):
        log = logging.getLogger('TestSudokuGrid.test_solve3')
        grid = SudokuGrid()
        grid.fill([
            [0, 5, 0, 0, 0, 0, 0, 4, 0],
            [0, 2, 0, 0, 0, 6, 8, 0, 1],
            [3, 0, 0, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 9, 7, 2, 0],
            [0, 0, 0, 0, 0, 1, 3, 0, 5],
            [0, 0, 0, 5, 0, 4, 1, 8, 0],
            [8, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 8, 4, 0, 7],
            [0, 4, 0, 0, 0, 0, 0, 9, 0]
        ])
        log.debug(grid)
        grid.solve()
        log.debug(grid)
        self.assertTrue(grid.solved())

    def test_solve4(self):
        log = logging.getLogger('TestSudokuGrid.test_solve4')
        grid = SudokuGrid()
        grid.fill([
            [0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 5, 2, 0, 0, 0],
            [6, 0, 0, 4, 0, 0, 5, 8, 0],
            [0, 2, 4, 0, 0, 5, 0, 0, 8],
            [0, 5, 0, 0, 0, 4, 1, 0, 0],
            [0, 9, 0, 1, 3, 0, 0, 0, 0],
            [0, 0, 9, 0, 4, 0, 0, 0, 2],
            [0, 0, 1, 0, 0, 0, 0, 5, 7],
            [0, 0, 0, 8, 0, 0, 3, 4, 0]
        ])
        log.debug(grid)
        grid.solve()
        log.debug(grid)
        self.assertTrue(grid.solved())


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('TestSudokuGrid.test_solve4').setLevel(
        logging.WARN)
    unittest.main()
