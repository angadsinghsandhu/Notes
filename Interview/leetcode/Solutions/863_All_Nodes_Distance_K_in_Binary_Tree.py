# TODO: revisit

# File: Leetcode/Solutions/Amazon/863_All_Nodes_Distance_K_in_Binary_Tree.py

"""
Problem Number: 863
Problem Name: All Nodes Distance K in Binary Tree
Difficulty: Medium
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (35)
Leetcode Link: https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/description/

DESCRIPTION

Given the root of a binary tree, the value of a target node "target", and an integer k, return an array of the values of all nodes that have a distance k from the target node.

You can return the answer in any order.

---

#### Example 1:
**Input:**
```plaintext
root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
```

**Output:**
```plaintext
[7,4,1]
```

**Explanation:**  
The nodes that are a distance 2 from the target node (with value 5) have values 7, 4, and 1.

#### Constraints:
- The number of nodes in the tree is in the range [1, 500].
- 0 <= Node.val <= 500
- All the values Node.val are unique.
- target is the value of one of the nodes in the tree.
- 0 <= k <= 1000
"""

from typing import List
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    """
    Thought Process:
    - The problem involves finding all nodes that are at a distance k from a given target node in a binary tree.
    - Since the tree is not a graph, we need to first map the parent of each node to allow traversal in both directions (upwards and downwards).
    - We can use a BFS approach starting from the target node to find all nodes at distance k.

    Input:
        root: TreeNode - The root of the binary tree.
        target: TreeNode - The target node.
        k: int - The distance from the target node.

    Output:
        List[int] - A list of node values that are at distance k from the target node.
    """

    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        """
        Approach:
        - Use a BFS approach to traverse the tree starting from the target node.
        - First, map the parent of each node to allow traversal in both directions.
        - Then, perform a BFS starting from the target node, keeping track of the distance from the target.
        - When the distance equals k, add the node's value to the result.

        T.C.: O(n) - We visit each node once.
        S.C.: O(n) - We store the parent map and the queue for BFS.
        """
        # Helper function to map parents of each node
        def map_parents(node, parent):
            if node:
                parent_map[node] = parent
                map_parents(node.left, node)
                map_parents(node.right, node)

        # Initialize the parent map
        parent_map = {}
        map_parents(root, None)

        # Initialize the queue for BFS
        queue = deque([(target, 0)])  # (node, distance from target)
        visited = set()
        result = []

        # Perform BFS
        while queue:
            node, distance = queue.popleft()

            # If the node is already visited, skip it
            if node in visited:
                continue

            # Mark the node as visited
            visited.add(node)

            # If the distance equals k, add the node's value to the result
            if distance == k:
                result.append(node.val)
                continue

            # Add the left child to the queue if it exists
            if node.left:
                queue.append((node.left, distance + 1))

            # Add the right child to the queue if it exists
            if node.right:
                queue.append((node.right, distance + 1))

            # Add the parent to the queue if it exists
            if parent_map[node]:
                queue.append((parent_map[node], distance + 1))

        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = TreeNode(3)
    root1.left = TreeNode(5)
    root1.right = TreeNode(1)
    root1.left.left = TreeNode(6)
    root1.left.right = TreeNode(2)
    root1.right.left = TreeNode(0)
    root1.right.right = TreeNode(8)
    root1.left.right.left = TreeNode(7)
    root1.left.right.right = TreeNode(4)

    target1 = root1.left  # Node with value 5
    k1 = 2
    print(solution.distanceK(root1, target1, k1))  # Output: [7, 4, 1]

    # Test case 2
    root2 = TreeNode(1)
    target2 = root2  # Node with value 1
    k2 = 3
    print(solution.distanceK(root2, target2, k2))  # Output: []