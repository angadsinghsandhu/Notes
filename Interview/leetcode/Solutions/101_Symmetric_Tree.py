# File: Leetcode/Solutions/Tree/101_Symmetric_Tree.py

"""
Problem Number: 101
Problem Name: Symmetric Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Frequently asked in interviews, a fundamental tree problem.
Leetcode Link: <https://leetcode.com/problems/symmetric-tree/description/>

DESCRIPTION

Given the `root` of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

---

#### Example 1:

Input:
root = [1,2,2,3,4,4,3]

Output:
true

Explanation:
The tree is symmetric:
      1
     / \
    2   2
   / \ / \
  3  4 4  3

---

#### Example 2:

Input:
root = [1,2,2,null,3,null,3]

Output:
false

Explanation:
The tree is not symmetric:
      1
     / \
    2   2
     \   \
      3   3
(The left subtree has a right child but no left child, while the right subtree has a right child but no left child.
For symmetry, the left subtree's right child should mirror the right subtree's left child. Here, it fails.)

---

#### Constraints:

- The number of nodes in the tree is in the range `[1, 1000]`.
- `-100 <= Node.val <= 100`

Follow up: Could you solve it both recursively and iteratively?
"""

from typing import Optional
import collections
from helpers import TreeNode, build_tree

class Solution:
    """
    Thought Process for Symmetric Tree:

    A binary tree is symmetric if it reads the same forwards and backwards, meaning its left subtree is a mirror image of its right subtree. This mirror property must hold true for all levels of the tree.

    Key Idea for Mirror Symmetry:
    To check if two trees (or subtrees) `t1` and `t2` are mirrors of each other, the following conditions must be met:
    1. Both `t1` and `t2` must be `None` (empty subtrees) - they are symmetric.
    2. If one of them is `None` and the other is not - they are NOT symmetric.
    3. If both are non-`None`:
       a. Their values must be equal (`t1.val == t2.val`).
       b. The left child of `t1` must be a mirror of the right child of `t2` (`is_mirror(t1.left, t2.right)`).
       c. The right child of `t1` must be a mirror of the left child of `t2` (`is_mirror(t1.right, t2.left)`).
       All three sub-conditions (a, b, c) must be true.

    ---

    Approach 1: Recursive Depth-First Search (DFS) - Optimal

    The problem's definition naturally leads to a recursive solution. We need a helper function that compares two nodes (initially `root.left` and `root.right`) to see if they are mirror images.

    Algorithm:
    1. Define a helper function `_is_mirror(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool`:
        a. Base Case 1: If both `t1` and `t2` are `None`, return `True` (they perfectly mirror each other).
        b. Base Case 2: If only one of `t1` or `t2` is `None` (but not both), return `False` (asymmetry).
        c. Recursive Step: If both `t1` and `t2` are non-`None`:
           Return `(t1.val == t2.val)` AND `_is_mirror(t1.left, t2.right)` AND `_is_mirror(t1.right, t2.left)`.
           This checks the values and then recursively checks the "outer" children (t1.left with t2.right) and the "inner" children (t1.right with t2.left) for mirror symmetry.

    2. The main `isSymmetric_Recursive(root)` function will:
        a. Handle the edge case: If `root` is `None`, return `True` (an empty tree is symmetric).
        b. Otherwise, call `_is_mirror(root.left, root.right)`.

    T.C.: O(N) - Each node is visited (compared) exactly once.
    S.C.: O(H) - For the recursion stack, where H is the height of the tree. In the worst case (skewed tree), H = N, so O(N). In the best case (balanced tree), H = logN, so O(logN).

    ---

    Approach 2: Iterative Breadth-First Search (BFS) - Optimal

    We can simulate a level-order traversal (BFS) using a queue. Instead of adding single nodes, we will add pairs of nodes that are supposed to be symmetric counterparts.

    Algorithm:
    1. Handle edge case: If `root` is `None`, return `True`.
    2. Initialize a `collections.deque` (queue).
    3. Add the initial pair of nodes to compare: `(root.left, root.right)`.
    4. While the `queue` is not empty:
        a. Dequeue a pair `(t1, t2)` from the front of the queue.
        b. Check for `None` conditions for the current pair:
           i. If both `t1` and `t2` are `None`, continue to the next pair (they are symmetric at this level).
           ii. If only one of `t1` or `t2` is `None`, return `False` (asymmetry detected).
        c. If both `t1` and `t2` are non-`None`, check their values:
           i. If `t1.val != t2.val`, return `False` (values don't match, asymmetry).
        d. If all checks pass for the current pair, enqueue their children for mirror comparison:
           i. Add `(t1.left, t2.right)` to the queue (outer children).
           ii. Add `(t1.right, t2.left)` to the queue (inner children).
    5. If the loop completes without returning `False`, it means all corresponding pairs were symmetric. Return `True`.

    T.C.: O(N) - Each node (or `None` reference in a pair) is enqueued and dequeued a constant number of times.
    S.C.: O(W) - Where W is the maximum width of the tree. In the worst case (a complete binary tree), W can be up to N/2, so O(N). In the best case (skewed tree), W is 1, so O(1).
    """

    def isSymmetric_Recursive(self, root: Optional[TreeNode]) -> bool:
        """
        Recursive solution using Depth-First Search.
        T.C.: O(N), S.C.: O(H).
        """
        if not root:
            return True  # An empty tree is symmetric

        def _is_mirror(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
            """
            Helper function to check if two subtrees are mirror images of each other.
            """
            # If both nodes are None, they are symmetric
            if not t1 and not t2:
                return True
            # If only one of the nodes is None, they are not symmetric
            if not t1 or not t2:
                return False
            
            # Check values and recursively check mirror conditions for children
            return (t1.val == t2.val) and \
                   _is_mirror(t1.left, t2.right) and \
                   _is_mirror(t1.right, t2.left)
        
        return _is_mirror(root.left, root.right)

    def isSymmetric_Iterative(self, root: Optional[TreeNode]) -> bool:
        """
        Iterative solution using Breadth-First Search.
        T.C.: O(N), S.C.: O(W).
        """
        if not root:
            return True # An empty tree is symmetric

        # Use a deque to simulate a queue for BFS
        queue = collections.deque()
        # Start with the left and right children of the root
        queue.append((root.left, root.right))

        while queue:
            t1, t2 = queue.popleft()

            # Case 1: Both nodes are None, they are symmetric at this point, continue
            if not t1 and not t2:
                continue
            
            # Case 2: One node is None and the other is not, they are not symmetric
            if not t1 or not t2:
                return False
            
            # Case 3: Both nodes are non-None, check their values
            if t1.val != t2.val:
                return False
            
            # If values match, add their children for further mirror comparison
            # Add outer children pair (t1's left vs t2's right)
            queue.append((t1.left, t2.right))
            # Add inner children pair (t1's right vs t2's left)
            queue.append((t1.right, t2.left))
        
        return True # If the loop completes, the tree is symmetric

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """
        Main entry point for the LeetCode problem.
        Calls the recursive solution as a standard optimal approach.
        """
        # return self.isSymmetric_Iterative(root)
        return self.isSymmetric_Recursive(root)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases: (input_tree_list, expected_is_symmetric)
    test_cases = [
        ([1, 2, 2, 3, 4, 4, 3], True),        # Example 1
        ([1, 2, 2, None, 3, None, 3], False), # Example 2
        ([], True),                           # Empty tree
        ([1], True),                          # Single node tree
        ([1, 2, 2, 3, None, None, 3], True),  # Symmetric example with nulls
        ([1, 2, 2, None, 3, 3, None], False), # Not symmetric
        ([1, 2, None], False),                # Skewed tree
        ([1,2,3,3,None,2,None], False),      # Values symmetric, structure not
        ([5,4,1,None,1,None,4,2,None,2,None], False) # Complex non-symmetric
    ]

    print("--- Recursive Solution ---")
    for tree_list, expected_symmetric in test_cases:
        root = build_tree(tree_list)
        result = solution.isSymmetric_Recursive(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Symmetric: {result}")
        print(f"Expected Symmetric: {expected_symmetric}")
        print(f"Status: {'Pass' if result == expected_symmetric else 'Fail'}")
        print("-" * 30)

    print("\n--- Iterative Solution (BFS) ---")
    for tree_list, expected_symmetric in test_cases:
        root = build_tree(tree_list)
        result = solution.isSymmetric_Iterative(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Symmetric: {result}")
        print(f"Expected Symmetric: {expected_symmetric}")
        print(f"Status: {'Pass' if result == expected_symmetric else 'Fail'}")
        print("-" * 30)

    print("\n--- Main Entry Point (Recursive Optimal) ---")
    for tree_list, expected_symmetric in test_cases:
        root = build_tree(tree_list)
        result = solution.isSymmetric(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Symmetric: {result}")
        print(f"Expected Symmetric: {expected_symmetric}")
        print(f"Status: {'Pass' if result == expected_symmetric else 'Fail'}")
        print("-" * 30)
