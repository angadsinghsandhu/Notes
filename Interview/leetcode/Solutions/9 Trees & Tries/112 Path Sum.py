# PATH SUM

# Problem number: 112
# Difficulty: Easy
# Tags: Tree, Depth-First Search, Binary Tree
# Link: https://leetcode.com/problems/path-sum/

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    This problem requires determining if there is a root-to-leaf path in a binary tree 
    such that the sum of the values along the path equals a given targetSum.
    We can solve this using a depth-first search (DFS) approach. The idea is to recursively 
    traverse the tree, subtracting the current node's value from the targetSum. 
    If we reach a leaf node and the remaining targetSum equals the node's value, 
    then such a path exists.

    T.C. : O(n) where n is the number of nodes in the tree
    S.C. : O(h) where h is the height of the tree (due to the recursive call stack)

    Input:
        - root : Optional[TreeNode] : root of the binary tree
        - targetSum : int : the target sum to check for a root-to-leaf path

    Output:
        - bool : True if such a path exists, otherwise False
    """
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # base case: if the node is None, return False
        if not root:
            return False
        
        # check if we've reached a leaf node
        if not root.left and not root.right:
            # return True if the targetSum equals the node's value
            return targetSum == root.val
        
        # recursively check left and right subtrees with the updated targetSum
        targetSum -= root.val
        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)

# Sample Inputs
root = TreeNode(5)
root.left = TreeNode(4)
root.right = TreeNode(8)
root.left.left = TreeNode(11)
root.left.left.left = TreeNode(7)
root.left.left.right = TreeNode(2)
root.right.left = TreeNode(13)
root.right.right = TreeNode(4)
root.right.right.right = TreeNode(1)
targetSum = 22

# Expected Output : True
print(Solution().hasPathSum(root, targetSum))
