# SURROUNDED REGIONS

# Problem number: 130
# Difficulty: Medium
# Tags: Depth-First Search, Breadth-First Search, Union-Find, Matrix
# Link: https://leetcode.com/problems/surrounded-regions/

from typing import List

class Solution:
    """
    This problem requires modifying a given m x n board where 'O' regions that are fully surrounded by 'X' 
    (i.e., not touching the board's edge) are captured by converting all 'O's in the region to 'X'.
    The solution can be approached using Depth-First Search (DFS) or Breadth-First Search (BFS).
    The idea is to identify 'O' regions connected to the edges (which can't be surrounded), mark them, 
    and then flip all unmarked 'O's to 'X'.

    T.C. : O(m * n)
    S.C. : O(m * n) for the recursive call stack in the worst case

    Input:
        - board : List[List[str]] : the m x n matrix containing 'X' and 'O' 

    Output:
        - None : the board is modified in place
    """
    def solve(self, board: List[List[str]]) -> None:
        if not board:
            return
        
        m, n = len(board), len(board[0])
        
        # Helper function to perform DFS from the given cell
        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != 'O':
                return
            board[i][j] = 'A'  # Mark the cell as 'A' to indicate it shouldn't be flipped
            # Perform DFS in all four directions
            dfs(i - 1, j)
            dfs(i + 1, j)
            dfs(i, j - 1)
            dfs(i, j + 1)
        
        # Start DFS from the edges to find and mark all 'O's connected to the edges
        for i in range(m):
            dfs(i, 0)
            dfs(i, n - 1)
        for j in range(n):
            dfs(0, j)
            dfs(m - 1, j)
        
        # Flip all 'O's to 'X', and all 'A's back to 'O'
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == 'A':
                    board[i][j] = 'O'

# Sample Inputs
board = [["X","X","X","X"],
         ["X","O","O","X"],
         ["X","X","O","X"],
         ["X","O","X","X"]]

# Expected Output : [["X","X","X","X"],
#                    ["X","X","X","X"],
#                    ["X","X","X","X"],
#                    ["X","O","X","X"]]
Solution().solve(board)
print(board)
