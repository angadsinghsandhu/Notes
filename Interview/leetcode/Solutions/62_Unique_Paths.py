# File: Leetcode/Solutions/62_Unique_Paths.py

"""
Problem Number: 62
Problem Name: Unique Paths
Difficulty: Medium
Tags: Math, Dynamic Programming, Combinatorics, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, Facebook
Leetcode Link: https://leetcode.com/problems/unique-paths/description/

DESCRIPTION

There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 10^9.

---

#### Example 1:
Input: m = 3, n = 7
Output: 28

---

#### Example 2:
Input: m = 3, n = 2
Output: 3
Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

---

#### Constraints:
- 1 <= m, n <= 100
"""

import math

class Solution:
    """
    Thought Process:
    - At any cell (r, c), the robot could have arrived from either the cell above (r-1, c) or the cell to the left (r, c-1).
    - Therefore, the number of ways to reach (r, c) = ways(r-1, c) + ways(r, c-1).
    - This is a grid-based dynamic programming problem with a simple recurrence relation.
    - Alternatively, this is a combinatorics problem: to reach the destination, the robot must take exactly (m-1) down moves and (n-1) right moves in any order.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^(m+n))
    2. Memoization (Top-Down): O(m * n) time and space.
    3. Tabulation (Bottom-Up): O(m * n) time and space.
    4. Space Optimized DP: O(n) space.
    5. Combinatorics: O(m) or O(n) time, O(1) space.
    """

    def unique_paths_recursive(self, m: int, n: int) -> int:
        """
        Approach: Pure Recursion
        T.C.: O(2^(m+n))
        S.C.: O(m+n) - recursion stack.
        """
        def solve(r, c):
            if r == m - 1 and c == n - 1:
                return 1
            if r >= m or c >= n:
                return 0
            return solve(r + 1, c) + solve(r, c + 1)

        return solve(0, 0)

    def unique_paths_tabulation(self, m: int, n: int) -> int:
        """
        Approach: 2D Tabulation
        - Create an m x n grid. 
        - Fill the first row and first column with 1 (only one way to go straight right or straight down).
        
        

        T.C.: O(m * n)
        S.C.: O(m * n)
        """
        dp = [[1] * n for _ in range(m)]

        for r in range(1, m):
            for c in range(1, n):
                dp[r][c] = dp[r-1][c] + dp[r][c-1]
                
        return dp[m-1][n-1]

    def unique_paths_optimized(self, m: int, n: int) -> int:
        """
        Approach: Space Optimized DP
        - We only need the previous row to calculate the current row.
        - We can actually just use a single row and update it in place.
        
        T.C.: O(m * n)
        S.C.: O(n)
        """
        row = [1] * n

        for i in range(m - 1):
            new_row = [1] * n
            # Start from index 1 because the first element of any row is always 1
            for j in range(1, n):
                new_row[j] = new_row[j-1] + row[j]
            row = new_row
            
        return row[n-1]

    def unique_paths_math(self, m: int, n: int) -> int:
        """
        Approach: Combinatorics (Combinations)
        - Total moves = (m - 1) + (n - 1).
        - We need to choose which of those moves are "Down" (or "Right").
        - Formula: C(total_moves, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)
        
        T.C.: O(min(m, n))
        S.C.: O(1)
        """
        return math.comb(m + n - 2, m - 1)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        (3, 7),
        (3, 2),
        (7, 3),
        (3, 3)
    ]

    for m, n in test_cases:
        print(f"Grid: {m} x {n}")
        print(f"Tabulation:     {solution.unique_paths_tabulation(m, n)}")
        print(f"Space Optimized: {solution.unique_paths_optimized(m, n)}")
        print(f"Combinatorics:   {solution.unique_paths_math(m, n)}")
        print("-" * 35)

    print(f"result: {solution.unique_paths_math(test_cases[0][0], test_cases[0][1])}")
