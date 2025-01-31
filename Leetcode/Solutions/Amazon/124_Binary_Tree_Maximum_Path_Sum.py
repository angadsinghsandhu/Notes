# TODO: new

# File: Leetcode/Solutions/124_Binary_Tree_Maximum_Path_Sum.py

"""
Problem Number: 124
Problem Name: Binary Tree Maximum Path Sum
Difficulty: Hard
Tags: Tree, Depth-First Search, Dynamic Programming, Binary Tree
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/binary-tree-maximum-path-sum/description/

DESCRIPTION

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.

---

#### Example 1:
**Input:**
```plaintext
root = [1,2,3]
```

**Output:**
```plaintext
6
```

**Explanation:**  
The optimal path is `2 -> 1 -> 3` with a path sum of `2 + 1 + 3 = 6`.

#### Example 2:
**Input:**
```plaintext
root = [-10,9,20,null,null,15,7]
```

**Output:**
```plaintext
42
```

**Explanation:**  
The optimal path is `15 -> 20 -> 7` with a path sum of `15 + 20 + 7 = 42`.

#### Constraints:
- The number of nodes in the tree is in the range `[1, 3 * 10^4]`.
- `-1000 <= Node.val <= 1000`
"""

from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem requires finding the maximum path sum in a binary tree, where a path can start and end at any node.
    - A path cannot split, meaning it cannot include both the left and right subtrees of a node simultaneously.
    - We can use a recursive approach to calculate the maximum path sum for each subtree and update the global maximum.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        int - The maximum path sum of any non-empty path in the tree.
    """

    def maxPathSum(self, root: TreeNode) -> int:
        """
        Approach:
        - Use a helper function `dfs` to recursively compute the maximum path sum for each subtree.
        - At each node, calculate the maximum path sum that includes the current node and either its left or right subtree.
        - Update the global maximum path sum if the current path sum (including both subtrees) is greater.
        - Return the maximum path sum that can be extended upward from the current node.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        # Initialize the global maximum path sum to negative infinity
        self.max_sum = float('-inf')

        def dfs(node: TreeNode) -> int:
            """
            Helper function to perform depth-first search and compute the maximum path sum.
            """
            if not node:
                return 0

            # Recursively compute the maximum path sum for the left and right subtrees
            # If the sum is negative, treat it as 0 (ignore the subtree)
            left_max = max(0, dfs(node.left))
            right_max = max(0, dfs(node.right))

            # Update the global maximum path sum
            # This includes the current node's value and the maximum sums from both subtrees
            self.max_sum = max(self.max_sum, node.val + left_max + right_max)

            # Return the maximum path sum that can be extended upward
            # This includes the current node's value and the maximum of the left or right subtree
            return node.val + max(left_max, right_max)

        # Start the DFS traversal from the root
        dfs(root)

        # Return the global maximum path sum
        return self.max_sum

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to create a binary tree from a list of values
    def create_tree(values: List[int], index: int = 0) -> TreeNode:
        if index >= len(values) or values[index] is None:
            return None
        root = TreeNode(values[index])
        root.left = create_tree(values, 2 * index + 1)
        root.right = create_tree(values, 2 * index + 2)
        return root

    # Test case 1
    tree1 = create_tree([1, 2, 3])
    print(solution.maxPathSum(tree1))  # Output: 6

    # Test case 2
    tree2 = create_tree([-10, 9, 20, None, None, 15, 7])
    print(solution.maxPathSum(tree2))  # Output: 42

    # Test case 3 (Single node)
    tree3 = create_tree([1])
    print(solution.maxPathSum(tree3))  # Output: 1

    # Test case 4 (All negative values)
    tree4 = create_tree([-3, -2, -1])
    print(solution.maxPathSum(tree4))  # Output: -1