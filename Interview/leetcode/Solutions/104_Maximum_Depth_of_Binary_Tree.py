# File: Leetcode/Solutions/Tree/104_Maximum_Depth_of_Binary_Tree.py

"""
Problem Number: 104
Problem Name: Maximum Depth of Binary Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree, Neetcode 150
Company (Frequency): Amazon, Apple, Facebook, Google, Microsoft
Leetcode Link: <https://leetcode.com/problems/maximum-depth-of-binary-tree/description/>

DESCRIPTION

Given the `root` of a binary tree, return its maximum depth.

A binary tree's `maximum depth` is the number of nodes along the longest path from the root node down to the farthest leaf node.

---

#### Example 1:

Input:
root = [3,9,20,null,null,15,7]

Output:
3

Explanation:
The longest path is 3 -> 20 -> 7 (or 3 -> 20 -> 15), which has 3 nodes.

---

#### Example 2:

Input:
root = [1,null,2]

Output:
2

Explanation:
The longest path is 1 -> 2, which has 2 nodes.

---

#### Constraints:

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`
"""

from typing import Optional
from collections import deque
from helpers import TreeNode, build_tree

class Solution:
    """
    Thought Process for Maximum Depth of Binary Tree:

    The maximum depth of a binary tree is defined as the number of nodes along the longest path from the root node down to the farthest leaf node.

    Key Idea:
    The maximum depth of a tree rooted at a given node can be found by taking 1 (for the node itself) plus the maximum depth of its left or right subtree.

    Base Case:
    - An empty tree (None node) has a depth of 0.

    ---

    Approach 1: Recursive Depth-First Search (DFS) - Optimal

    This problem has a natural recursive structure. For any given node, its depth is 1 (for itself) plus the maximum depth of its left or right child's subtree. We apply this definition recursively.

    Algorithm:
    1. Define a recursive helper function `_dfs_max_depth(node: Optional[TreeNode]) -> int`:
        a. Base Case: If `node` is `None`, return 0.
        b. Recursive Step:
           i. Recursively call `left_depth = _dfs_max_depth(node.left)`.
           ii. Recursively call `right_depth = _dfs_max_depth(node.right)`.
           iii. Return `1 + max(left_depth, right_depth)`.

    2. The main `maxDepth` function simply calls `_dfs_max_depth(root)`.

    T.C.: O(N) - Each node is visited exactly once.
    S.C.: O(H) - For the recursion stack, where H is the height of the tree. In the worst case (skewed tree), H = N, so O(N). In the best case (balanced tree), H = logN, so O(logN).

    ---

    Approach 2: Iterative Breadth-First Search (BFS) - Optimal

    BFS explores the tree level by level. By counting the number of levels explored, we can determine the maximum depth. Each time we complete processing all nodes at a particular level, we increment our depth counter.

    Algorithm:
    1. Handle edge case: If `root` is `None`, return 0.
    2. Initialize a `collections.deque` (queue) and add the `root` node to it.
    3. Initialize `depth = 0`.
    4. While the `queue` is not empty:
        a. Increment `depth` (we are starting a new level).
        b. Get the `level_size`, which is the current number of nodes in the queue.
        c. Loop `level_size` times:
           i. Dequeue a `node` from the front of the queue.
           ii. If `node` has a left child, enqueue it.
           iii. If `node` has a right child, enqueue it.
    5. Return `depth`.

    T.C.: O(N) - Each node is enqueued and dequeued exactly once.
    S.C.: O(W) - Where W is the maximum width of the tree (maximum number of nodes at any single level). In the worst case (a complete binary tree), W can be up to N/2, so O(N). In the best case (skewed tree), W is 1, so O(1).
    """

    def maxDepth_Recursive(self, root: Optional[TreeNode]) -> int:
        """
        Recursive solution using Depth-First Search.
        T.C.: O(N), S.C.: O(H) (where H is tree height).
        """
        if not root:
            return 0  # Base case: empty tree has depth 0

        # Recursively find the maximum depth of left and right subtrees
        left_depth = self.maxDepth_Recursive(root.left)
        right_depth = self.maxDepth_Recursive(root.right)

        # The depth of the current node's tree is 1 (for itself)
        # plus the maximum of its children's depths.
        return 1 + max(left_depth, right_depth)

    def maxDepth_Iterative(self, root: Optional[TreeNode]) -> int:
        """
        Iterative solution using Breadth-First Search (Level Order Traversal).
        T.C.: O(N), S.C.: O(W) (where W is max width of tree).
        """
        if not root:
            return 0  # Base case: empty tree has depth 0

        # Use a deque for efficient popping from the left
        queue = deque([root])
        depth = 0

        while queue:
            # Increment depth for each new level we process
            depth += 1
            # Get the number of nodes at the current level
            level_size = len(queue)

            # Process all nodes at the current level
            for _ in range(level_size):
                node = queue.popleft() # Dequeue node

                # Enqueue children for the next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return depth

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Main entry point for the LeetCode problem.
        Chooses the recursive DFS approach as it's typically more concise for this problem.
        """
        return self.maxDepth_Recursive(root)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases: (input_tree_list, expected_depth)
    test_cases = [
        ([3, 9, 20, None, None, 15, 7], 3),  # Example 1
        ([1, None, 2], 2),                   # Example 2
        ([], 0),                             # Empty tree
        ([1], 1),                            # Single node tree
        ([1, 2, 3], 2),                      # Full tree height 2
        ([1, 2, None, 3, None, 4], 4),       # Skewed left then right
        ([1, None, 2, None, 3, None, 4], 4), # Skewed right
        ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 4) # Full balanced tree of height 4
    ]

    print("--- Recursive Solution ---")
    for tree_list, expected_depth in test_cases:
        root = build_tree(tree_list)
        result = solution.maxDepth_Recursive(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Depth: {result}")
        print(f"Expected Depth: {expected_depth}")
        print(f"Status: {'Pass' if result == expected_depth else 'Fail'}")
        print("-" * 30)

    print("\n--- Iterative Solution (BFS) ---")
    for tree_list, expected_depth in test_cases:
        root = build_tree(tree_list)
        result = solution.maxDepth_Iterative(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Depth: {result}")
        print(f"Expected Depth: {expected_depth}")
        print(f"Status: {'Pass' if result == expected_depth else 'Fail'}")
        print("-" * 30)

    print("\n--- Main Entry Point (Recursive Optimal) ---")
    for tree_list, expected_depth in test_cases:
        root = build_tree(tree_list)
        result = solution.maxDepth(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Depth: {result}")
        print(f"Expected Depth: {expected_depth}")
        print(f"Status: {'Pass' if result == expected_depth else 'Fail'}")
        print("-" * 30)