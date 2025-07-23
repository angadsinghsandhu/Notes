# SERIALIZE AND DESERIALIZE BINARY TREE

# Problem number: 297
# Difficulty: Hard
# Tags: Tree, Binary Tree, Breadth-First Search, Depth-First Search
# Link: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
# Similar Problems: 449 (Serialize and Deserialize BST)

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
# Definition for a binary tree node is already provided by LeetCode, so we don't redefine it.

from typing import Optional
from collections import deque

class Codec:
    """
    This problem requires converting a binary tree into a string format and vice versa.
    Serialization is the process of converting the tree into a string.
    Deserialization is the reverse process that reconstructs the tree from the string.
    
    The problem can be solved using both Breadth-First Search (BFS) and Depth-First Search (DFS).
    
    We will use BFS for serialization and deserialization, which will help us handle the 
    tree level by level.
    
    The tree is serialized into a comma-separated string, where 'null' denotes missing nodes.
    """

    def serialize(self, root: Optional['TreeNode']) -> str:
        """
        Serializes a tree to a single string using BFS.
        
        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(n) due to the queue used in BFS and the string storage
        """
        if not root:
            return 'null'
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append('null')
        
        return ','.join(result)

    def deserialize(self, data: str) -> Optional['TreeNode']:
        """
        Deserializes the string back to a tree using BFS.
        
        T.C. : O(n) where n is the number of nodes in the tree
        S.C. : O(n) due to the queue used in BFS and the string storage
        """
        if data == 'null':
            return None
        
        nodes = data.split(',')
        root = TreeNode(int(nodes[0]))
        queue = deque([root])
        index = 1
        
        while queue:
            node = queue.popleft()
            
            if nodes[index] != 'null':
                node.left = TreeNode(int(nodes[index]))
                queue.append(node.left)
            index += 1
            
            if nodes[index] != 'null':
                node.right = TreeNode(int(nodes[index]))
                queue.append(node.right)
            index += 1
        
        return root

# Best Method: The BFS approach is ideal for level-by-level traversal and can handle sparse trees efficiently.

# Sample Usage:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
