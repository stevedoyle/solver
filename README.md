# Solver

A set of utilities for solving grid based puzzles including sudoku.

## Getting Started

At the moment, solver is simply a library of utilities. After cloning the repo, run the unit tests to make sure that everything is working.

`python3 -m unittest discover`

## Sudoku Example
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
    grid.solve()
    print(grid)

## Futoskiki Example
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
    grid.solve()


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

