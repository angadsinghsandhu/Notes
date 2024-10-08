# BINARY TREE MAXIMUM PATH SUM

# Problem number: 124
# Difficulty: Hard
# Tags: Binary Tree, Depth-First Search, Dynamic Programming
# Link: https://leetcode.com/problems/binary-tree-maximum-path-sum/

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    The problem requires us to find the maximum path sum in a binary tree.
    The path can start and end at any node, and we need to find the path 
    with the largest sum.
    
    We can solve this using a Depth-First Search (DFS) approach, where for each 
    node, we calculate the maximum path sum that passes through it by recursively 
    computing the maximum contributions from its left and right subtrees.

    We keep track of the global maximum path sum as we traverse the tree.
    """

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """
        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(h) where h is the height of the tree due to recursion stack
        
        Best method: DFS with dynamic programming to keep track of the maximum 
        path sum during the traversal. This allows us to efficiently compute 
        the maximum path sum.
        """
        # Initialize the maximum path sum to a very small value
        self.max_sum = float('-inf')
        
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            # Recursively calculate the maximum path sum for the left and right subtrees
            left_gain = max(dfs(node.left), 0)  # Max sum on the left, ignore negatives
            right_gain = max(dfs(node.right), 0)  # Max sum on the right, ignore negatives

            # Calculate the path sum with the current node as the highest node (root of the path)
            current_max_path = node.val + left_gain + right_gain

            # Update the global maximum path sum
            self.max_sum = max(self.max_sum, current_max_path)

            # Return the maximum sum of the path that can be extended to the parent
            return node.val + max(left_gain, right_gain)

        # Start DFS traversal from the root
        dfs(root)

        return self.max_sum

# Best Method: DFS approach with dynamic programming for tracking the maximum path sum.

# Example Usage:
# Input: root = [1,2,3]
# Tree structure: 1 -> 2, 3
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
result = Solution().maxPathSum(root)
print(result)  # Output: 6

# Input: root = [-10,9,20,null,null,15,7]
root = TreeNode(-10)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)
result = Solution().maxPathSum(root)
print(result)  # Output: 42
