# File: Leetcode/Solutions/Amazon/297_Serialize_and_Deserialize_Binary_Tree.py

"""
Problem Number: 297
Problem Name: Serialize and Deserialize Binary Tree
Difficulty: Hard
Tags: Tree, Depth-First Search, Breadth-First Search, Design, String, Binary Tree
Company (Frequency): Amazon (45)
Leetcode Link: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/description/

DESCRIPTION

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

---

#### Example 1:
**Input:**
```plaintext
root = [1,2,3,null,null,4,5]
```

**Output:**
```plaintext
[1,2,3,null,null,4,5]
```

#### Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -1000 <= Node.val <= 1000
"""

from typing import Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    """
    Thought Process:
    - The problem involves converting a binary tree into a string (serialization) and reconstructing the tree from the string (deserialization).
    - A preorder traversal (DFS) approach is suitable for serialization because it captures the structure of the tree in a top-down manner.
    - For deserialization, we can use the same preorder traversal to reconstruct the tree from the serialized string.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        str - The serialized string representation of the tree.
        TreeNode - The root of the deserialized binary tree.
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        """
        Approach:
        - Use a preorder traversal to serialize the tree.
        - For each node, append its value to the result string.
        - If a node is None, append a special marker (e.g., "#") to represent null.
        - Separate values with a delimiter (e.g., ",").

        T.C.: O(n) - We visit each node once.
        S.C.: O(n) - The serialized string stores all node values.
        """
        if not root:
            return ""
        
        result = []
        def preorder(node):
            if not node:
                result.append("#")
                return
            result.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        preorder(root)
        return ",".join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """
        Approach:
        - Split the serialized string into a list of values.
        - Use a preorder traversal to reconstruct the tree.
        - If a value is the special marker ("#"), return None.
        - Otherwise, create a TreeNode with the value and recursively set its left and right children.

        T.C.: O(n) - We process each value once.
        S.C.: O(n) - The recursion stack can go up to the height of the tree.
        """
        if not data:
            return None
        
        values = data.split(",")
        def build_tree():
            if not values:
                return None
            val = values.pop(0)
            if val == "#":
                return None
            node = TreeNode(int(val))
            node.left = build_tree()
            node.right = build_tree()
            return node
        
        return build_tree()

# Run and print sample test cases
if __name__ == "__main__":
    codec = Codec()

    # Test case 1
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.right.left = TreeNode(4)
    root1.right.right = TreeNode(5)

    serialized = codec.serialize(root1)
    print(serialized)  # Output: "1,2,#,#,3,4,#,#,5,#,#"

    deserialized = codec.deserialize(serialized)
    print(codec.serialize(deserialized))  # Output: "1,2,#,#,3,4,#,#,5,#,#"

    # Test case 2
    root2 = None
    serialized = codec.serialize(root2)
    print(serialized)  # Output: ""

    deserialized = codec.deserialize(serialized)
    print(codec.serialize(deserialized))  # Output: ""