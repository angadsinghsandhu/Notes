# TODO: new

# File: Leetcode/Solutions/1373_Maximum_Sum_BST_in_Binary_Tree.py

"""
Problem Number: 1373
Problem Name: Maximum Sum BST in Binary Tree
Difficulty: Hard
Tags: Tree, Depth-First Search, Binary Search Tree, Dynamic Programming, Binary Tree
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/description/

DESCRIPTION

Given a binary tree, return the maximum sum of all keys of any subtree that is also a Binary Search Tree (BST).

A BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

---

#### Example 1:
**Input:**
```plaintext
root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]
```

**Output:**
```plaintext
20
```

**Explanation:**  
The maximum sum is obtained from the subtree rooted at node 3, which is a valid BST with a sum of 20.

#### Example 2:
**Input:**
```plaintext
root = [4,3,null,1,2]
```

**Output:**
```plaintext
2
```

**Explanation:**  
The maximum sum is obtained from the subtree rooted at node 2, which is a valid BST with a sum of 2.

#### Example 3:
**Input:**
```plaintext
root = [-4,-2,-5]
```

**Output:**
```plaintext
0
```

**Explanation:**  
All values are negative, so no valid BST exists with a positive sum. The result is 0.

#### Constraints:
- The number of nodes in the tree is in the range `[1, 4 * 10^4]`.
- `-4 * 10^4 <= Node.val <= 4 * 10^4`
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
    - The problem requires finding the maximum sum of any subtree that is also a valid BST.
    - We can use a recursive approach to traverse the tree and validate whether each subtree is a BST.
    - For each node, we need to track the minimum value, maximum value, and sum of the subtree.
    - If a subtree is a valid BST, we update the global maximum sum.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        int - The maximum sum of any valid BST subtree.
    """

    def maxSumBST(self, root: Optional[TreeNode]) -> int:
        """
        Approach:
        - Use a helper function `dfs` to perform a post-order traversal of the tree.
        - For each node, check if its left and right subtrees are valid BSTs.
        - If the current subtree is a valid BST, calculate its sum and update the global maximum sum.
        - Return the maximum sum found.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        self.max_sum = 0  # Global variable to track the maximum sum

        def dfs(node: Optional[TreeNode]) -> tuple:
            """
            Helper function to perform DFS and return:
            - Whether the subtree is a valid BST.
            - The minimum value in the subtree.
            - The maximum value in the subtree.
            - The sum of the subtree.
            """
            if not node:
                return True, float('inf'), float('-inf'), 0

            # Recursively check the left and right subtrees
            left_is_bst, left_min, left_max, left_sum = dfs(node.left)
            right_is_bst, right_min, right_max, right_sum = dfs(node.right)

            # Check if the current subtree is a valid BST
            if (left_is_bst and right_is_bst and
                left_max < node.val < right_min):
                # Calculate the sum of the current subtree
                subtree_sum = left_sum + right_sum + node.val
                # Update the global maximum sum
                self.max_sum = max(self.max_sum, subtree_sum)
                # Return the properties of the current subtree
                return (True,
                        min(left_min, node.val),
                        max(right_max, node.val),
                        subtree_sum)
            else:
                # If the current subtree is not a valid BST, return invalid properties
                return False, 0, 0, 0

        # Start the DFS traversal from the root
        dfs(root)

        # Return the maximum sum found
        return self.max_sum

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

    # Test case 1
    tree1 = create_tree([1, 4, 3, 2, 4, 2, 5, None, None, None, None, None, None, 4, 6])
    print(solution.maxSumBST(tree1))  # Output: 20

    # Test case 2
    tree2 = create_tree([4, 3, None, 1, 2])
    print(solution.maxSumBST(tree2))  # Output: 2

    # Test case 3 (All negative values)
    tree3 = create_tree([-4, -2, -5])
    print(solution.maxSumBST(tree3))  # Output: 0

    # Test case 4 (Single node)
    tree4 = create_tree([1])
    print(solution.maxSumBST(tree4))  # Output: 1