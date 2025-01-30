# TODO

### **File:** `Leetcode/Solutions/Amazon/994_Rotting_Oranges.py`

"""
Problem Number: 994
Problem Name: Rotting Oranges
Difficulty: Medium
Tags: Matrix, Breadth-First Search (BFS), Graph, Queue
Company (Frequency): Amazon (76)
Leetcode Link: <https://leetcode.com/problems/rotting-oranges/>

DESCRIPTION

You are given an `m x n` grid where each cell can have one of three values:

- `0` representing an empty cell.
- `1` representing a fresh orange.
- `2` representing a rotten orange.

Every minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten.

Return the **minimum number of minutes** that must elapse until no cell has a fresh orange.  
If this is impossible, return `-1`.

---

#### Example 1:
**Input:**
```plaintext
grid = [[2,1,1],[1,1,0],[0,1,1]]
```
**Output:**
```plaintext
4
```

#### Example 2:
**Input:**
```plaintext
grid = [[2,1,1],[0,1,1],[1,0,1]]
```
**Output:**
```plaintext
-1
```
**Explanation:**  
The orange in the bottom left corner `(row 2, column 0)` is never rotten,  
because rotting only happens **4-directionally**.

#### Example 3:
**Input:**
```plaintext
grid = [[0,2]]
```
**Output:**
```plaintext
0
```
**Explanation:**  
Since there are already no fresh oranges at minute `0`, the answer is just `0`.

#### Constraints:
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 10`
- `grid[i][j]` is `0`, `1`, or `2`.
"""

from collections import deque

class Solution:
    """
    Thought Process:
    - This problem is a variation of the **Multi-Source Shortest Path** in an unweighted grid.
    - We can use **Breadth-First Search (BFS)** since all oranges rot at the same time, layer by layer.
    - **Steps:**
      1. Add all initially rotten oranges to a queue.
      2. Use BFS to rot adjacent fresh oranges while tracking the elapsed minutes.
      3. Return the number of minutes taken or `-1` if any fresh orange remains.

    Input:
        grid: List[List[int]] - The `m x n` grid of oranges.

    Output:
        int - The minimum number of minutes for all oranges to rot, or `-1` if impossible.
    """

    def orangesRotting(self, grid: list[list[int]]) -> int:
        """
        Approach:
        - Use a **queue** to store the rotten oranges' positions.
        - Use **BFS** to spread the rot layer by layer.
        - Track the number of fresh oranges and time taken.

        T.C.: O(m * n) - Each cell is processed at most once.
        S.C.: O(m * n) - In the worst case, all cells are in the queue.
        """
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0

        # Step 1: Add all rotten oranges to the queue & count fresh ones.
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c, 0))  # (row, col, minutes elapsed)
                elif grid[r][c] == 1:
                    fresh_count += 1

        # Edge case: No fresh oranges at the start.
        if fresh_count == 0:
            return 0

        # Step 2: BFS to rot adjacent fresh oranges.
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        minutes_elapsed = 0

        while queue:
            r, c, minutes = queue.popleft()
            minutes_elapsed = max(minutes_elapsed, minutes)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2  # Rot the fresh orange
                    fresh_count -= 1  # Decrease fresh orange count
                    queue.append((nr, nc, minutes + 1))  # Add newly rotten orange

        # Step 3: Check if any fresh orange remains.
        return minutes_elapsed if fresh_count == 0 else -1


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.orangesRotting([[2,1,1],[1,1,0],[0,1,1]]))  # Output: 4
    print(solution.orangesRotting([[2,1,1],[0,1,1],[1,0,1]]))  # Output: -1
    print(solution.orangesRotting([[0,2]]))                    # Output: 0