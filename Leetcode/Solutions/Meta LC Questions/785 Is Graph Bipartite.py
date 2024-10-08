# IS GRAPH BIPARTITE?

# Problem number: 785
# Difficulty: Medium
# Tags: Graph, Depth-First Search, Breadth-First Search, Bipartite
# Link: https://leetcode.com/problems/is-graph-bipartite/

from typing import List

class Solution:
    """
    This problem asks to determine if a given undirected graph is bipartite. A graph is bipartite 
    if we can split its nodes into two sets where no two nodes within the same set share an edge. 
    We can check this by trying to color the graph using two colors (e.g., 0 and 1) using DFS or BFS. 
    If we find any conflicts while coloring, the graph is not bipartite.
    
    We'll implement two methods to solve this problem:
    1. DFS Approach (with coloring)
    2. BFS Approach (with coloring)

    Both methods attempt to color the graph node by node and detect conflicts.
    """

    def isBipartite_DFS(self, graph: List[List[int]]) -> bool:
        """
        DFS approach to determine if the graph is bipartite.
        
        T.C. : O(n + e) where n is the number of nodes and e is the number of edges in the graph.
        S.C. : O(n) due to the recursion stack and the coloring array.
        """
        def dfs(node: int, color: int) -> bool:
            colors[node] = color
            for neighbor in graph[node]:
                if colors[neighbor] == -1:
                    # If the neighbor hasn't been colored, color it with the opposite color
                    if not dfs(neighbor, 1 - color):
                        return False
                elif colors[neighbor] == color:
                    # If the neighbor has the same color, the graph isn't bipartite
                    return False
            return True
        
        n = len(graph)
        colors = [-1] * n  # -1 means uncolored, 0 and 1 are two different colors

        for node in range(n):
            if colors[node] == -1:
                # If the node hasn't been colored, start DFS from that node
                if not dfs(node, 0):
                    return False

        return True

    def isBipartite_BFS(self, graph: List[List[int]]) -> bool:
        """
        BFS approach to determine if the graph is bipartite.
        
        T.C. : O(n + e) where n is the number of nodes and e is the number of edges in the graph.
        S.C. : O(n) due to the queue and the coloring array.
        """
        from collections import deque

        n = len(graph)
        colors = [-1] * n  # -1 means uncolored, 0 and 1 are two different colors

        for node in range(n):
            if colors[node] == -1:
                # Start BFS from an uncolored node
                queue = deque([node])
                colors[node] = 0  # Start coloring with 0

                while queue:
                    current = queue.popleft()
                    for neighbor in graph[current]:
                        if colors[neighbor] == -1:
                            # Color the neighbor with the opposite color
                            colors[neighbor] = 1 - colors[current]
                            queue.append(neighbor)
                        elif colors[neighbor] == colors[current]:
                            # If the neighbor has the same color, the graph isn't bipartite
                            return False

        return True

# Best Method: Both DFS and BFS approaches are equally optimal. BFS may be more intuitive for cycle detection.

# Sample Inputs for Testing
graph1 = [[1,2,3],[0,2],[0,1,3],[0,2]]  # Expected output: False
graph2 = [[1,3],[0,2],[1,3],[0,2]]      # Expected output: True

# Testing DFS Method
print(Solution().isBipartite_DFS(graph1))  # Output: False
print(Solution().isBipartite_DFS(graph2))  # Output: True

# Testing BFS Method
print(Solution().isBipartite_BFS(graph1))  # Output: False
print(Solution().isBipartite_BFS(graph2))  # Output: True
