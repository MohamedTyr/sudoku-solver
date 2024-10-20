# Sudoku Solver

## Overview

This is a graphical Sudoku puzzle generator and solver built using Python's `tkinter` library. It provides a clean, interactive interface where users can solve generated puzzles or watch the step-by-step solution in action. The program features random puzzle generation, puzzle validation, and an animated solving process for visualizing how the Sudoku is solved.


<div align="center">
  <video src="Demo.mp4" width="400" />
</div>


## Features

- **Random Puzzle Generation:** Each game, the program generates a unique valid Sudoku puzzle with 40-50 pre-filled numbers, offering a new challenge every time.
- **Interactive Sudoku Grid:** Users can enter numbers directly into a $9 \times 9$ grid, with real-time validation highlighting correct entries in light blue and errors in red.

- **Step-by-Step Solve Animation:** The solver uses a backtracking algorithm to display the solution in an animated format, showing the sequence of number placements.

- **Clean GUI Design:** The modern, user-friendly interface features intuitive navigation and responsive controls, enhancing the overall solving experience.

## Requirements

- Python 3.x
- `tkinter` (usually included in Python installations)

## How to Run

1. Clone or download the repository.
2. Run the script using Python:
   ```bash
   python modern_sudoku_solver.py
   ```
3. The GUI window will open, displaying the Sudoku board.

## How to Play

- **New Game**: Click the "New Game" button to generate a new Sudoku puzzle.
- **Solve**: Click the "Solve" button to watch the step-by-step solution of the puzzle.
- **Manual Play**: Fill in numbers into the cells by clicking on the grid.
  - If a move is valid, the cell will be highlighted in light blue.
  - Invalid moves will be highlighted in red.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute it as needed!

## Author

Developed by Mohamed Abdelhamid.

Enjoy solving puzzles!
