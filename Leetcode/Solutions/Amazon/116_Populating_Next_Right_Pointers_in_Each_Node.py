# TODO: new

# File: Leetcode/Solutions/Amazon/116_Populating_Next_Right_Pointers_in_Each_Node.py

"""
Problem Number: 116
Problem Name: Populating Next Right Pointers in Each Node
Difficulty: Medium
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (40)
Leetcode Link: https://leetcode.com/problems/populating-next-right-pointers-in-each-node/description/

DESCRIPTION

You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}

Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.

---

#### Example 1:
**Input:**
```plaintext
root = [1,2,3,4,5,6,7]
```

**Output:**
```plaintext
[1,#,2,3,#,4,5,6,7,#]
```

**Explanation:**  
Given the above perfect binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.

#### Constraints:
- The number of nodes in the tree is in the range [0, 2^12 - 1].
- -1000 <= Node.val <= 1000

---

#### Follow-up:
- You may only use constant extra space.
- The recursive approach is fine. You may assume implicit stack space does not count as extra space for this problem.
"""

from typing import Optional

# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution:
    """
    Thought Process:
    - The problem involves connecting each node to its next right node in a perfect binary tree.
    - A perfect binary tree has all leaves on the same level, and every parent has exactly two children.
    - We can use a level-order traversal (BFS) to connect nodes at the same level.
    - Alternatively, we can use a recursive approach to connect nodes level by level.

    Input:
        root: Node - The root of the perfect binary tree.

    Output:
        Node - The root of the modified tree with next pointers populated.
    """

    def connect(self, root: Optional[Node]) -> Optional[Node]:
        """
        Approach:
        - Use a level-order traversal (BFS) to connect nodes at the same level.
        - For each level, connect the next pointer of each node to its right neighbor.
        - If a node is the last in its level, its next pointer should be set to NULL.

        T.C.: O(n) - We visit each node once.
        S.C.: O(1) - We use constant extra space (excluding the recursion stack).
        """
        if not root:
            return root
        
        # Start with the root node
        leftmost = root
        
        # Traverse each level
        while leftmost.left:
            # Traverse the current level and connect the next pointers
            head = leftmost
            while head:
                # Connect the left child to the right child
                head.left.next = head.right
                
                # Connect the right child to the next node's left child (if it exists)
                if head.next:
                    head.right.next = head.next.left
                
                # Move to the next node in the current level
                head = head.next
            
            # Move to the next level
            leftmost = leftmost.left
        
        return root

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = Node(1)
    root1.left = Node(2)
    root1.right = Node(3)
    root1.left.left = Node(4)
    root1.left.right = Node(5)
    root1.right.left = Node(6)
    root1.right.right = Node(7)
    
    # Connect next pointers
    solution.connect(root1)
    
    # Print the result (level order traversal with next pointers)
    def print_tree(root: Node):
        result = []
        while root:
            current = root
            while current:
                result.append(current.val)
                current = current.next
            result.append('#')
            root = root.left
        return result
    
    print(print_tree(root1))  # Output: [1, '#', 2, 3, '#', 4, 5, 6, 7, '#']