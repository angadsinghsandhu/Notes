# NUMBER OF ISLANDS

# Problem number: 200
# Difficulty: Medium
# Tags: Depth-First Search, Breadth-First Search, Union-Find
# Link: https://leetcode.com/problems/number-of-islands/

from typing import List

class Solution:
    """
    This problem requires counting the number of islands in a 2D binary grid. 
    An island is defined as a group of connected '1's (land) surrounded by '0's (water).
    We can solve this problem using various methods: Depth-First Search (DFS), 
    Breadth-First Search (BFS), and Union-Find (Disjoint Set Union). 
    Below are the implementations of each approach.

    Input:
        - grid : List[List[str]] : 2D binary grid where '1' represents land and '0' represents water

    Output:
        - int : number of islands
    """
    
    def numIslandsDFS(self, grid: List[List[str]]) -> int:
        """
        Depth-First Search (DFS) approach to count the number of islands.
        This method explores each '1' and marks the connected lands as visited by 
        changing '1' to '0' during the traversal.

        T.C. : O(m * n) where m and n are the dimensions of the grid
        S.C. : O(m * n) in the worst case for the recursion stack
        """
        if not grid:
            return 0

        def dfs(r, c):
            # base case: return if out of bounds or at a '0'
            if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == '0':
                return
            # mark the cell as visited
            grid[r][c] = '0'
            # explore all adjacent cells
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        island_count = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == '1':
                    # start a new DFS when an unvisited land is found
                    dfs(r, c)
                    island_count += 1
        
        return island_count
    
    def numIslandsBFS(self, grid: List[List[str]]) -> int:
        """
        Breadth-First Search (BFS) approach to count the number of islands.
        This method uses a queue to explore each '1' and marks the connected 
        lands as visited by changing '1' to '0' during the traversal.

        T.C. : O(m * n) where m and n are the dimensions of the grid
        S.C. : O(min(m, n)) for the queue
        """
        if not grid:
            return 0
        
        from collections import deque
        
        def bfs(r, c):
            queue = deque([(r, c)])
            grid[r][c] = '0'  # mark as visited
            while queue:
                x, y = queue.popleft()
                # explore all adjacent cells
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = x + dx, y + dy
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == '1':
                        queue.append((nr, nc))
                        grid[nr][nc] = '0'  # mark as visited
        
        island_count = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == '1':
                    # start a new BFS when an unvisited land is found
                    bfs(r, c)
                    island_count += 1
        
        return island_count

    def numIslandsUnionFind(self, grid: List[List[str]]) -> int:
        """
        Union-Find (Disjoint Set Union) approach to count the number of islands.
        This method treats each cell as a separate set and unions connected 
        lands. The number of disjoint sets after processing all '1's gives the 
        number of islands.

        T.C. : O(m * n * α(m * n)) where α is the inverse Ackermann function (nearly constant)
        S.C. : O(m * n) for the Union-Find data structure
        """
        if not grid:
            return 0
        
        parent = {}
        rank = {}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1
        
        rows, cols = len(grid), len(grid[0])
        island_count = 0
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    parent[(r, c)] = (r, c)
                    rank[(r, c)] = 0
                    island_count += 1
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    # union with right and down cells
                    for nr, nc in [(r + 1, c), (r, c + 1)]:
                        if nr < rows and nc < cols and grid[nr][nc] == '1':
                            if find((r, c)) != find((nr, nc)):
                                union((r, c), (nr, nc))
                                island_count -= 1
        
        return island_count

# Best Method: DFS or BFS depending on preference and input size
# DFS and BFS have similar time complexities, but DFS uses more stack space in deep trees, 
# while BFS uses more memory for the queue.

# Sample Inputs
grid1 = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]

grid2 = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

# Expected Outputs
print(Solution().numIslandsDFS(grid1))  # Output: 1
print(Solution().numIslandsDFS(grid2))  # Output: 3

print(Solution().numIslandsBFS(grid1))  # Output: 1
print(Solution().numIslandsBFS(grid2))  # Output: 3

print(Solution().numIslandsUnionFind(grid1))  # Output: 1
print(Solution().numIslandsUnionFind(grid2))  # Output: 3
