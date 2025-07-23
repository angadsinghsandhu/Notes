# TODO: revisit

# File: Leetcode/Solutions/Amazon/688_Knight_Probability_in_Chessboard.py

"""
Problem Number: 688
Problem Name: Knight Probability in Chessboard
Difficulty: Medium
Tags: Dynamic Programming
Company (Frequency): Amazon (45)
Leetcode Link: https://leetcode.com/problems/knight-probability-in-chessboard/description/

DESCRIPTION

On an `n x n` chessboard, a knight starts at the cell `(row, column)` and attempts to make exactly `k` moves. The rows and columns are 0-indexed, so the top-left cell is `(0, 0)`, and the bottom-right cell is `(n - 1, n - 1)`.

A chess knight has eight possible moves it can make, as illustrated below. Each move is two cells in a cardinal direction, then one cell in an orthogonal direction.

Each time the knight is to move, it chooses one of eight possible moves uniformly at random (even if the piece would go off the chessboard) and moves there.

The knight continues moving until it has made exactly `k` moves or has moved off the chessboard.

Return the probability that the knight remains on the board after it has stopped moving.

---

#### Example 1:
**Input:**
```plaintext
n = 3, k = 2, row = 0, column = 0
```

**Output:**
```plaintext
0.06250
```

**Explanation:**  
There are two moves (to `(1,2)`, `(2,1)`) that will keep the knight on the board.
From each of those positions, there are also two moves that will keep the knight on the board.
The total probability the knight stays on the board is `0.0625`.

#### Constraints:
- `1 <= n <= 25`
- `0 <= k <= 100`
- `0 <= row, column <= n - 1`
"""

class Solution:
    """
    Thought Process:
    - The problem involves calculating the probability that a knight remains on the chessboard after making exactly `k` moves.
    - The knight has 8 possible moves, and each move is equally likely.
    - We can use dynamic programming to compute the probability of the knight being on each cell after each move.
    - The probability of the knight being on a cell after `k` moves depends on the probabilities of being on the adjacent cells after `k-1` moves.

    Input:
        n: int - The size of the chessboard (n x n).
        k: int - The number of moves the knight makes.
        row: int - The starting row of the knight.
        column: int - The starting column of the knight.

    Output:
        float - The probability that the knight remains on the board after `k` moves.
    """

    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        """
        Approach:
        - Use dynamic programming to compute the probability of the knight being on each cell after each move.
        - Initialize a 2D DP table where `dp[i][j]` represents the probability of the knight being on cell `(i, j)` after the current number of moves.
        - For each move, update the DP table by considering all 8 possible moves from each cell.
        - If a move takes the knight off the board, it does not contribute to the probability.
        - After processing all `k` moves, the probability of the knight being on the board is the sum of probabilities in the DP table.

        T.C.: O(k * n^2) - We process each cell on the board for each move.
        S.C.: O(n^2) - We use a 2D DP table to store probabilities.
        """
        # Define the 8 possible moves of a knight
        moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
                 (2, 1), (1, 2), (-1, 2), (-2, 1)]
        
        # Initialize the DP table
        dp = [[0] * n for _ in range(n)]
        dp[row][column] = 1.0  # The knight starts at (row, column) with probability 1.0
        
        # Iterate over each move
        for _ in range(k):
            new_dp = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if dp[i][j] > 0:
                        for dx, dy in moves:
                            x, y = i + dx, j + dy
                            if 0 <= x < n and 0 <= y < n:
                                new_dp[x][y] += dp[i][j] / 8.0
            dp = new_dp
        
        # The total probability is the sum of all probabilities in the DP table
        return sum(map(sum, dp))

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    n1, k1, row1, column1 = 3, 2, 0, 0
    print(solution.knightProbability(n1, k1, row1, column1))  # Output: 0.0625

    # Test case 2
    n2, k2, row2, column2 = 1, 0, 0, 0
    print(solution.knightProbability(n2, k2, row2, column2))  # Output: 1.0