# TODO: revisit [IMP]

# File: Leetcode/Solutions/Amazon/200_Number_of_Islands.py

"""
Problem Number: 200
Problem Name: Number of Islands
Difficulty: Medium
Tags: Depth-First Search (DFS), Breadth-First Search (BFS), Union-Find, Matrix
Company (Frequency): Amazon (103)
Leetcode Link: https://leetcode.com/problems/number-of-islands/description/

DESCRIPTION

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

---

#### Example 1:
**Input:**
```plaintext
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
```

**Output:**
```plaintext
1
```

#### Constraints:
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`.
"""

from typing import List
from collections import deque

class Solution:
    """
    Thought Process:
    - The problem involves counting the number of connected regions of `'1'`s (islands) in a 2D grid.
    - A brute-force approach involves using DFS or BFS to explore and mark all connected `'1'`s as part of the same island.
    - An optimized approach uses BFS with a queue for iterative exploration, which is more memory-efficient for large grids.

    Input:
        grid: List[List[str]] - A 2D binary grid representing land and water.

    Output:
        int - The number of islands.
    """

    def dfs_solution(self, grid: List[List[str]]) -> int:
        """
        Approach:
        - Use Depth-First Search (DFS) to explore and mark all connected `'1'`s as part of the same island.
        - Iterate through the grid, and whenever a `'1'` is found, increment the island count and perform DFS to mark all connected `'1'`s.

        T.C.: O(m * n) - Each cell is visited once.
        S.C.: O(m * n) - Recursion stack in the worst case.
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        def dfs(i, j):
            if not (0 <= i , len(grid) and 0 <= j < len(grid[0])) or grid[i][j] == '0':
                return
            grid[i][j] = '0'  # Mark as visited
            # Explore all four directions
            for dx, dy in directions:
                dfs(i + dx, j + dy)

        num_islands = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    num_islands += 1
                    dfs(i, j)
        return num_islands

    def bfs_solution(self, grid: List[List[str]]) -> int:
        """
        Approach:
        - Use Breadth-First Search (BFS) with a queue to explore and mark all connected `'1'`s as part of the same island.
        - Iterate through the grid, and whenever a `'1'` is found, increment the island count and perform BFS to mark all connected `'1'`s.

        T.C.: O(m * n) - Each cell is visited once.
        S.C.: O(min(m, n)) - Queue size in the worst case.
        """
        num_islands = 0
        rows, cols = len(grid), len(grid[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        def bfs(i, j):
            queue = deque([(i, j)])
            grid[i][j] = '0'

            while queue:
                x, y = queue.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'
                        queue.append((nx, ny))

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    num_islands += 1
                    bfs(i, j)
        return num_islands

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    print(solution.dfs_solution([row[:] for row in grid1]))  # Output: 1
    print(solution.bfs_solution([row[:] for row in grid1]))  # Output: 1

    # Test case 2
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    print(solution.dfs_solution([row[:] for row in grid2]))  # Output: 3
    print(solution.bfs_solution([row[:] for row in grid2]))  # Output: 3