import unittest
from sudoku import Cell


class TestCell(unittest.TestCase):
    def test_init(self):
        cell = Cell(9)
        self.assertEqual(cell.value, None)
        self.assertEqual(cell.candidates, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_setValue(self):
        cell = Cell(4)
        cell.setValue(2)
        self.assertEqual(cell.value, 2)
        self.assertEqual(cell.candidates, [])

    def test_eliminate(self):
        cell = Cell(5)
        self.assertEqual(cell.candidates, [1, 2, 3, 4, 5])
        cell.eliminate(3)
        self.assertEqual(cell.candidates, [1, 2, 4, 5])
        cell.eliminate(3)
        self.assertEqual(cell.candidates, [1, 2, 4, 5])
