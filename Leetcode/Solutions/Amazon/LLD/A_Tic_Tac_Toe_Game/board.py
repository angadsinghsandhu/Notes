# ================================================================
# File: tictactoe/board.py
# Description:
#   The Board class represents the game board for Tic Tac Toe.
#   - It is responsible for initializing and updating the 3x3 grid.
#   - Provides methods to make moves, check for a winner, and check if the board is full.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling for invalid moves.
# ================================================================

class Board:
    def __init__(self):
        # Initialize a 3x3 grid with '-' representing empty cells.
        self.grid = [['-' for _ in range(3)] for _ in range(3)]
        self.moves_count = 0

    def make_move(self, row, col, symbol):
        # Validate the move is within bounds and on an empty cell.
        if not (0 <= row < 3 and 0 <= col < 3) or self.grid[row][col] != '-':
            raise ValueError("Invalid move!")
        self.grid[row][col] = symbol
        self.moves_count += 1

    def is_full(self):
        # Check if the board is full (9 moves made).
        return self.moves_count == 9

    def has_winner(self):
        # Check rows for a win.
        for row in range(3):
            if self.grid[row][0] != '-' and self.grid[row][0] == self.grid[row][1] == self.grid[row][2]:
                return True

        # Check columns for a win.
        for col in range(3):
            if self.grid[0][col] != '-' and self.grid[0][col] == self.grid[1][col] == self.grid[2][col]:
                return True

        # Check diagonals for a win.
        if self.grid[0][0] != '-' and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            return True
        if self.grid[0][2] != '-' and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            return True

        return False

    def print_board(self):
        # Display the current state of the board.
        for row in range(3):
            print(" ".join(self.grid[row]))
        print()  # Print an empty line for better readability.
