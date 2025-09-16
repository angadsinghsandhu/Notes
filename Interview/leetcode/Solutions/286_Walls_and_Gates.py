# TODO: revisit

"""
Problem Number: 286
Problem Name: Walls and Gates
Difficulty: Medium
Tags: BFS, Multi-source BFS, Grid, Graph, Neetcode 150
Company (Frequency): Amazon, Bloomberg, ByteDance, Facebook, Google, Microsoft, Uber
Leetcode Link: https://leetcode.com/problems/walls-and-gates/

DESCRIPTION

You are given an m x n 2D grid initialized with these three possible values:
- -1: A wall or an obstacle.
- 0: A gate.
- INF: Infinity means an empty room. Represented by 2^31 - 1 = 2147483647.

Fill each empty room with the distance to its nearest gate. If it's impossible to reach a gate, leave it as INF.

Example:
Given the 2D grid:
INF  -1   0  INF
INF INF INF  -1
INF  -1 INF  -1
  0  -1 INF INF

After running the function:
  3  -1   0   1
  2   2   1  -1
  1  -1   2  -1
  0  -1   3   4

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 250
- grid[i][j] is -1, 0, or 2^31 - 1.
"""

from typing import List
from collections import deque

class Solution:
    """
    Thought Process:
    - The problem requires calculating the shortest distance from each empty room (INF) to the nearest gate (0).
    - BFS is ideal for shortest path problems in unweighted grids. Starting BFS from all gates simultaneously ensures efficient propagation of minimum distances.

    Approach:
    1. Multi-source BFS: Initialize a queue with all gate coordinates (value 0).
    2. BFS Expansion: For each cell, update its neighbors' distances if they're empty rooms (INF).
    3. In-place Modification: Update the input grid directly to store distances, using BFS to guarantee shortest paths.

    Time Complexity: O(m*n) - Each cell is processed at most once.
    Space Complexity: O(m*n) - Queue storage in worst-case scenario.
    """

    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Modifies the input matrix in-place with distances to nearest gates.
        
        Parameters:
        rooms (List[List[int]]): Input grid with -1 (walls), 0 (gates), and 2147483647 (empty rooms)
        
        Returns:
        None: Modifies the input matrix directly
        """
        if not rooms or not rooms[0]:
            return
        
        m, n = len(rooms), len(rooms[0])
        q = deque()
        
        # Initialize queue with all gates (0s)
        for i in range(m):
            for j in range(n):
                if rooms[i][j] == 0:
                    q.append((i, j))
        
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while q:
            i, j = q.popleft()
            for di, dj in directions:
                ni, nj = i + di, j + dj
                # Check boundaries and if cell is an unprocessed room (INF)
                if 0 <= ni < m and 0 <= nj < n and rooms[ni][nj] == 2147483647:
                    rooms[ni][nj] = rooms[i][j] + 1
                    q.append((ni, nj))

# Sample test cases
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    rooms1 = [
        [2147483647, -1, 0, 2147483647],
        [2147483647, 2147483647, 2147483647, -1],
        [2147483647, -1, 2147483647, -1],
        [0, -1, 2147483647, 2147483647]
    ]
    solution.wallsAndGates(rooms1)
    print("Test 1 Result:")
    for row in rooms1:
        print(row)
    # Expected Output:
    # [3, -1, 0, 1]
    # [2, 2, 1, -1]
    # [1, -1, 2, -1]
    # [0, -1, 3, 4]
    
    # Test case 2 (All walls)
    rooms2 = [
        [-1, -1],
        [-1, -1]
    ]
    solution.wallsAndGates(rooms2)
    print("\nTest 2 Result:")
    for row in rooms2:
        print(row)
    # Expected Output remains unchanged
    
    # Test case 3 (Single gate)
    rooms3 = [
        [2147483647, 0],
        [2147483647, 2147483647]
    ]
    solution.wallsAndGates(rooms3)
    print("\nTest 3 Result:")
    for row in rooms3:
        print(row)
    # Expected Output:
    # [1, 0]
    # [2, 1]