from typing import List, Optional

############ Array Helper Functions ############
# Helper function to pretty print a 2D matrix
def print_matrix(matrix: List[List[int]]) -> None:
    """
    Helper function to print a 2D matrix.
    
    Args:
        matrix (List[List[int]]): The matrix to print.
    """
    for row in matrix:
        print(" ".join(map(str, row)))
    print()

############ Tree Helper Functions ############
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Helper function to build a tree from a list (for testing purposes)
def build_tree(nodes: List[Optional[int]]) -> Optional[TreeNode]:
    if not nodes:
        return None

    root_val = nodes[0]
    if root_val is None:
        return None
    
    root = TreeNode(root_val)
    queue = [root]
    i = 1
    while queue and i < len(nodes):
        current = queue.pop(0)
        
        # Left child
        if i < len(nodes) and nodes[i] is not None:
            current.left = TreeNode(nodes[i])
            queue.append(current.left)
        i += 1
        
        # Right child
        if i < len(nodes) and nodes[i] is not None:
            current.right = TreeNode(nodes[i])
            queue.append(current.right)
        i += 1
    return root

# Helper function to print the tree in level order (for testing purposes)
def print_tree(node: Optional[TreeNode]) -> None:
    if not node:
        print("None")
        return
    queue = [node]
    while queue:
        current = queue.pop(0)
        if current:
            print(current.val, end=' ')
            queue.append(current.left)
            queue.append(current.right)
        else:
            print("None", end=' ')
    print()

################ Graph Helper Functions ############
# Helper function to print a graph represented as an adjacency list
def print_graph(graph: List[List[int]]) -> None:
    """
    Helper function to print a graph represented as an adjacency list.
    
    Args:
        graph (List[List[int]]): The graph to print.
    """
    for i, edges in enumerate(graph):
        print(f"{i}: {' '.join(map(str, edges))}")
    print()

# Helper function to build a graph from a list of edges
def build_graph(edges: List[List[int]]) -> List[List[int]]:
    """
    Helper function to build a graph from a list of edges.
    
    Args:
        edges (List[List[int]]): List of edges where each edge is represented as [u, v].
    
    Returns:
        List[List[int]]: Adjacency list representation of the graph.
    """
    max_node = max(max(u, v) for u, v in edges)
    graph = [[] for _ in range(max_node + 1)]
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # Assuming undirected graph
    
    return graph
