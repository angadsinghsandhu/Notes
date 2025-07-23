# TODO: revisit

# File: Leetcode/Solutions/221_Maximal_Square.py

"""
Problem Number: 221
Problem Name: Maximal Square
Difficulty: Medium
Tags: Dynamic Programming, Matrix
Company (Frequency): Amazon (45), Google (32), Microsoft (25)
Leetcode Link: https://leetcode.com/problems/maximal-square/description/

DESCRIPTION

Given an `m x n` binary matrix filled with `0`'s and `1`'s, find the largest square containing only `1`'s and return its area.

---

#### Example 1:
**Input:**
```plaintext
matrix = [
    ["1","0","1","0","0"],
    ["1","0","1","1","1"],
    ["1","1","1","1","1"],
    ["1","0","0","1","0"]
]
```

**Output:**
```plaintext
4
```

**Explanation:**  
The largest square containing only `1`'s has an area of `4`.

#### Constraints:
- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 300`
- `matrix[i][j]` is `'0'` or `'1'`.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding the largest square of `1`'s in a binary matrix.
    - A brute-force approach involves checking every possible square, but this is inefficient.
    - An optimized approach uses dynamic programming to keep track of the largest square ending at each cell.

    Input:
        matrix: List[List[str]] - A binary matrix filled with `0`'s and `1`'s.

    Output:
        int - The area of the largest square containing only `1`'s.
    """

    def brute_force_solution(self, matrix: List[List[str]]) -> int:
        """
        Approach:
        - Iterate through every possible square in the matrix.
        - Check if the square contains only `1`'s.
        - Track the largest square found.

        T.C.: O((m * n)^2) - Checking every possible square.
        S.C.: O(1) - No additional space used.
        """
        if not matrix:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        max_square = 0

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == '1':
                    current_max = 1
                    flag = True
                    while i + current_max < rows and j + current_max < cols and flag:
                        for k in range(i, i + current_max + 1):
                            if matrix[k][j + current_max] == '0':
                                flag = False
                                break
                        for k in range(j, j + current_max + 1):
                            if matrix[i + current_max][k] == '0':
                                flag = False
                                break
                        if flag:
                            current_max += 1
                    max_square = max(max_square, current_max)

        return max_square * max_square

    def optimized_solution(self, matrix: List[List[str]]) -> int:
        """
        Approach:
        - Use dynamic programming to store the size of the largest square ending at each cell.
        - If the current cell is `'1'`, the size of the square ending at that cell is the minimum of the squares ending at the top, left, and top-left cells plus `1`.
        - Track the maximum square size found.

        T.C.: O(m * n) - Iterating through the matrix once.
        S.C.: O(m * n) - Using a DP table to store intermediate results.
        """
        if not matrix:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]
        max_square = 0

        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if matrix[i - 1][j - 1] == '1':
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    max_square = max(max_square, dp[i][j])

        return max_square * max_square

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    matrix1 = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"]
    ]
    print(solution.brute_force_solution([row[:] for row in matrix1]))  # Output: 4
    print(solution.optimized_solution([row[:] for row in matrix1]))    # Output: 4

    # Test case 2
    matrix2 = [
        ["0", "1"],
        ["1", "0"]
    ]
    print(solution.brute_force_solution([row[:] for row in matrix2]))  # Output: 1
    print(solution.optimized_solution([row[:] for row in matrix2]))    # Output: 1

    # Test case 3
    matrix3 = [["0"]]
    print(solution.brute_force_solution([row[:] for row in matrix3]))  # Output: 0
    print(solution.optimized_solution([row[:] for row in matrix3]))    # Output: 0