# MINIMUM PATH SUM

# Problem number: 64
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/minimum-path-sum/

from typing import List

class Solution:
    """
    This problem involves finding the minimum path sum from the top-left to the bottom-right 
    of a given grid. The movement is restricted to either right or down at any point in time.
    We can solve this using a dynamic programming approach where we update each cell in the grid 
    to hold the minimum sum required to reach that cell.

    The DP transition is simple: for each cell, we take the minimum of the sum from the cell directly above 
    or the cell directly to the left, and add the current cell's value to it.

    T.C. : O(m * n)
    S.C. : O(1) [in-place modification of the grid]

    Input:
        - grid : List[List[int]] : a 2D grid of non-negative integers

    Output:
        - int : the minimum sum path from the top-left to the bottom-right of the grid
    """
    def minPathSum(self, grid: List[List[int]]) -> int:
        # Get the dimensions of the grid
        m, n = len(grid), len(grid[0])
        
        # Update the grid in-place to store the minimum path sum at each cell
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                elif i == 0:
                    grid[i][j] += grid[i][j-1]
                elif j == 0:
                    grid[i][j] += grid[i-1][j]
                else:
                    grid[i][j] += min(grid[i-1][j], grid[i][j-1])
        
        # The bottom-right cell contains the minimum path sum
        return grid[-1][-1]
    
# Sample Inputs
grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]

# Expected Output : 7
print(Solution().minPathSum(grid))