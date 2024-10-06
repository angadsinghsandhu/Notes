# BINARY SEARCH TREE ITERATOR

# Problem number: 173
# Difficulty: Medium
# Tags: Stack, Tree, Binary Search Tree, Design, In-order Traversal
# Link: https://leetcode.com/problems/binary-search-tree-iterator/

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    """
    This class implements an iterator over a Binary Search Tree (BST) that returns the next node
    in in-order traversal. The in-order traversal visits nodes in ascending order for a BST.

    The iterator uses an explicit stack to maintain the traversal state and only pushes left
    children onto the stack until a leaf node is reached. Each call to next() will move the pointer 
    forward and return the current node's value, and hasNext() will check if there are more nodes left to visit.
    
    Time Complexity (next & hasNext): O(1) average per call
    Space Complexity: O(h) where h is the height of the tree (due to stack space)
    """

    def __init__(self, root: Optional[TreeNode]):
        """
        Initialize the stack and traverse to the leftmost node to start the in-order traversal.
        """
        self.stack = []
        self._push_left_nodes(root)

    def _push_left_nodes(self, node: Optional[TreeNode]):
        """
        Helper function to push all left children of a node onto the stack.
        """
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """
        Returns the next smallest number in the in-order traversal.
        Time Complexity: O(1) on average
        """
        # Pop the top node (the next in in-order)
        node = self.stack.pop()

        # If the node has a right child, push all its left children onto the stack
        if node.right:
            self._push_left_nodes(node.right)

        return node.val

    def hasNext(self) -> bool:
        """
        Returns whether we have a next smallest number in the in-order traversal.
        Time Complexity: O(1)
        """
        return len(self.stack) > 0


# Best Method: This is an optimal approach using O(h) space and O(1) time complexity on average for each call.

# Sample Inputs for Testing
# Constructing a BST with [7, 3, 15, None, None, 9, 20]
root = TreeNode(7)
root.left = TreeNode(3)
root.right = TreeNode(15)
root.right.left = TreeNode(9)
root.right.right = TreeNode(20)

# Testing the BSTIterator
iterator = BSTIterator(root)
print(iterator.next())    # return 3
print(iterator.next())    # return 7
print(iterator.hasNext()) # return True
print(iterator.next())    # return 9
print(iterator.hasNext()) # return True
print(iterator.next())    # return 15
print(iterator.hasNext()) # return True
print(iterator.next())    # return 20
print(iterator.hasNext()) # return False
