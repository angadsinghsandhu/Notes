# File: Leetcode/Solutions/100_Same_Tree.py

"""
Problem Number: 100
Problem Name: Same Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/same-tree/description/

DESCRIPTION

Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

---

#### Example 1:
**Input:**
```plaintext
p = [1,2,3], q = [1,2,3]
```

**Output:**
```plaintext
true
```

**Explanation:**  
Both trees are structurally identical, and all corresponding nodes have the same value.

#### Example 2:
**Input:**
```plaintext
p = [1,2], q = [1,null,2]
```

**Output:**
```plaintext
false
```

**Explanation:**  
The trees are not structurally identical.

#### Example 3:
**Input:**
```plaintext
p = [1,2,1], q = [1,1,2]
```

**Output:**
```plaintext
false
```

**Explanation:**  
The trees are not structurally identical, and the node values do not match.

#### Constraints:
- The number of nodes in both trees is in the range `[0, 100]`.
- `-10^4 <= Node.val <= 10^4`
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
    - The problem requires checking if two binary trees are identical in structure and node values.
    - We can solve this problem using both recursive and iterative approaches.

    Input:
        p: TreeNode - The root of the first binary tree.
        q: TreeNode - The root of the second binary tree.

    Output:
        bool - True if the trees are identical, False otherwise.
    """

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 1: Recursive Solution
        - Use a recursive function to compare the nodes of both trees.
        - If both nodes are None, they are identical.
        - If one node is None or their values are different, the trees are not identical.
        - Recursively check the left and right subtrees.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        # If both nodes are None, they are identical
        if not p and not q:
            return True
        # If one node is None or their values are different, the trees are not identical
        if not p or not q or p.val != q.val:
            return False
        # Recursively check the left and right subtrees
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

    def isSameTreeIterative(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 2: Iterative Solution
        - Use a stack to perform a depth-first traversal of both trees.
        - Compare the nodes at each step to ensure they are identical.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The stack uses space proportional to the height of the tree.
        """
        stack = [(p, q)]
        while stack:
            node1, node2 = stack.pop()
            # If both nodes are None, continue
            if not node1 and not node2:
                continue
            # If one node is None or their values are different, return False
            if not node1 or not node2 or node1.val != node2.val:
                return False
            # Add the left and right children to the stack
            stack.append((node1.left, node2.left))
            stack.append((node1.right, node2.right))
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

    # Test case 1 (Identical trees)
    p1 = create_tree([1, 2, 3])
    q1 = create_tree([1, 2, 3])
    print(solution.isSameTree(p1, q1))  # Output: True
    print(solution.isSameTreeIterative(p1, q1))  # Output: True

    # Test case 2 (Different structure)
    p2 = create_tree([1, 2])
    q2 = create_tree([1, None, 2])
    print(solution.isSameTree(p2, q2))  # Output: False
    print(solution.isSameTreeIterative(p2, q2))  # Output: False

    # Test case 3 (Different values)
    p3 = create_tree([1, 2, 1])
    q3 = create_tree([1, 1, 2])
    print(solution.isSameTree(p3, q3))  # Output: False
    print(solution.isSameTreeIterative(p3, q3))  # Output: False

    # Test case 4 (Empty trees)
    p4 = create_tree([])
    q4 = create_tree([])
    print(solution.isSameTree(p4, q4))  # Output: True
    print(solution.isSameTreeIterative(p4, q4))  # Output: True