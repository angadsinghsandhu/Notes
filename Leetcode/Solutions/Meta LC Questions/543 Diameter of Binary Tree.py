# DIAMETER OF BINARY TREE

# Problem number: 543
# Difficulty: Easy
# Tags: Tree, Depth-First Search, Binary Tree, Recursion
# Link: https://leetcode.com/problems/diameter-of-binary-tree/

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    This problem requires calculating the diameter of a binary tree. The diameter is defined as
    the length of the longest path between any two nodes in the tree. The path may or may not
    pass through the root.
    
    We will solve this problem using Depth-First Search (DFS) to compute the diameter at each node.
    
    Two methods will be implemented:
    1. DFS Recursive Approach
    2. Optimized Recursive DFS with Single Traversal
    
    Both methods will return the length of the diameter.
    """

    def diameterOfBinaryTree_DFS(self, root: Optional[TreeNode]) -> int:
        """
        This is the standard DFS approach where we calculate the height of each subtree 
        and use the heights of left and right children to calculate the diameter.
        
        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(n) due to the recursion stack in the worst case for skewed trees
        """
        def height(node: TreeNode) -> int:
            if not node:
                return 0
            left_height = height(node.left)
            right_height = height(node.right)
            self.diameter = max(self.diameter, left_height + right_height)
            return 1 + max(left_height, right_height)
        
        self.diameter = 0
        height(root)
        return self.diameter

    def diameterOfBinaryTree_Optimized(self, root: Optional[TreeNode]) -> int:
        """
        Optimized DFS where we calculate the height of subtrees while updating the diameter in one pass.
        
        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(n) for the recursion stack (or O(h) where h is the height of the tree)
        """
        def dfs(node: TreeNode) -> int:
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            # Update the diameter with the current path through this node
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)
        
        self.diameter = 0
        dfs(root)
        return self.diameter

# Best Method: The Optimized DFS is the preferred solution as it computes the diameter in a single traversal, minimizing time complexity.

# Sample Inputs for Testing
# Example 1:
root1 = TreeNode(1)
root1.left = TreeNode(2)
root1.right = TreeNode(3)
root1.left.left = TreeNode(4)
root1.left.right = TreeNode(5)

# Example 2:
root2 = TreeNode(1)
root2.left = TreeNode(2)

# Testing DFS Method
sol = Solution()
print(sol.diameterOfBinaryTree_DFS(root1))  # Output: 3
print(sol.diameterOfBinaryTree_DFS(root2))  # Output: 1

# Testing Optimized DFS Method
sol = Solution()
print(sol.diameterOfBinaryTree_Optimized(root1))  # Output: 3
print(sol.diameterOfBinaryTree_Optimized(root2))  # Output: 1
