import collections
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
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val: int = val
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right

# Helper function to build a tree from a list (for testing purposes)
def build_tree(nodes: List[Optional[int]]) -> Optional[TreeNode]:
    if not nodes or nodes[0] is None: # Combine conditions for empty list or None root
        return None

    root = TreeNode(nodes[0])
    # Use collections.deque for O(1) appends and pops
    queue = collections.deque([root])
    i = 1
    while queue and i < len(nodes):
        current = queue.popleft() # O(1) operation

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

    queue = collections.deque([node]) # O(1) operations
    result_str = []

    while queue:
        current = queue.popleft()
        if current:
            result_str.append(str(current.val))
            queue.append(current.left)
            queue.append(current.right)
        else:
            result_str.append("None")

    # Optional: Trim trailing 'None's if you want a LeetCode-like representation
    # For a full visual representation including trailing Nones on the last level,
    # you might keep them. The current implementation effectively does this.

    print(" ".join(result_str))
    # The extra print() in the original `print_matrix` and `print_graph`
    # is for a newline. Here, `print(" ".join(result_str))` already adds a newline.
    # If you want an *additional* newline like your other print functions, add print()
    # print() 

# Helper function to convert a tree to a list for verification
def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []

    result = []
    q = collections.deque([root])

    while q:
        node = q.popleft()
        if node:
            result.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            result.append(None)
            # If this is None, but there are still non-None nodes to be processed
            # (i.e., this isn't the end of the useful part of the tree representation)
            # we need to add its "children" (which are None) to maintain structure.
            # Otherwise, if it's trailing Nones, we stop.
            # This logic is a bit tricky; a simpler approach is to add all Nones and then trim.
            q.append(None) # These Nones will be processed and ignored
            q.append(None) # but they maintain queue size for a level if we did level_size logic

    # Remove trailing None values to match LeetCode's compact representation
    # Keep removing None from the end as long as there are Nones
    while result and result[-1] is None:
        result.pop()
    
    return result

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
    if not edges:
        return [] # Return empty list if no edges

    # A more robust way to find max_node, in case nodes are not consecutive
    # and to handle cases like [[0,1]] where max_node based on values could be small.
    # This approach ensures all existing node indices are considered.
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)

    if not all_nodes: # This would happen only if edges was empty, already handled above
        return []

    max_node = max(all_nodes)

    graph = [[] for _ in range(max_node + 1)]

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # Assuming undirected graph

    return graph
