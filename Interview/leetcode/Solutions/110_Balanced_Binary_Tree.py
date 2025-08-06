# File: Leetcode/Solutions/110_Balanced_Binary_Tree.py
# This is a common problem from LeetCode (110) and GeeksforGeeks.

"""
Problem Number: 110
Problem Name: Balanced Binary Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Binary Tree
Company (Frequency): Amazon (15), Facebook (10), Google (8)
Leetcode Link: https://leetcode.com/problems/balanced-binary-tree/description/
GeeksforGeeks Link: https://www.geeksforgeeks.org/check-if-a-binary-tree-is-height-balanced-or-not/

DESCRIPTION

Given a binary tree, determine if it is height-balanced. A binary tree is considered height-balanced if the absolute difference in heights of the left and right subtrees is at most 1 for every single node in the tree.

---

#### Example 1:
Input:
(A balanced binary tree)

Output:

True

Explanation:
The height difference between the left and right subtrees at all nodes is at most 1. Hence, the tree is balanced.

#### Example 2:
Input:
(An unbalanced binary tree)

Output:

False

Explanation:
The height difference between the left and right subtrees at node 2 is 2, which exceeds 1. Hence, the tree is not balanced.

#### Constraints:
- The number of nodes in the tree is in the range [0, 5000].
- -1000 <= Node.val <= 1000
"""

from typing import Optional
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The problem requires checking the height-balance property for *every* node in the tree.
    - A tree is height-balanced if, for every node, `|height(left_subtree) - height(right_subtree)| <= 1`.
    - This suggests a traversal-based approach, likely a form of DFS.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        bool - True if the tree is height-balanced, False otherwise.
    """

    def isBalanced_Naive(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 1: Top-Down Recursion (O(n^2))
        - This approach involves two separate recursive functions: one to check for balance and another to compute height.
        - `isBalanced(node)`:
          - Base case: If `node` is `None`, it's balanced (height 0).
          - Recursive step:
            - Calculate `l_height = height(node.left)`.
            - Calculate `r_height = height(node.right)`.
            - Check if `|l_height - r_height| <= 1`.
            - Recursively call `isBalanced(node.left)` and `isBalanced(node.right)`.
            - Return `True` only if all three conditions are met.
        - `height(node)`:
          - Base case: If `node` is `None`, return 0.
          - Recursive step: return `1 + max(height(node.left), height(node.right))`.
        - The time complexity is O(N^2) in the worst case (e.g., a skewed tree) because for each node, we re-compute the heights of its subtrees.

        T.C.: O(N^2)
        S.C.: O(H) - For the recursion stack.
        """
        if not root:
            return True
        
        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))
            
        l_height = height(root.left)
        r_height = height(root.right)
        
        if abs(l_height - r_height) > 1:
            return False
            
        return self.isBalanced_Naive(root.left) and self.isBalanced_Naive(root.right)
    
    def isBalanced_Optimized(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 2: Bottom-Up Recursion (O(n))
        - The inefficiency of the naive approach is the repeated height calculation. The optimized solution combines both checks into a single post-order traversal.
        - We define a recursive helper function `check_height_balance` that returns the height of the subtree if it's balanced, or a special value (like -1) if it's not balanced.
        - `check_height_balance(node)`:
          - Base case: If `node` is `None`, return 0 (height of an empty subtree).
          - Recursive step:
            - Recursively call on the left child: `left_height = check_height_balance(node.left)`.
            - If `left_height` is -1, the left subtree is unbalanced, so the entire tree is unbalanced. Return -1.
            - Recursively call on the right child: `right_height = check_height_balance(node.right)`.
            - If `right_height` is -1, the right subtree is unbalanced, so the entire tree is unbalanced. Return -1.
            - Check the height difference for the current node: `|left_height - right_height|`.
            - If the difference is greater than 1, the current subtree is unbalanced. Return -1.
            - Otherwise, the current subtree is balanced. Return its height: `1 + max(left_height, right_height)`.
        - The main function simply calls the helper and checks if the result is -1.

        T.C.: O(N) - Each node is visited only once.
        S.C.: O(H) - For the recursion stack.
        """
        def check_height_balance(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            
            left_height = check_height_balance(node.left)
            if left_height == -1:
                return -1
                
            right_height = check_height_balance(node.right)
            if right_height == -1:
                return -1
            
            if abs(left_height - right_height) > 1:
                return -1
            
            return 1 + max(left_height, right_height)
        
        return check_height_balance(root) != -1

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        Main entry point for the problem.
        The optimized bottom-up approach is the standard, most efficient solution.
        """
        return self.isBalanced_Optimized(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Balanced Tree
    #     3
    #    / \
    #   9   20
    #      /  \
    #     15   7
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    print(f"Test Case 1 Output (Naive): {solution.isBalanced_Naive(root1)}")  # Expected: True
    print(f"Test Case 1 Output (Optimized): {solution.isBalanced(root1)}") # Expected: True
    print("-" * 30)

    # Unbalanced Tree
    #       1
    #      /
    #     2
    #    /
    #   3
    root2 = build_tree([1, 2, None, 3, None, 4])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    print(f"Test Case 2 Output (Naive): {solution.isBalanced_Naive(root2)}")  # Expected: False
    print(f"Test Case 2 Output (Optimized): {solution.isBalanced(root2)}") # Expected: False
    print("-" * 30)
    
    # Another unbalanced tree
    #     1
    #    / \
    #   2   2
    #  / \
    # 3   3
    #    /
    #   4
    root3 = build_tree([1, 2, 2, 3, 3, None, None, 4])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    print(f"Test Case 3 Output (Naive): {solution.isBalanced_Naive(root3)}")  # Expected: False
    print(f"Test Case 3 Output (Optimized): {solution.isBalanced(root3)}") # Expected: False
    print("-" * 30)

    # Empty tree
    root4 = build_tree([])
    print(f"Test Case 4 Input: {tree_to_list(root4)}")
    print(f"Test Case 4 Output (Naive): {solution.isBalanced_Naive(root4)}")  # Expected: True
    print(f"Test Case 4 Output (Optimized): {solution.isBalanced(root4)}") # Expected: True
    print("-" * 30)
