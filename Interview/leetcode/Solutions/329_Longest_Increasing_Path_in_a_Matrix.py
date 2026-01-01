# File: Leetcode/Solutions/329_Longest_Increasing_Path_in_a_Matrix.py

"""
Problem Number: 329
Problem Name: Longest Increasing Path in a Matrix
Difficulty: Hard
Tags: Array, Dynamic Programming, Depth-First Search, Graph, Topological Sort, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, DoorDash
Leetcode Link: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/description/

DESCRIPTION

Given an `m x n` integers `matrix`, return the length of the longest increasing path in `matrix`.

From each cell, you can either move in four directions: left, right, up, or down. You may not move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

---

#### Example 1:
Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
Output: 4
Explanation: The longest increasing path is [1, 2, 6, 9].

---

#### Example 2:
Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
Output: 4
Explanation: The longest increasing path is [3, 4, 5, 6]. Diagonals are not allowed.

---

#### Example 3:
Input: matrix = [[1]]
Output: 1

---

#### Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- 0 <= matrix[i][j] <= 2^31 - 1
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This problem asks for the longest path where each subsequent cell is strictly greater than the current.
    - Because it must be strictly increasing, we are guaranteed there are no cycles (a path cannot return to a cell it has already visited).
    - This makes the problem a Directed Acyclic Graph (DAG) problem.
    - We can use DFS + Memoization to find the longest path starting from each cell.
    - Alternatively, we can use Kahn's Algorithm (Topological Sort) by treating out-degrees as dependencies.

    Approach Hierarchy:
    1. Brute Force (DFS): O(4^(m*n)) - TLE
    2. DFS + Memoization: O(m * n) time and space.
    3. Topological Sort (Kahn's): O(m * n) time and space.
    """

    def longest_path_memo(self, matrix: List[List[int]]) -> int:
        """
        Approach: DFS + Memoization
        - For each cell, explore its 4 neighbors.
        - If a neighbor is greater, recursively find the path length from that neighbor.
        - Cache the results to avoid re-computing the path for the same cell.

        T.C.: O(m * n) - Each cell is visited and computed exactly once.
        S.C.: O(m * n) - For the memoization table and recursion stack.
        """
        if not matrix or not matrix[0]:
            return 0
            
        rows, cols = len(matrix), len(matrix[0])
        memo = {} # (r, c) -> longest path starting from here

        

        def dfs(r, c):
            if (r, c) in memo:
                return memo[(r, c)]
            
            res = 1 # Base case: the cell itself is a path of length 1
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    matrix[nr][nc] > matrix[r][c]):
                    res = max(res, 1 + dfs(nr, nc))
            
            memo[(r, c)] = res
            return res

        max_path = 0
        for r in range(rows):
            for c in range(cols):
                max_path = max(max_path, dfs(r, c))
                
        return max_path

    def longest_path_topological(self, matrix: List[List[int]]) -> int:
        """
        Approach: Topological Sort (Kahn's Algorithm)
        - Calculate the out-degree of each cell (how many neighbors are strictly greater).
        - Cells with out-degree 0 are "leaves" (the ends of increasing paths).
        - Use a BFS-style approach to peel off layers of leaves.
        
        

        T.C.: O(m * n)
        S.C.: O(m * n)
        """
        if not matrix or not matrix[0]:
            return 0
            
        rows, cols = len(matrix), len(matrix[0])
        out_degree = [[0] * cols for _ in range(rows)]
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        
        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        matrix[nr][nc] > matrix[r][c]):
                        out_degree[r][c] += 1
                        
        # Find all leaves (out-degree 0)
        queue = []
        for r in range(rows):
            for c in range(cols):
                if out_degree[r][c] == 0:
                    queue.append((r, c))
                    
        height = 0
        while queue:
            height += 1
            level_size = len(queue)
            for _ in range(level_size):
                r, c = queue.pop(0)
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Look at neighbors that could lead TO this cell
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        matrix[nr][nc] < matrix[r][c]):
                        out_degree[nr][nc] -= 1
                        if out_degree[nr][nc] == 0:
                            queue.append((nr, nc))
                            
        return height

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        [[9,9,4],[6,6,8],[2,1,1]],
        [[3,4,5],[3,2,6],[2,2,1]],
        [[1]]
    ]

    for m in test_cases:
        print(f"Matrix: {m}")
        print(f"DFS + Memo: {solution.longest_path_memo(m)}")
        print(f"Topological: {solution.longest_path_topological(m)}")
        print("-" * 35)

    print(f"result: {solution.longest_path_memo(test_cases[0])}")
