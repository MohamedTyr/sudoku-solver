import tkinter as tk
from tkinter import messagebox, font
import random
import copy


class ModernSudokuGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Modern Sudoku Solver")
        self.window.configure(bg="#f0f0f0")
        self.cells = {}
        self.original_board = [[0] * 9 for _ in range(9)]
        self.solution = None
        self.solving = False
        self.solution_steps = []
        self.current_step = 0

        self.setup_styles()
        self.setup_gui()
        self.generate_puzzle()

    def setup_styles(self):
        self.cell_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")

    def setup_gui(self):
        # Title
        title_label = tk.Label(
            self.window,
            text="Sudoku Solver",
            font=self.title_font,
            bg="#f0f0f0",
            fg="#333333",
        )
        title_label.grid(row=0, column=0, pady=(20, 10))

        # Create frame for Sudoku grid
        self.grid_frame = tk.Frame(self.window, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.grid_frame.grid(row=1, column=0, padx=20, pady=20)

        for i in range(9):
            for j in range(9):
                cell = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=self.cell_font,
                    justify="center",
                    bd=0,
                    highlightthickness=1,
                    highlightbackground="#cccccc",
                )
                cell.grid(row=i, column=j, padx=1, pady=1, ipady=5)
                cell.bind(
                    "<KeyRelease>", lambda e, row=i, col=j: self.validate_move(row, col)
                )
                self.cells[(i, j)] = cell

                if i % 3 == 0 and i != 0:
                    cell.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:
                    cell.grid(padx=(3, 1))

        # Button frame
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.grid(row=2, column=0, pady=20)

        solve_button = tk.Button(
            button_frame,
            text="Solve",
            command=self.start_solve_animation,
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
        )
        solve_button.grid(row=0, column=1, padx=10)

        new_button = tk.Button(
            button_frame,
            text="New Game",
            command=self.generate_puzzle,
            font=self.button_font,
            bg="#2196F3",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
        )
        new_button.grid(row=0, column=0, padx=10)

    def reset_board(self):
        """Reset all board states and cell properties"""
        self.original_board = [[0] * 9 for _ in range(9)]
        self.solution = None
        self.solving = False
        self.solution_steps = []
        self.current_step = 0

        # Reset all cells
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.delete(0, tk.END)
                cell.config(state="normal", fg="#000000", bg="#ffffff")

    def is_valid_board(self, board):
        """Check if the current board state is valid"""

        def is_valid_unit(units):
            units = [u for u in units if u != 0]
            return len(units) == len(set(units))

        # Check rows
        for row in board:
            if not is_valid_unit(row):
                return False

        # Check columns
        for col in range(9):
            if not is_valid_unit([board[row][col] for row in range(9)]):
                return False

        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(board[box_row + i][box_col + j])
                if not is_valid_unit(box):
                    return False

        return True

    def generate_valid_complete_board(self):
        """Generate a complete valid Sudoku board"""
        # Start with empty board
        board = [[0] * 9 for _ in range(9)]

        # Fill diagonal boxes first (these are independent of each other)
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box + i][box + j] = nums.pop()

        # Solve the rest of the board
        self._solve_with_steps(board, [])
        return board

    def generate_puzzle(self):
        """Generate a new valid Sudoku puzzle"""
        self.reset_board()  # Reset everything first

        # Generate a complete solved board
        try:
            complete_board = self.generate_valid_complete_board()
            if not self.is_valid_board(complete_board):
                raise ValueError("Generated invalid board")

            # Save the solution
            self.solution = [row[:] for row in complete_board]

            # Create the puzzle by removing numbers
            self.original_board = [row[:] for row in complete_board]
            cells_to_remove = random.randint(40, 50)

            positions = [(i, j) for i in range(9) for j in range(9)]
            random.shuffle(positions)

            for pos in positions[:cells_to_remove]:
                self.original_board[pos[0]][pos[1]] = 0

            # Verify the board is still valid
            if not self.is_valid_board(self.original_board):
                raise ValueError("Generated invalid puzzle")

            self.update_board_display()

        except Exception as e:
            print(f"Error generating puzzle: {e}")
            # If anything goes wrong, try again
            self.generate_puzzle()

    def get_possible_values(self, board, row, col):
        used = set()
        # Check row
        for i in range(9):
            used.add(board[row][i])
        # Check column
        for i in range(9):
            used.add(board[i][col])
        # Check box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                used.add(board[i][j])
        return [num for num in range(1, 10) if num not in used]

    def find_best_empty_cell(self, board):
        min_possibilities = 10
        best_cell = None
        best_values = None

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    possible_values = self.get_possible_values(board, i, j)
                    if len(possible_values) < min_possibilities:
                        min_possibilities = len(possible_values)
                        best_cell = (i, j)
                        best_values = possible_values
                        if min_possibilities == 0:
                            return None, []
                        if min_possibilities == 1:
                            return best_cell, best_values
        return best_cell, best_values

    def solve_with_steps(self, board):
        steps = []
        if not self._solve_with_steps(board, steps):
            return None, []
        return board, steps

    def _solve_with_steps(self, board, steps):
        cell, values = self.find_best_empty_cell(board)
        if not cell:
            if values == []:  # No valid moves
                return False
            return True  # Board is filled

        row, col = cell
        for value in values:
            board[row][col] = value
            steps.append((row, col, value))

            if self._solve_with_steps(board, steps):
                return True

            board[row][col] = 0
            steps.append((row, col, 0))  # Add backtrack step

        return False

    def update_board_display(self):
        """Update the GUI to display the current board state"""
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.delete(0, tk.END)

                if self.original_board[i][j] != 0:
                    cell.insert(0, str(self.original_board[i][j]))
                    cell.config(state="readonly", fg="#000000", bg="#e6e6e6")
                else:
                    cell.config(state="normal", fg="#000000", bg="#ffffff")

    def validate_move(self, row, col):
        cell = self.cells[(row, col)]
        value = cell.get()

        if value == "":
            self.original_board[row][col] = 0
            cell.config(bg="#ffffff")
            return

        try:
            value = int(value)
            if value < 1 or value > 9:
                raise ValueError
        except ValueError:
            cell.delete(0, tk.END)
            return

        if value == self.solution[row][col]:
            self.original_board[row][col] = value
            cell.config(fg="#000000", bg="#e6f3ff")
        else:
            cell.config(fg="#ff0000", bg="#ffebee")

    def start_solve_animation(self):
        if self.solving:
            return

        self.solving = True
        board_copy = [row[:] for row in self.original_board]
        _, self.solution_steps = self.solve_with_steps(board_copy)
        self.current_step = 0
        self.animate_solution_step()

    def animate_solution_step(self):
        if not self.solving or self.current_step >= len(self.solution_steps):
            self.solving = False
            if not any(0 in row for row in self.original_board):
                messagebox.showinfo("Success", "Sudoku solved!")
            return

        row, col, value = self.solution_steps[self.current_step]
        self.original_board[row][col] = value
        cell = self.cells[(row, col)]
        cell.config(state="normal")
        cell.delete(0, tk.END)

        if value != 0:
            cell.insert(0, str(value))
            cell.config(fg="#0000ff", bg="#e6f3ff")
        else:
            cell.config(bg="#ffffff")

        self.current_step += 1
        self.window.after(100, self.animate_solution_step)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = ModernSudokuGUI()
    game.run()
