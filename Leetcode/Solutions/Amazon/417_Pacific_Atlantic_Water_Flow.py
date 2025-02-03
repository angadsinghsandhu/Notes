# TODO: revisit

# File: Leetcode/Solutions/417_Pacific_Atlantic_Water_Flow.py

"""
Problem Number: 417
Problem Name: Pacific Atlantic Water Flow
Difficulty: Medium
Tags: Depth-First Search, Breadth-First Search, Array, Matrix
Company (Frequency): Amazon (15), Microsoft (10), Google (8)
Leetcode Link: https://leetcode.com/problems/pacific-atlantic-water-flow/description/

DESCRIPTION

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an m x n integer matrix `heights` where `heights[r][c]` represents the height above sea level of the cell at coordinate (r, c).

The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.

Return a 2D list of grid coordinates `result` where `result[i] = [ri, ci]` denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.

---

#### Example 1:
**Input:**
```plaintext
heights = [ [1,2,2,3,5],
            [3,2,3,4,4],
            [2,4,5,3,1],
            [6,7,1,4,5],
            [5,1,1,2,4]]
```

**Output:**
```plaintext
[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

**Explanation:**  
The following cells can flow to the Pacific and Atlantic oceans, as shown below:
[0,4]: [0,4] -> Pacific Ocean 
       [0,4] -> Atlantic Ocean
[1,3]: [1,3] -> [0,3] -> Pacific Ocean 
       [1,3] -> [1,4] -> Atlantic Ocean
[1,4]: [1,4] -> [1,3] -> [0,3] -> Pacific Ocean 
       [1,4] -> Atlantic Ocean
[2,2]: [2,2] -> [1,2] -> [0,2] -> Pacific Ocean 
       [2,2] -> [2,3] -> [2,4] -> Atlantic Ocean
[3,0]: [3,0] -> Pacific Ocean 
       [3,0] -> [4,0] -> Atlantic Ocean
[3,1]: [3,1] -> [3,0] -> Pacific Ocean 
       [3,1] -> [4,1] -> Atlantic Ocean
[4,0]: [4,0] -> Pacific Ocean 
       [4,0] -> Atlantic Ocean

#### Constraints:
- `m == heights.length`
- `n == heights[r].length`
- `1 <= m, n <= 200`
- `0 <= heights[r][c] <= 10^5`
"""

from typing import List
from collections import deque

class Solution:
    """
    Thought Process:
    - The problem involves finding cells from which water can flow to both the Pacific and Atlantic oceans.
    - A brute-force approach would involve checking every cell, but this is inefficient.
    - An optimized approach uses BFS or DFS starting from the ocean borders and moving inland to mark reachable cells.

    Input:
        heights: List[List[int]] - A 2D list representing the heights of the island's cells.

    Output:
        List[List[int]] - A list of coordinates representing cells that can flow to both oceans.
    """

    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """
        Approach:
        - Use BFS starting from the Pacific and Atlantic ocean borders.
        - Track cells that can be reached from each ocean.
        - Return the intersection of cells that can be reached from both oceans.

        T.C.: O(m * n) - Each cell is processed once.
        S.C.: O(m * n) - Additional space for visited sets and queues.
        """
        if not heights:
            return []

        num_rows, num_columns = len(heights), len(heights[0])
        pacific_queue = deque()
        atlantic_queue = deque()
        visited_pacific = set()
        visited_atlantic = set()

        # Initialize queues and visited sets with border cells
        for row in range(num_rows):
            pacific_queue.append((row, 0))
            visited_pacific.add((row, 0))

            atlantic_queue.append((row, num_columns - 1))
            visited_atlantic.add((row, num_columns - 1))

        for col in range(num_columns):
            pacific_queue.append((0, col))
            visited_pacific.add((0, col))

            atlantic_queue.append((num_rows - 1, col))
            visited_atlantic.add((num_rows - 1, col))

        # Perform BFS for Pacific Ocean
        self._bfs(heights, pacific_queue, visited_pacific, num_rows, num_columns)

        # Perform BFS for Atlantic Ocean
        self._bfs(heights, atlantic_queue, visited_atlantic, num_rows, num_columns)

        # Return the intersection of cells that can be reached from both oceans
        return list(visited_pacific.intersection(visited_atlantic))

    def _bfs(self, heights: List[List[int]], queue: deque, visited: set, num_rows: int, num_columns: int) -> None:
        """
        Helper function to perform BFS.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Right, Down, Left, Up
        while queue:
            row, col = queue.popleft()
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < num_rows and 0 <= new_col < num_columns and
                    (new_row, new_col) not in visited and
                    heights[new_row][new_col] >= heights[row][col]):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    heights1 = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    print(solution.pacificAtlantic(heights1))  # Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

    # Test case 2
    heights2 = [[1]]
    print(solution.pacificAtlantic(heights2))  # Output: [[0,0]]
