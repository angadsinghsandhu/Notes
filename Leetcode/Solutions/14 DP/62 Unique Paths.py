# UNIQUE PATHS

# Problem number: 62
# Difficulty: Medium
# Tags: Dynamic Programming, Combinatorics
# link: https://leetcode.com/problems/unique-paths/

class Solution:
    """
    This problem requires calculating the number of unique paths from the top-left corner 
    to the bottom-right corner of an m x n grid. The robot can only move either down or right.

    The solution can be approached using dynamic programming. We create a 2D DP array where each 
    cell represents the number of unique paths to that cell. The number of paths to reach any cell 
    is the sum of the paths to the cell directly above and the cell directly to the left.

    Alternatively, the problem can be solved using combinatorial mathematics, where the total number of 
    unique paths is equal to the binomial coefficient C(m + n - 2, m - 1) or C(m + n - 2, n - 1).

    T.C. : O(m * n)
    S.C. : O(m * n) [or O(min(m, n)) for optimized space complexity]

    Input:
        - m : int : number of rows
        - n : int : number of columns

    Output:
        - int : number of unique paths from the top-left to the bottom-right of the grid
    """
    def uniquePaths(self, m: int, n: int) -> int:
        # Initialize a 2D DP array with 1s as there's only one way to reach any cell in the first row or column
        dp = [[1] * n for _ in range(m)]
        
        # Fill the DP array
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        # The bottom-right cell contains the total number of unique paths
        return dp[-1][-1]
    
# Sample Inputs
m = 3
n = 7

# Expected Output : 28
print(Solution().uniquePaths(m, n))