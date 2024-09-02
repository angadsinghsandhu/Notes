# NUMBER OF CONNECTED COMPONENTS IN AN UNDIRECTED GRAPH

# Problem number: 323
# Difficulty: Medium
# Tags: Graph, Depth-First Search, Breadth-First Search, Union Find
# Link: https://leetcode.ca/all/323.html, https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

from typing import List

class Solution:
    """
    This problem requires finding the number of connected components in an undirected graph.
    There are two main approaches to solve this problem: 
    1. Depth-First Search (DFS) / Breadth-First Search (BFS)
    2. Union-Find (Disjoint Set Union)
    
    Method 1: Union-Find is generally more efficient for this problem, particularly for dense graphs.
    Method 2: DFS is simpler and intuitive, especially useful for sparse graphs or when recursion is preferred.

    Both methods have the same input and output for easy comparison.
    """

    def countComponentsUnionFind(self, n: int, edges: List[List[int]]) -> int:
        """
        Approach 1: Union-Find
        This approach uses the Union-Find data structure to group nodes into connected components.
        As we iterate through the edges, we union the nodes, and at the end, the number of distinct sets
        (components) gives the answer.

        T.C. : O(E * α(n)) where E is the number of edges and α(n) is the inverse Ackermann function
        S.C. : O(n) for storing parent and rank arrays

        Input:
            - n : int : the number of nodes
            - edges : List[List[int]] : the list of undirected edges

        Output:
            - int : the number of connected components in the graph
        """
        parent = list(range(n))
        rank = [1] * n

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # path compression
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

        # Perform union for each edge
        for u, v in edges:
            union(u, v)

        # Count distinct roots which represent different components
        return len(set(find(x) for x in range(n)))

    def countComponentsDFS(self, n: int, edges: List[List[int]]) -> int:
        """
        Approach 2: Depth-First Search (DFS)
        This approach uses DFS to explore each component in the graph. Starting from each unvisited node,
        we perform a DFS to mark all reachable nodes, which belong to the same component.

        T.C. : O(V + E) where V is the number of vertices and E is the number of edges
        S.C. : O(V + E) for storing the adjacency list and the visited array

        Input:
            - n : int : the number of nodes
            - edges : List[List[int]] : the list of undirected edges

        Output:
            - int : the number of connected components in the graph
        """
        # Create adjacency list
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()

        def dfs(node):
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        # Count components using DFS
        count = 0
        for i in range(n):
            if i not in visited:
                count += 1
                dfs(i)

        return count

# Sample Inputs
n1 = 5
edges1 = [[0, 1], [1, 2], [3, 4]]

n2 = 5
edges2 = [[0, 1], [1, 2], [2, 3], [3, 4]]

# Expected Output : 2 and 1 respectively
print(Solution().countComponentsUnionFind(n1, edges1))  # Output: 2
print(Solution().countComponentsUnionFind(n2, edges2))  # Output: 1

print(Solution().countComponentsDFS(n1, edges1))  # Output: 2
print(Solution().countComponentsDFS(n2, edges2))  # Output: 1
