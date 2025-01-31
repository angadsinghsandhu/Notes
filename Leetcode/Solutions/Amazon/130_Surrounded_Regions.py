# TODO: revisit

"""
Problem Number: 130
Problem Name: Surrounded Regions
Difficulty: Medium
Tags: Depth-First Search (DFS), Breadth-First Search (BFS), Union-Find, Matrix
Company (Frequency): Amazon, Microsoft, Facebook, Apple, Google (Medium)
Leetcode Link: https://leetcode.com/problems/surrounded-regions/

DESCRIPTION

Given an m x n matrix board containing 'X' and 'O', capture all regions that are 4-directionally surrounded by 'X'. A region is captured by flipping all 'O's into 'X's in that surrounded region.

Example 1:
Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
Explanation: The bottom 'O' is not surrounded because it is on the edge of the board.

Example 2:
Input: board = [["X"]]
Output: [["X"]]

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The key insight is that only 'O's connected to the board's border cannot be surrounded.
    - Instead of finding surrounded regions directly, we reverse the problem:
      1. Mark all 'O's connected to the border with a temporary marker ('T')
      2. Flip all remaining 'O's (which are surrounded) to 'X's
      3. Restore the temporarily marked 'T's back to 'O's
    - This approach leverages DFS/BFS to efficiently mark border-connected regions.

    Approach:
    1. Border Identification: Iterate through border cells (first/last rows, first/last columns)
    2. DFS Marking: For each border 'O', perform DFS to mark all connected 'O's as 'T'
    3. Bulk Flip: Convert all remaining 'O's to 'X's (these are surrounded regions)
    4. Restoration: Convert all 'T's back to 'O's to restore border-connected regions

    Time Complexity: O(M*N) where M = rows, N = columns. Each cell is processed 2-3 times.
    Space Complexity: O(M*N) in worst case (DFS stack for full board of 'O's)
    """

    def solve(self, board: List[List[str]]) -> None:
        """
        Modifies the input board in-place to capture surrounded regions.
        
        Parameters:
        board (List[List[str]]): Input matrix with 'X' and 'O' characters
        
        Returns:
        None: Modifies the input matrix directly
        """
        if not board or not board[0]:
            return
        
        rows, cols = len(board), len(board[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        def dfs(r: int, c: int) -> None:
            """Marks border-connected 'O's with temporary 'T' marker using DFS"""
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == 'O':
                board[r][c] = 'T'
                for dr, dc in directions:
                    dfs(r + dr, c + dc)
        
        # Mark border-connected regions
        for r in range(rows):
            for c in range(cols):
                if (r in (0, rows-1) or c in (0, cols-1)) and board[r][c] == 'O':
                    dfs(r, c)
        
        # Convert surrounded 'O's to 'X's and restore border 'T's to 'O's
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == 'T':
                    board[r][c] = 'O'

# Sample test cases
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    board1 = [
        ["X","X","X","X"],
        ["X","O","O","X"],
        ["X","X","O","X"],
        ["X","O","X","X"]
    ]
    solution.solve(board1)
    print("Test 1 Result:", board1)
    # Expected Output: All surrounded 'O's flipped except border 'O'
    
    # Test case 2
    board2 = [["X"]]
    solution.solve(board2)
    print("Test 2 Result:", board2)
    # Expected Output: [["X"]]
    
    # Test case 3 (Custom: All 'O's connected to border)
    board3 = [
        ["O","O","O"],
        ["O","X","O"],
        ["O","O","O"]
    ]
    solution.solve(board3)
    print("Test 3 Result:", board3)
    # Expected Output: Original board remains unchanged