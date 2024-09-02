# CLONE GRAPH

# Problem number: 133
# Difficulty: Medium
# Tags: Graph, Depth-First Search, Breadth-First Search
# Link: https://leetcode.com/problems/clone-graph/

from typing import List, Optional, Dict

# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List['Node']] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    """
    This problem requires creating a deep copy (clone) of a connected, undirected graph.
    The solutions can use either Depth-First Search (DFS) or Breadth-First Search (BFS) 
    to traverse the graph and clone it node by node.

    The input is given as a reference to the first node of the graph, and the output 
    should be a reference to the first node of the cloned graph.

    We will implement two methods:
    1. DFS Approach
    2. BFS Approach

    Both methods have the same input and output formats to allow comparison.
    """

    def cloneGraph_DFS(self, node: Optional[Node]) -> Optional[Node]:
        """
        DFS approach to clone the graph.
        
        T.C. : O(n) where n is the number of nodes in the graph
        S.C. : O(n) due to recursion stack and the use of a hash map
        """
        def dfs(node: Node, visited: Dict[Node, Node]) -> Node:
            if node in visited:
                return visited[node]

            # Clone the node
            clone = Node(node.val)
            visited[node] = clone

            # Recursively clone all the neighbors
            for neighbor in node.neighbors:
                clone.neighbors.append(dfs(neighbor, visited))

            return clone
        
        if not node:
            return None
        
        return dfs(node, {})

    def cloneGraph_BFS(self, node: Optional[Node]) -> Optional[Node]:
        """
        BFS approach to clone the graph.
        
        T.C. : O(n) where n is the number of nodes in the graph
        S.C. : O(n) due to queue and the use of a hash map
        """
        if not node:
            return None

        from collections import deque

        visited = {}
        queue = deque([node])
        visited[node] = Node(node.val)

        while queue:
            current_node = queue.popleft()

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    # Clone the neighbor and put it in the visited map
                    visited[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)
                
                # Add the cloned neighbor to the current node's clone
                visited[current_node].neighbors.append(visited[neighbor])

        return visited[node]

# Best Method: DFS is often preferred for its simplicity in recursion, but both are optimal.

# Sample Inputs for Testing
adjList = [[2,4],[1,3],[2,4],[1,3]]
nodes = [Node(i) for i in range(1, 5)]
nodes[0].neighbors = [nodes[1], nodes[3]]
nodes[1].neighbors = [nodes[0], nodes[2]]
nodes[2].neighbors = [nodes[1], nodes[3]]
nodes[3].neighbors = [nodes[0], nodes[2]]

# Testing DFS Method
cloned_graph_dfs = Solution().cloneGraph_DFS(nodes[0])

# Testing BFS Method
cloned_graph_bfs = Solution().cloneGraph_BFS(nodes[0])

# Outputs should be structurally the same but different instances
print(cloned_graph_dfs.val == cloned_graph_bfs.val)  # Should output True
