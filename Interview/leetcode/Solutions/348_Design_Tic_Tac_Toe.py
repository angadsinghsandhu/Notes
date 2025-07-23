# File: Leetcode/Solutions/348_Design_Tic_Tac_Toe.py

"""
Problem Number: 348
Problem Name: Design Tic-Tac-Toe
Difficulty: Medium
Tags: Design, Array, Hash Table, Matrix, Simulation
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/design-tic-tac-toe/description/

DESCRIPTION

Design a Tic-Tac-Toe game that is played between two players on an n x n grid.

The following rules are followed:

1. A move is guaranteed to be valid and is placed on an empty block.
2. Once a winning condition is reached, no more moves are allowed.
3. A player who succeeds in placing n of their marks in a horizontal, vertical, or diagonal row wins the game.

Implement the `TicTacToe` class:

- `TicTacToe(int n)`: Initializes the object with the size of the board `n`.
- `int move(int row, int col, int player)`: Indicates that the player with id `player` plays at the cell `(row, col)` of the board. The move is guaranteed to be a valid move, and the two players alternate in making moves. Return:
  - `0` if there is no winner after the move.
  - `1` if player 1 is the winner after the move.
  - `2` if player 2 is the winner after the move.

---

#### Example 1:
**Input:**
```plaintext
["TicTacToe", "move", "move", "move", "move", "move", "move", "move"]
[[3], [0, 0, 1], [0, 2, 2], [2, 2, 1], [1, 1, 2], [2, 0, 1], [1, 0, 2], [2, 1, 1]]
```

**Output:**
```plaintext
[null, 0, 0, 0, 0, 0, 0, 1]
```

**Explanation:**  
TicTacToe ticTacToe = new TicTacToe(3);
Assume that player 1 is "X" and player 2 is "O" in the board.
ticTacToe.move(0, 0, 1); // return 0 (no one wins)
|X| | |
| | | |    // Player 1 makes a move at (0, 0).
| | | |

ticTacToe.move(0, 2, 2); // return 0 (no one wins)
|X| |O|
| | | |    // Player 2 makes a move at (0, 2).
| | | |

ticTacToe.move(2, 2, 1); // return 0 (no one wins)
|X| |O|
| | | |    // Player 1 makes a move at (2, 2).
| | |X|

ticTacToe.move(1, 1, 2); // return 0 (no one wins)
|X| |O|
| |O| |    // Player 2 makes a move at (1, 1).
| | |X|

ticTacToe.move(2, 0, 1); // return 0 (no one wins)
|X| |O|
| |O| |    // Player 1 makes a move at (2, 0).
|X| |X|

ticTacToe.move(1, 0, 2); // return 0 (no one wins)
|X| |O|
|O|O| |    // Player 2 makes a move at (1, 0).
|X| |X|

ticTacToe.move(2, 1, 1); // return 1 (player 1 wins)
|X| |O|
|O|O| |    // Player 1 makes a move at (2, 1).
|X|X|X|
"""

class TicTacToe:
    """
    Thought Process:
    - The problem involves designing a Tic-Tac-Toe game that efficiently checks for a win condition after each move.
    - A brute-force approach would involve checking all rows, columns, and diagonals after each move, but this is inefficient.
    - An optimized approach uses counters to track the number of marks for each player in each row, column, and diagonal.

    Input:
        n: int - The size of the Tic-Tac-Toe board.

    Output:
        int - The result of the move: 0 (no winner), 1 (player 1 wins), or 2 (player 2 wins).
    """

    def __init__(self, n: int):
        """
        Initialize the Tic-Tac-Toe game board with a given size.
        """
        self.n = n
        # Initialize counters for rows, columns, and diagonals
        self.rows = [0] * n  # Tracks the sum of marks in each row
        self.cols = [0] * n  # Tracks the sum of marks in each column
        self.diag = 0        # Tracks the sum of marks in the main diagonal
        self.anti_diag = 0   # Tracks the sum of marks in the anti-diagonal

    def move(self, row: int, col: int, player: int) -> int:
        """
        Player makes a move at a specified row and column.
        :param row: The row index of the board, 0-indexed.
        :param col: The column index of the board, 0-indexed.
        :param player: The identifier of the player (either 1 or 2).
        :return: The current winning condition, can be either:
                 0: No one wins.
                 1: Player 1 wins.
                 2: Player 2 wins.
        """
        # Determine the value to add based on the player
        value = 1 if player == 1 else -1

        # Update the row and column counters
        self.rows[row] += value
        self.cols[col] += value

        # Update the diagonal counters if the move is on a diagonal
        if row == col:
            self.diag += value
        if row + col == self.n - 1:
            self.anti_diag += value

        # Check if any row, column, or diagonal has n marks of the same player
        if (
            abs(self.rows[row]) == self.n
            or abs(self.cols[col]) == self.n
            or abs(self.diag) == self.n
            or abs(self.anti_diag) == self.n
        ):
            return player  # The current player wins

        return 0  # No winner yet

# Run and print sample test cases
if __name__ == "__main__":
    # Test case 1
    tic_tac_toe = TicTacToe(3)
    print(tic_tac_toe.move(0, 0, 1))  # Output: 0
    print(tic_tac_toe.move(0, 2, 2))  # Output: 0
    print(tic_tac_toe.move(2, 2, 1))  # Output: 0
    print(tic_tac_toe.move(1, 1, 2))  # Output: 0
    print(tic_tac_toe.move(2, 0, 1))  # Output: 0
    print(tic_tac_toe.move(1, 0, 2))  # Output: 0
    print(tic_tac_toe.move(2, 1, 1))  # Output: 1
