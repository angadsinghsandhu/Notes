# File: Leetcode/Solutions/101_Symmetric_Tree.py

"""
Problem Number: 101
Problem Name: Symmetric Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/symmetric-tree/description/

DESCRIPTION

Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

---

#### Example 1:
**Input:**
```plaintext
    1
   / \
  2   2
 / \ / \
3  4 4  3
```

**Output:**
```plaintext
true
```

**Explanation:**  
The binary tree is symmetric around its center.

#### Example 2:
**Input:**
```plaintext
    1
   / \
  2   2
   \   \
    3    3
```

**Output:**
```plaintext
false
```

**Explanation:**  
The binary tree is not symmetric around its center.

#### Constraints:
- The number of nodes in the tree is in the range `[1, 1000]`.
- `-100 <= Node.val <= 100`

#### Follow-up:
Can you solve it both recursively and iteratively?
"""

from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem requires checking if a binary tree is symmetric around its center.
    - A tree is symmetric if the left subtree is a mirror reflection of the right subtree.
    - We can solve this problem using both recursive and iterative approaches.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        bool - True if the tree is symmetric, False otherwise.
    """

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 1: Recursive Solution
        - Use a helper function to compare the left and right subtrees.
        - The helper function checks if the left subtree of the first node is a mirror of the right subtree of the second node, and vice versa.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        def is_mirror(node1: Optional[TreeNode], node2: Optional[TreeNode]) -> bool:
            # If both nodes are None, they are symmetric
            if not node1 and not node2:
                return True
            # If one of the nodes is None or their values are different, they are not symmetric
            if not node1 or not node2 or node1.val != node2.val:
                return False
            # Recursively check the outer and inner pairs of subtrees
            return is_mirror(node1.left, node2.right) and is_mirror(node1.right, node2.left)

        # Start the recursion by comparing the root with itself
        return is_mirror(root, root)

    def isSymmetricIterative(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 2: Iterative Solution
        - Use a queue to perform a level-order traversal.
        - Compare nodes in pairs to check if they are mirrors of each other.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(n) - The queue can hold up to n/2 nodes in the worst case.
        """
        if not root:
            return True

        from collections import deque
        queue = deque()
        queue.append(root.left)
        queue.append(root.right)

        while queue:
            node1 = queue.popleft()
            node2 = queue.popleft()

            # If both nodes are None, continue
            if not node1 and not node2:
                continue
            # If one of the nodes is None or their values are different, return False
            if not node1 or not node2 or node1.val != node2.val:
                return False

            # Add the outer pair (left of node1 and right of node2)
            queue.append(node1.left)
            queue.append(node2.right)

            # Add the inner pair (right of node1 and left of node2)
            queue.append(node1.right)
            queue.append(node2.left)

        return True

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to create a binary tree from a list of values
    def create_tree(values: List[int], index: int = 0) -> Optional[TreeNode]:
        if index >= len(values) or values[index] is None:
            return None
        root = TreeNode(values[index])
        root.left = create_tree(values, 2 * index + 1)
        root.right = create_tree(values, 2 * index + 2)
        return root

    # Test case 1 (Symmetric tree)
    tree1 = create_tree([1, 2, 2, 3, 4, 4, 3])
    print(solution.isSymmetric(tree1))  # Output: True
    print(solution.isSymmetricIterative(tree1))  # Output: True

    # Test case 2 (Asymmetric tree)
    tree2 = create_tree([1, 2, 2, None, 3, None, 3])
    print(solution.isSymmetric(tree2))  # Output: False
    print(solution.isSymmetricIterative(tree2))  # Output: False

    # Test case 3 (Single node)
    tree3 = create_tree([1])
    print(solution.isSymmetric(tree3))  # Output: True
    print(solution.isSymmetricIterative(tree3))  # Output: True

    # Test case 4 (Empty tree)
    tree4 = create_tree([])
    print(solution.isSymmetric(tree4))  # Output: True
    print(solution.isSymmetricIterative(tree4))  # Output: True