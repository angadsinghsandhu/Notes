# VALIDATE BINARY SEARCH TREE

# Problem number: 98
# Difficulty: Medium
# Tags: Tree, Binary Search Tree, Depth-First Search, Recursion
# Link: https://leetcode.com/problems/validate-binary-search-tree/

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    This problem requires verifying if a binary tree is a valid Binary Search Tree (BST).
    A valid BST has the following properties:
    1. The left subtree of a node contains only nodes with keys less than the node's key.
    2. The right subtree of a node contains only nodes with keys greater than the node's key.
    3. Both left and right subtrees must also be binary search trees.
    
    We'll solve this problem using an in-order traversal and also a range-checking recursive approach.
    """

    def isValidBST_recursive(self, root: Optional[TreeNode]) -> bool:
        """
        Recursive approach with range checking to validate the BST.

        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(n) due to the recursion stack
        """

        def validate(node: TreeNode, low: float, high: float) -> bool:
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
        return validate(root, float('-inf'), float('inf'))

    def isValidBST_inorder(self, root: Optional[TreeNode]) -> bool:
        """
        In-order traversal approach to validate the BST.
        
        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(n) due to the use of an auxiliary stack
        """
        stack = []
        prev = None
        current = root
        
        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()

            if prev and current.val <= prev.val:
                return False

            prev = current
            current = current.right
        
        return True

# Best Method: The recursive approach is more intuitive, but the in-order traversal is a common method for validation.

# Sample Input for Testing
root1 = TreeNode(2)
root1.left = TreeNode(1)
root1.right = TreeNode(3)

root2 = TreeNode(5)
root2.left = TreeNode(1)
root2.right = TreeNode(4)
root2.right.left = TreeNode(3)
root2.right.right = TreeNode(6)

# Testing Recursive Method
sol = Solution()
print(sol.isValidBST_recursive(root1))  # Expected output: True
print(sol.isValidBST_recursive(root2))  # Expected output: False

# Testing In-Order Method
print(sol.isValidBST_inorder(root1))  # Expected output: True
print(sol.isValidBST_inorder(root2))  # Expected output: False
