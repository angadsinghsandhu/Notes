# TODO: new

# File: Leetcode/Solutions/Amazon/98_Validate_Binary_Search_Tree.py

"""
Problem Number: 98
Problem Name: Validate Binary Search Tree
Difficulty: Medium
Tags: Tree, Depth-First Search, Binary Search Tree, Binary Tree
Company (Frequency): Amazon (45)
Leetcode Link: https://leetcode.com/problems/validate-binary-search-tree/description/

DESCRIPTION

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

---

#### Example 1:
**Input:**
```plaintext
root = [2,1,3]
```

**Output:**
```plaintext
true
```

**Explanation:**  
The tree is a valid BST because the left subtree (1) is less than the root (2), and the right subtree (3) is greater than the root.

#### Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1
"""

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem involves validating whether a binary tree is a valid BST.
    - A valid BST requires that for every node, its left subtree contains only nodes with values less than the node's value, and its right subtree contains only nodes with values greater than the node's value.
    - We can use an in-order traversal to check if the tree is a valid BST. In a valid BST, an in-order traversal should yield values in strictly increasing order.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        bool - True if the tree is a valid BST, False otherwise.
    """

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """
        Approach:
        - Perform an in-order traversal of the tree.
        - Keep track of the last visited node's value.
        - Ensure that each node's value is greater than the last visited node's value.
        - If any node violates this condition, the tree is not a valid BST.

        T.C.: O(n) - We visit each node once.
        S.C.: O(h) - The space used by the recursion stack, where h is the height of the tree.
        """
        def in_order_traversal(node):
            nonlocal last_value_visited
            
            if node is None:
                return True
            
            # Traverse the left subtree
            if not in_order_traversal(node.left):
                return False
            
            # Check the current node's value
            if last_value_visited >= node.val:
                return False
            
            # Update the last visited value
            last_value_visited = node.val
            
            # Traverse the right subtree
            if not in_order_traversal(node.right):
                return False
            
            return True

        # Initialize the last visited value with negative infinity
        last_value_visited = float('-inf')
        
        # Start the in-order traversal from the root
        return in_order_traversal(root)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)
    print(solution.isValidBST(root1))  # Output: True

    # Test case 2
    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)
    print(solution.isValidBST(root2))  # Output: False