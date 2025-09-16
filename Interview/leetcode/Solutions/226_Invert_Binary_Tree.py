# File: Leetcode/Solutions/Tree/226_Invert_Binary_Tree.py
# pyright: ignore[reportInvalidStringEscapeSequence]

r"""
Problem Number: 226
Trial: 0
Problem Name: Invert Binary Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree, Neetcode 150
Company (Frequency): Amazon, Apple, Facebook, Google, Microsoft
Leetcode Link: <https://leetcode.com/problems/invert-binary-tree/description/>

DESCRIPTION

Given the `root` of a binary tree, invert the tree, and return its root.

---

#### Example 1:

Input:
root = [4,2,7,1,3,6,9]

Output:
[4,7,2,9,6,3,1]

Explanation:
Original Tree:
      4
     / \
    2   7
   / \ / \
  1  3 6  9

Inverted Tree:
      4
     / \
    7   2
   / \ / \
  9  6 3  1

---

#### Example 2:

Input:
root = [2,1,3]

Output:
[2,3,1]

---

#### Example 3:

Input:
root = []

Output:
[]

---

#### Constraints:

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`
"""

from typing import Optional
import collections
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process for Invert Binary Tree:

    Inverting a binary tree means for every node, its left child becomes its right child, and its right child becomes its left child. This operation needs to be applied recursively to all nodes in the tree.

    Key Idea:
    The inversion is a local operation (swapping children of a single node) that has a global effect when applied recursively. For any given node, we perform the swap and then ensure its new children (which were its original children) are also inverted.

    Base Case:
    - If a node is `None` (representing an empty subtree), there's nothing to invert, so we simply return `None`.

    ---

    Approach 1: Recursive Depth-First Search (DFS) - Optimal

    This problem is inherently recursive. We can apply the inversion logic either in a pre-order fashion (swap children first, then recurse) or post-order fashion (recurse on children first, then swap). Both yield the same correct result. The pre-order approach is often slightly more intuitive for this specific problem.

    Algorithm (Pre-order traversal logic):
    1. Define a recursive function `_invert_recursive(node: Optional[TreeNode]) -> Optional[TreeNode]`:
        a. Base Case: If `node` is `None`, return `None`.
        b. Recursive Step:
           i. Store the original left child: `temp_left = node.left`.
           ii. Assign the inverted right subtree to the left: `node.left = _invert_recursive(node.right)`.
           iii. Assign the inverted original left subtree (now stored in `temp_left`) to the right: `node.right = _invert_recursive(temp_left)`.
           iv. Return the `node` (which is now inverted).

    2. The main `invertTree` function simply calls `_invert_recursive(root)`.

    T.C.: O(N) - Each node is visited exactly once.
    S.C.: O(H) - For the recursion stack, where H is the height of the tree. In the worst case (skewed tree), H = N, so O(N). In the best case (balanced tree), H = logN, so O(logN).

    ---

    Approach 2: Iterative Breadth-First Search (BFS) - Optimal

    We can achieve the inversion iteratively using a Breadth-First Search (BFS) or level-order traversal. For each node processed at a given level, we swap its left and right children and then add the (now swapped) children to the queue for processing in subsequent levels.

    Algorithm:
    1. Handle edge case: If `root` is `None`, return `None`.
    2. Initialize a `collections.deque` (queue) and add the `root` node to it.
    3. While the `queue` is not empty:
        a. Dequeue a `node` from the front of the queue.
        b. Swap `node.left` and `node.right`: `node.left, node.right = node.right, node.left`.
        c. If `node` has a new left child (which was the original right child), enqueue it.
        d. If `node` has a new right child (which was the original left child), enqueue it.
    4. Return the original `root` (its children and subtrees are now inverted).

    T.C.: O(N) - Each node is enqueued and dequeued exactly once, and a constant amount of work is done per node.
    S.C.: O(W) - Where W is the maximum width of the tree (maximum number of nodes at any single level). In the worst case (a complete binary tree), W can be up to N/2, so O(N). In the best case (skewed tree), W is 1, so O(1).
    """

    def invertTree_Recursive(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Recursive solution using Depth-First Search (pre-order logic).
        T.C.: O(N), S.C.: O(H).
        """
        if not root:
            return None

        # Swap the left and right children
        root.left, root.right = root.right, root.left

        # Recursively invert the new left subtree (which was the original right)
        self.invertTree_Recursive(root.left)
        # Recursively invert the new right subtree (which was the original left)
        self.invertTree_Recursive(root.right)

        return root

    def invertTree_Iterative(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Iterative solution using Breadth-First Search (Level Order Traversal).
        T.C.: O(N), S.C.: O(W).
        """
        if not root:
            return None

        queue = collections.deque([root])

        while queue:
            node = queue.popleft() # Get the current node

            # Swap its left and right children
            node.left, node.right = node.right, node.left

            # If the (new) left child exists, add it to the queue for processing
            if node.left:
                queue.append(node.left)
            # If the (new) right child exists, add it to the queue for processing
            if node.right:
                queue.append(node.right)
        
        return root

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Main entry point for the LeetCode problem.
        Chooses the recursive DFS approach as it's often more concise for tree manipulations.
        """
        return self.invertTree_Recursive(root)
        # return self.invertTree_Iterative(root)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases: (input_tree_list, expected_inverted_list)
    test_cases = [
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]), # Example 1
        ([2, 1, 3], [2, 3, 1]),                         # Example 2
        ([], []),                                       # Example 3 (empty tree)
        ([1], [1]),                                     # Single node tree
        ([1, 2, None, 3, 4], [1, None, 2, 4, 3]),       # Tree with missing children
        ([1, None, 2, 3], [1, 2, None, None, 3]),       # Skewed right
        ([1,2,None,3,None,4], [1,None,2,None,3,None,4]), # Skewed left
        ([1,2,3,4,5,6,7], [1,3,2,7,6,5,4])              # Full tree
    ]

    print("--- Recursive Solution ---")
    for input_list, expected_list in test_cases:
        original_root = build_tree(input_list)
        inverted_root = solution.invertTree_Recursive(original_root)
        result_list = tree_to_list(inverted_root)
        print(f"Input Tree: {input_list}")
        print(f"Output Inverted Tree: {result_list}")
        print(f"Expected Inverted Tree: {expected_list}")
        print(f"Status: {'Pass' if result_list == expected_list else 'Fail'}")
        print("-" * 30)

    # Rebuild trees for iterative test since original trees are modified in place
    print("\n--- Iterative Solution (BFS) ---")
    for input_list, expected_list in test_cases:
        original_root = build_tree(input_list)
        inverted_root = solution.invertTree_Iterative(original_root)
        result_list = tree_to_list(inverted_root)
        print(f"Input Tree: {input_list}")
        print(f"Output Inverted Tree: {result_list}")
        print(f"Expected Inverted Tree: {expected_list}")
        print(f"Status: {'Pass' if result_list == expected_list else 'Fail'}")
        print("-" * 30)

    # Rebuild trees for main entry point test
    print("\n--- Main Entry Point (Recursive Optimal) ---")
    for input_list, expected_list in test_cases:
        original_root = build_tree(input_list)
        inverted_root = solution.invertTree(original_root)
        result_list = tree_to_list(inverted_root)
        print(f"Input Tree: {input_list}")
        print(f"Output Inverted Tree: {result_list}")
        print(f"Expected Inverted Tree: {expected_list}")
        print(f"Status: {'Pass' if result_list == expected_list else 'Fail'}")
        print("-" * 30)
