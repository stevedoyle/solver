import unittest
from sudoku import FutosjikiGrid
import sys
import logging


class TestFutosjikiGrid(unittest.TestCase):

    def test_init(self):
        grid = FutosjikiGrid(5)
        self.assertEqual(grid.nrows, 5)
        self.assertEqual(grid.ncols, 5)

    def test_solve1(self):
        log = logging.getLogger('TestFutosjikiGrid.test_solve2')
        grid = FutosjikiGrid(4)
        grid.fill([
            [3, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        grid.addRule((1, 0), (1, 1))
        grid.addRule((2, 0), (1, 0))
        grid.addRule((2, 2), (3, 2))

        log.debug(grid)
        grid.solve()
        log.debug(grid)
        self.assertTrue(grid.solved())

    def test_solve_with_guessing(self):
        log = logging.getLogger('TestFutosjikiGrid.test_solve_with_guessing')
        grid = FutosjikiGrid(5)
        grid.fill([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0],
            [0, 0, 0, 2, 0]
        ])
        grid.addRule((0, 0), (1, 0))
        grid.addRule((0, 3), (1, 3))
        grid.addRule((1, 3), (1, 2))
        grid.addRule((1, 2), (2, 2))
        grid.addRule((2, 4), (1, 4))
        grid.addRule((4, 1), (4, 0))
        grid.addRule((4, 2), (3, 2))

        log.debug(grid)
        grid.solve()
        log.debug(grid)
        for r in range(5):
            for c in range(5):
                log.debug('[%d][%d] = %s' % (r, c, grid.candidates(r, c)))
        self.assertTrue(grid.solved())


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('TestFutosjikiGrid.test_solve_with_guessing').setLevel(
        logging.DEBUG)
    unittest.main()
