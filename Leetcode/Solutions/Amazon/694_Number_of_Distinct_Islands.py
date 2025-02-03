# TODO: revisit

# File: Leetcode/Solutions/694_Number_of_Distinct_Islands.py

"""
Problem Number: 694
Problem Name: Number of Distinct Islands
Difficulty: Medium
Tags: Depth-First Search, Breadth-First Search, Union Find, Hash Table, Hash Function
Company (Frequency): Amazon, Apple, Bloomberg, Facebook, Google, Lyft, Microsoft, Uber
Leetcode Link: https://leetcode.com/problems/number-of-distinct-islands/description/

DESCRIPTION

Given a non-empty 2D array `grid` of 0's and 1's, an island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical). You may assume all four edges of the grid are surrounded by water.

Count the number of distinct islands. An island is considered to be the same as another if and only if one island can be translated (and not rotated or reflected) to equal the other.

---

#### Example 1:
**Input:**
```plaintext
grid = [
  [1,1,0,0,0],
  [1,1,0,0,0],
  [0,0,0,1,1],
  [0,0,0,1,1]
]
```

**Output:**
```plaintext
1
```

**Explanation:**  
The two islands are considered the same because they can be translated to match each other.

#### Example 2:
**Input:**
```plaintext
grid = [
  [1,1,0,1,1],
  [1,0,0,0,0],
  [0,0,0,0,1],
  [1,1,0,1,1]
]
```

**Output:**
```plaintext
3
```

**Explanation:**  
The islands are considered different because they cannot be translated to match each other.

#### Constraints:
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 50`
- `grid[i][j]` is either `0` or `1`.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding the number of distinct islands in a 2D grid.
    - An island is a group of connected '1's (land) surrounded by '0's (water).
    - Two islands are considered the same if they can be translated to match each other.
    - We can use Depth-First Search (DFS) to explore each island and record its shape.
    - The shape of an island can be represented by the sequence of moves taken during DFS.
    - By storing these sequences in a set, we can count the number of distinct islands.

    Input:
        grid: List[List[int]] - A 2D binary matrix representing the grid.

    Output:
        int - The number of distinct islands.
    """

    def numDistinctIslands(self, grid: List[List[int]]) -> int:
        """
        Approach:
        - Use DFS to explore each island and record the path taken to traverse it.
        - The path is represented as a string of moves (e.g., "right", "down", etc.).
        - Store each unique path in a set to count the number of distinct islands.

        T.C.: O(M * N) - Each cell is visited once.
        S.C.: O(M * N) - The set can store up to M * N unique paths in the worst case.
        """
        def dfs(i: int, j: int, move: int):
            grid[i][j] = 0  # Mark the cell as visited
            path.append(str(move))  # Record the move direction
            # Possible movements: up, right, down, left
            directions = (-1, 0, 1, 0, -1)
            for h in range(4):
                x, y = i + directions[h], j + directions[h+1]
                if 0 <= x < m and 0 <= y < n and grid[x][y]:
                    dfs(x, y, h+1)
            path.append(str(-move))  # Record the reverse move to differentiate shapes

        paths = set()  # Set to store unique island paths
        path = []  # Temporary list to store the current island's path
        m, n = len(grid), len(grid[0])  # Dimensions of the grid

        for i in range(m):
            for j in range(n):
                if grid[i][j]:  # If the cell is part of an island
                    dfs(i, j, 0)  # Start DFS from this cell
                    paths.add("".join(path))  # Add the path to the set
                    path.clear()  # Clear the path for the next island

        return len(paths)  # The number of distinct islands is the size of the set

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    grid1 = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1]
    ]
    print(solution.numDistinctIslands(grid1))  # Output: 1

    # Test case 2
    grid2 = [
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1]
    ]
    print(solution.numDistinctIslands(grid2))  # Output: 3
