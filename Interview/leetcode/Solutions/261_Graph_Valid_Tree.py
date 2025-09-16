# File: Leetcode/Solutions/261_Graph_Valid_Tree.py

"""
Problem Number: 261
Problem Name: Graph Valid Tree
Difficulty: Medium
Tags: Depth-First Search, Breadth-First Search, Union Find, Graph, Neetcode 150
Company (Frequency): Google (12), Facebook (10), Amazon (8)
Leetcode Link: https://leetcode.com/problems/graph-valid-tree/description/

DESCRIPTION

You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and a list of `edges` where `edges[i] = [ai, bi]` indicates that there is an undirected edge between nodes `ai` and `bi`.

Return `true` if the given graph is a valid tree, and `false` otherwise.

A graph is a valid tree if it satisfies two conditions:
1. It is connected.
2. It contains no cycles.

Alternatively, for a graph with `n` nodes and `n-1` edges:
1. It is connected. OR
2. It contains no cycles. (If it has no cycles and is connected, it must have n-1 edges. If it has n-1 edges and no cycles, it must be connected.)

Combined: A graph with `n` nodes is a tree if and only if it is connected and has exactly `n-1` edges.
Or, a graph with `n` nodes is a tree if and only if it has `n-1` edges and no cycles.

---

#### Example 1:

Input:
n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]

Output:

true

Explanation:

The graph forms a valid tree.

#### Example 2:

Input:
n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]

Output:

false

Explanation:

The graph contains a cycle (1-2-3-1).

#### Constraints:

  - `1 <= n <= 2000`
  - `0 <= edges.length <= 5000`
  - `edges[i].length == 2`
  - `0 <= ai, bi < n`
  - `ai != bi`
  - There are no duplicate edges.
  - The graph is undirected.
"""

import collections
from typing import List, Any

class Solution:
    """
    Thought Process:
    A graph is a valid tree if and only if it satisfies these two conditions:
    1. It is connected.
    2. It contains no cycles.

    Alternatively, for a graph with `n` nodes:
    If it has exactly `n-1` edges:
        - If it's connected, it must be a tree (no cycles).
        - If it has no cycles, it must be connected (and thus a tree).
    So, if `edges.length != n - 1`, it cannot be a tree. This is a quick initial check.

    After this check, we can use DFS or BFS to verify connectivity and detect cycles simultaneously.

    Input:
        n: int - The number of nodes in the graph.
        edges: List[List[int]] - A list of undirected edges.

    Output:
        bool - True if the graph is a valid tree, False otherwise.
    """

    def validTree_DFS(self, n: int, edges: List[List[int]]) -> bool:
        """
        Approach 1: DFS (Depth-First Search)
        Conditions to check:
        1. Number of edges must be exactly `n - 1`. If not, return False.
        2. Graph must be connected (all nodes reachable from a starting node).
        3. Graph must contain no cycles.

        We can combine connectivity and cycle detection using DFS:
        - Maintain a `visited` set to keep track of visited nodes.
        - During DFS, if we encounter a `visited` node that is not the direct `parent` of the current node,
          then a cycle is detected.
        - After DFS, check if all `n` nodes have been visited. If not, the graph is not connected.

        T.C.: O(N + E) - Where N is the number of nodes and E is the number of edges.
                          Each node and edge is visited at most once.
        S.C.: O(N + E) - For adjacency list and recursion stack (O(N) in worst case).
        """
        if len(edges) != n - 1:
            return False

        adj = collections.defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()

        def dfs(node: int, parent: int) -> bool:
            visited.add(node)

            for neighbor in adj[node]:
                if neighbor == parent:
                    continue # Ignore the parent, as it's the path we just came from
                
                if neighbor in visited:
                    return False # Cycle detected (visited node not parent)
                
                if not dfs(neighbor, node):
                    return False # Cycle detected in a deeper branch

            return True

        # Start DFS from node 0. If it returns False, a cycle was found.
        # After DFS, check if all nodes were visited to ensure connectivity.
        if not dfs(0, -1): # -1 as a placeholder for no parent for the root call
            return False
        
        # Check if all nodes are visited (connectivity)
        return len(visited) == n

    def validTree_BFS(self, n: int, edges: List[List[int]]) -> bool:
        """
        Approach 2: BFS (Breadth-First Search)
        Similar conditions as DFS:
        1. Number of edges must be `n - 1`.
        2. Connected and no cycles.

        Using BFS for cycle detection and connectivity:
        - Maintain a `visited` set.
        - Use a queue for BFS, storing `(node, parent)` pairs.
        - If a neighbor is `visited` and not the `parent`, a cycle is detected.
        - After BFS, check if all `n` nodes are visited.

        T.C.: O(N + E) - Where N is the number of nodes and E is the number of edges.
                          Each node and edge is visited at most once.
        S.C.: O(N + E) - For adjacency list and queue.
        """
        if len(edges) != n - 1:
            return False

        adj = collections.defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()
        queue = collections.deque([(0, -1)]) # (current_node, parent_node)
        visited.add(0)
        
        nodes_count = 0

        while queue:
            node, parent = queue.popleft()
            nodes_count += 1

            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in visited:
                    return False # Cycle detected
                
                visited.add(neighbor)
                queue.append((neighbor, node))
        
        # Check if all nodes were visited (connectivity) and no cycles were found
        return nodes_count == n

    def validTree(self, n: int, edges: List[List[int]], use_dfs: Any = True) -> bool:
        """
        Main entry point for the LeetCode problem.
        Allows choosing between recursive (DFS) and iterative (BFS) solutions.
        """
        if use_dfs:
            return self.validTree_DFS(n, edges)
        else:
            return self.validTree_BFS(n, edges)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    n1 = 5
    edges1 = [[0,1],[0,2],[0,3],[1,4]]
    # print_graph(build_graph(edges1)) # For debugging graph structure
    print(f"Test Case 1 Input: n={n1}, edges={edges1}")
    print(f"Test Case 1 Output (Recursive): {solution.validTree(n1, edges1, use_dfs=True)}")  # Expected: True
    print(f"Test Case 1 Output (Iterative): {solution.validTree(n1, edges1, use_dfs=False)}") # Expected: True
    print("-" * 30)

    # Test case 2
    n2 = 5
    edges2 = [[0,1],[1,2],[2,3],[1,3],[1,4]]
    print(f"Test Case 2 Input: n={n2}, edges={edges2}")
    print(f"Test Case 2 Output (Recursive): {solution.validTree(n2, edges2, use_dfs=True)}")  # Expected: False
    print(f"Test Case 2 Output (Iterative): {solution.validTree(n2, edges2, use_dfs=False)}") # Expected: False
    print("-" * 30)

    # Test case 3: Disconnected graph, but correct number of edges
    n3 = 4
    edges3 = [[0,1],[2,3]]
    print(f"Test Case 3 Input: n={n3}, edges={edges3}")
    print(f"Test Case 3 Output (Recursive): {solution.validTree(n3, edges3, use_dfs=True)}")  # Expected: False
    print(f"Test Case 3 Output (Iterative): {solution.validTree(n3, edges3, use_dfs=False)}") # Expected: False
    print("-" * 30)

    # Test case 4: Too few edges
    n4 = 3
    edges4 = [[0,1]]
    print(f"Test Case 4 Input: n={n4}, edges={edges4}")
    print(f"Test Case 4 Output (Recursive): {solution.validTree(n4, edges4, use_dfs=True)}")  # Expected: False
    print(f"Test Case 4 Output (Iterative): {solution.validTree(n4, edges4, use_dfs=False)}") # Expected: False
    print("-" * 30)

    # Test case 5: Single node, no edges
    n5 = 1
    edges5 = []
    print(f"Test Case 5 Input: n={n5}, edges={edges5}")
    print(f"Test Case 5 Output (Recursive): {solution.validTree(n5, edges5, use_dfs=True)}")  # Expected: True
    print(f"Test Case 5 Output (Iterative): {solution.validTree(n5, edges5, use_dfs=False)}") # Expected: True
    print("-" * 30)

    # Test case 6: Two nodes, one edge
    n6 = 2
    edges6 = [[0,1]]
    print(f"Test Case 6 Input: n={n6}, edges={edges6}")
    print(f"Test Case 6 Output (Recursive): {solution.validTree(n6, edges6, use_dfs=True)}")  # Expected: True
    print(f"Test Case 6 Output (Iterative): {solution.validTree(n6, edges6, use_dfs=False)}") # Expected: True
    print("-" * 30)

    # Test case 7: Two nodes, no edges (disconnected)
    n7 = 2
    edges7 = []
    print(f"Test Case 7 Input: n={n7}, edges={edges7}")
    print(f"Test Case 7 Output (Recursive): {solution.validTree(n7, edges7, use_dfs=True)}")  # Expected: False
    print(f"Test Case 7 Output (Iterative): {solution.validTree(n7, edges7, use_dfs=False)}") # Expected: False
    print("-" * 30)