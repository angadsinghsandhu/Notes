# File: Leetcode/Solutions/100_Same_Tree.py

"""
Problem Number: 100
Problem Name: Same Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (15), Microsoft (10), Google (8)
Leetcode Link: https://leetcode.com/problems/same-tree/description/

DESCRIPTION

Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

---

#### Example 1:

Input:
p = [1,2,3], q = [1,2,3]

Output:

true

#### Example 2:

Input:
p = [1,2], q = [1,null,2]

Output:

false

#### Example 3:

Input:
p = [1,2,1], q = [1,1,2]

Output:

false

#### Constraints:

  - The number of nodes in both trees is in the range `[0, 100]`.
  - `-104 <= Node.val <= 104`
"""

import collections
from typing import Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - To check if two binary trees are the same, we need to verify two conditions:
      1. They are structurally identical (same shape).
      2. Corresponding nodes have the same values.
    - This naturally lends itself to a traversal approach, comparing nodes at corresponding positions.

    Input:
        p: Optional[TreeNode] - The root of the first binary tree.
        q: Optional[TreeNode] - The root of the second binary tree.

    Output:
        bool - True if the trees are the same, False otherwise.
    """

    def isSameTree_Recursive(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 1: Recursive (Depth-First Search)
        - Base Cases:
          - If both `p` and `q` are None, they are identical (empty trees/subtrees), return True.
          - If one of `p` or `q` is None, but the other is not, they are not identical, return False.
          - If `p.val` is not equal to `q.val`, they are not identical, return False.
        - Recursive Step:
          - If none of the above base cases are met (i.e., both `p` and `q` are non-None and `p.val == q.val`),
            then recursively check if their left subtrees are the same AND their right subtrees are the same.
            The result is `isSameTree(p.left, q.left) AND isSameTree(p.right, q.right)`.

        T.C.: O(N) - Where N is the minimum number of nodes in the two trees. Each node is visited at most once.
        S.C.: O(H) - Where H is the height of the tree. In the worst case (skewed tree), H can be N.
        """
        # Both are null (base case for identical empty subtrees)
        if not p and not q:
            return True
        # One is null, the other is not (base case for structural difference)
        if not p or not q:
            return False
        # Values are different (base case for value difference)
        if p.val != q.val:
            return False

        # Recursively check left and right subtrees
        return self.isSameTree_Recursive(p.left, q.left) and \
               self.isSameTree_Recursive(p.right, q.right)

    def isSameTree_Iterative(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        Approach 2: Iterative (Breadth-First Search)
        - Use a queue (or two queues, one for each tree) to perform a level-order traversal.
        - At each step, dequeue nodes from both trees and compare them.
        - If at any point the nodes are not identical (one is None, the other not; or values differ), return False.
        - Enqueue their children in the same order.

        T.C.: O(N) - Where N is the minimum number of nodes in the two trees. Each node is processed once.
        S.C.: O(N) - In the worst case (a complete binary tree), the queue can hold up to N/2 nodes at one level.
        """
        queue = collections.deque([(p, q)])

        while queue:
            node_p, node_q = queue.popleft()

            # Case 1: Both nodes are None (end of a branch, matches)
            if not node_p and not node_q:
                continue # Continue to next pair in queue

            # Case 2: One node is None, the other is not (structural difference)
            if not node_p or not node_q:
                return False

            # Case 3: Both nodes are non-None, but their values differ
            if node_p.val != node_q.val:
                return False

            # If all checks pass for current nodes, enqueue their children
            queue.append((node_p.left, node_q.left))
            queue.append((node_p.right, node_q.right))

        return True # All nodes checked and found to be identical

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode], use_recursive: Any = True) -> bool:
        """
        Main entry point for the LeetCode problem.
        Allows choosing between recursive (DFS) and iterative (BFS) solutions.
        """
        if use_recursive:
            return self.isSameTree_Recursive(p, q)
        else:
            return self.isSameTree_Iterative(p, q)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1: Same trees
    p1 = build_tree([1, 2, 3])
    q1 = build_tree([1, 2, 3])
    print(f"Test Case 1 Input p: {tree_to_list(p1)}, q: {tree_to_list(q1)}")
    print(f"Test Case 1 Output (Recursive): {solution.isSameTree(p1, q1, use_recursive=True)}")  # Expected: True
    print(f"Test Case 1 Output (Iterative): {solution.isSameTree(p1, q1, use_recursive=False)}") # Expected: True
    print("-" * 30)

    # Test case 2: Different structure
    p2 = build_tree([1, 2])
    q2 = build_tree([1, None, 2])
    print(f"Test Case 2 Input p: {tree_to_list(p2)}, q: {tree_to_list(q2)}")
    print(f"Test Case 2 Output (Recursive): {solution.isSameTree(p2, q2, use_recursive=True)}")  # Expected: False
    print(f"Test Case 2 Output (Iterative): {solution.isSameTree(p2, q2, use_recursive=False)}") # Expected: False
    print("-" * 30)

    # Test case 3: Same structure, different values
    p3 = build_tree([1, 2, 1])
    q3 = build_tree([1, 1, 2])
    print(f"Test Case 3 Input p: {tree_to_list(p3)}, q: {tree_to_list(q3)}")
    print(f"Test Case 3 Output (Recursive): {solution.isSameTree(p3, q3, use_recursive=True)}")  # Expected: False
    print(f"Test Case 3 Output (Iterative): {solution.isSameTree(p3, q3, use_recursive=False)}") # Expected: False
    print("-" * 30)

    # Test case 4: Both empty
    p4 = build_tree([])
    q4 = build_tree([])
    print(f"Test Case 4 Input p: {tree_to_list(p4)}, q: {tree_to_list(q4)}")
    print(f"Test Case 4 Output (Recursive): {solution.isSameTree(p4, q4, use_recursive=True)}")  # Expected: True
    print(f"Test Case 4 Output (Iterative): {solution.isSameTree(p4, q4, use_recursive=False)}") # Expected: True
    print("-" * 30)

    # Test case 5: One empty, one not
    p5 = build_tree([1])
    q5 = build_tree([])
    print(f"Test Case 5 Input p: {tree_to_list(p5)}, q: {tree_to_list(q5)}")
    print(f"Test Case 5 Output (Recursive): {solution.isSameTree(p5, q5, use_recursive=True)}")  # Expected: False
    print(f"Test Case 5 Output (Iterative): {solution.isSameTree(p5, q5, use_recursive=False)}") # Expected: False
    print("-" * 30)

    # Test case 6: More complex, identical
    p6 = build_tree([1, 2, 3, 4, 5, 6, 7])
    q6 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print(f"Test Case 6 Input p: {tree_to_list(p6)}, q: {tree_to_list(q6)}")
    print(f"Test Case 6 Output (Recursive): {solution.isSameTree(p6, q6, use_recursive=True)}")  # Expected: True
    print(f"Test Case 6 Output (Iterative): {solution.isSameTree(p6, q6, use_recursive=False)}") # Expected: True
    print("-" * 30)

    # Test case 7: Complex, value difference
    p7 = build_tree([1, 2, 3, 4, 5, 6, 7])
    q7 = build_tree([1, 2, 3, 4, 5, 6, 8]) # Value 7 vs 8
    print(f"Test Case 7 Input p: {tree_to_list(p7)}, q: {tree_to_list(q7)}")
    print(f"Test Case 7 Output (Recursive): {solution.isSameTree(p7, q7, use_recursive=True)}")  # Expected: False
    print(f"Test Case 7 Output (Iterative): {solution.isSameTree(p7, q7, use_recursive=False)}") # Expected: False
    print("-" * 30)