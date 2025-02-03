# TODO: revisit

# File: Leetcode/Solutions/545_Boundary_of_Binary_Tree.py

"""
Problem Number: 545
Problem Name: Boundary of Binary Tree
Difficulty: Medium
Tags: Tree, Depth-First Search, Binary Tree
Company (Frequency): Amazon (15), Apple (10), Microsoft (8)
Leetcode Link: https://leetcode.com/problems/boundary-of-binary-tree/description/

DESCRIPTION

Given a binary tree, return the values of its boundary in anti-clockwise direction starting from the root. The boundary includes the left boundary, leaves, and right boundary in order without duplicate nodes. (The values of the nodes may still be duplicates.)

- The left boundary is defined as the path from the root to the left-most node.
- The right boundary is defined as the path from the root to the right-most node.
- If the root doesn't have a left subtree or right subtree, then the root itself is the left boundary or right boundary.
- The left-most node is defined as a leaf node you could reach when you always firstly travel to the left subtree if it exists. If not, travel to the right subtree. Repeat until you reach a leaf node.
- The right-most node is defined similarly with left and right exchanged.

---

#### Example 1:
**Input:**
```plaintext
  1
   \
    2
   / \
  3   4
```

**Output:**
```plaintext
[1, 3, 4, 2]
```

**Explanation:**  
- The root doesn't have a left subtree, so the root itself is the left boundary.
- The leaves are nodes 3 and 4.
- The right boundary is nodes 1, 2, 4. Note the anti-clockwise direction means you should output the reversed right boundary.
- The final result is `[1, 3, 4, 2]`.

#### Example 2:
**Input:**
```plaintext
    ____1_____
   /          \
  2            3
 / \          /
4   5        6
   / \      / \
  7   8    9  10
```

**Output:**
```plaintext
[1, 2, 4, 7, 8, 9, 10, 6, 3]
```

**Explanation:**  
- The left boundary is nodes 1, 2, 4.
- The leaves are nodes 4, 7, 8, 9, 10.
- The right boundary is nodes 1, 3, 6, 10.
- The final result is `[1, 2, 4, 7, 8, 9, 10, 6, 3]`.

#### Constraints:
- `0 <= n <= 1000`
- `-10^4 <= Node.val <= 10^4`
"""

from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem requires traversing the boundary of a binary tree in an anti-clockwise direction.
    - The boundary includes the left boundary (excluding leaves), the leaves (from left to right), and the right boundary (excluding leaves, in reverse order).
    - We can break the problem into three parts: collecting the left boundary, collecting the leaves, and collecting the right boundary.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        List[int] - The values of the boundary nodes in anti-clockwise order.
    """

    def boundaryOfBinaryTree(self, root: TreeNode) -> List[int]:
        """
        Approach:
        - Handle edge cases where the tree is empty or has only one node.
        - Collect the left boundary (excluding leaves).
        - Collect all leaves in left-to-right order.
        - Collect the right boundary (excluding leaves, in reverse order).
        - Combine the results into a single list.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(n) - Space for the result list and recursion stack.
        """
        if not root:
            return []

        boundary = []

        # Add the root if it's not a leaf
        if not self._is_leaf(root):
            boundary.append(root.val)

        # Add the left boundary (excluding leaves)
        self._add_left_boundary(root.left, boundary)

        # Add all leaves
        self._add_leaves(root, boundary)

        # Add the right boundary (excluding leaves, in reverse order)
        self._add_right_boundary(root.right, boundary)

        return boundary

    def _is_leaf(self, node: TreeNode) -> bool:
        """Helper function to check if a node is a leaf."""
        return not node.left and not node.right

    def _add_left_boundary(self, node: TreeNode, boundary: List[int]) -> None:
        """Helper function to add the left boundary (excluding leaves)."""
        if not node or self._is_leaf(node):
            return

        boundary.append(node.val)

        # Prefer the left child if it exists; otherwise, go to the right child
        if node.left:
            self._add_left_boundary(node.left, boundary)
        else:
            self._add_left_boundary(node.right, boundary)

    def _add_leaves(self, node: TreeNode, boundary: List[int]) -> None:
        """Helper function to add all leaves in left-to-right order."""
        if not node:
            return

        if self._is_leaf(node):
            boundary.append(node.val)
            return

        # Recursively add leaves from left and right subtrees
        self._add_leaves(node.left, boundary)
        self._add_leaves(node.right, boundary)

    def _add_right_boundary(self, node: TreeNode, boundary: List[int]) -> None:
        """Helper function to add the right boundary (excluding leaves, in reverse order)."""
        if not node or self._is_leaf(node):
            return

        # Prefer the right child if it exists; otherwise, go to the left child
        if node.right:
            self._add_right_boundary(node.right, boundary)
        else:
            self._add_right_boundary(node.left, boundary)

        # Add the node's value after visiting its children (reverse order)
        boundary.append(node.val)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to create a binary tree from a list of values
    def create_tree(values: List[int], index: int = 0) -> TreeNode:
        if index >= len(values) or values[index] is None:
            return None
        root = TreeNode(values[index])
        root.left = create_tree(values, 2 * index + 1)
        root.right = create_tree(values, 2 * index + 2)
        return root

    # Test case 1
    tree1 = create_tree([1, None, 2, None, None, 3, 4])
    print(solution.boundaryOfBinaryTree(tree1))  # Output: [1, 3, 4, 2]

    # Test case 2
    tree2 = create_tree([1, 2, 3, 4, 5, None, 6, None, None, 7, 8, 9, 10])
    print(solution.boundaryOfBinaryTree(tree2))  # Output: [1, 2, 4, 7, 8, 9, 10, 6, 3]

    # Test case 3 (Single node)
    tree3 = create_tree([1])
    print(solution.boundaryOfBinaryTree(tree3))  # Output: [1]