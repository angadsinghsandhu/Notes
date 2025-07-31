# File: Leetcode/Solutions/106_Construct_Binary_Tree_from_Inorder_and_Postorder_Traversal.py

"""
Problem Number: 106
Problem Name: Construct Binary Tree from Inorder and Postorder Traversal
Difficulty: Medium
Tags: Array, Hash Table, Divide and Conquer, Tree, Binary Tree
Company (Frequency): Amazon (10), Facebook (7), Google (5)
Leetcode Link: https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

DESCRIPTION

Given two integer arrays `inorder` and `postorder` where `inorder` is the inorder traversal of a binary tree and `postorder` is the postorder traversal of the same tree, construct and return the binary tree.

---

#### Example 1:

Input:
inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]

Output:

[3,9,20,null,null,15,7]

#### Example 2:

Input:
inorder = [-1], postorder = [-1]

Output:

[-1]

#### Constraints:

  - `1 <= inorder.length <= 3000`
  - `postorder.length == inorder.length`
  - `-3000 <= inorder[i], postorder[i] <= 3000`
  - `inorder` and `postorder` consist of unique values.
  - Each value of `postorder` also appears in `inorder`.
  - `inorder` is guaranteed to be the inorder traversal of the tree.
  - `postorder` is guaranteed to be the postorder traversal of the tree.
"""

from typing import List, Optional, Any
from helpers import TreeNode, tree_to_list

class Solution:
    """
    Thought Process:
    - This problem requires reconstructing a binary tree given its inorder and postorder traversals.
    - Key properties:
      - Inorder traversal: Left -> Root -> Right
      - Postorder traversal: Left -> Right -> Root
    - The *last element* in the postorder traversal is always the root of the current subtree.
    - Once we identify the root from postorder, we can find its position in the inorder traversal.
    - The elements to the *left* of the root in inorder traversal form the left subtree's inorder traversal.
    - The elements to the *right* of the root in inorder traversal form the right subtree's inorder traversal.
    - Similarly, in postorder, the elements before the root correspond to the left and right subtrees. The number of elements in the left inorder subarray will tell us where the left subtree's postorder traversal ends and the right subtree's begins.

    - This naturally suggests a recursive, divide-and-conquer approach.
    - To efficiently find the root's index in the inorder array, a hash map (dictionary) can be used to store value-to-index mappings for the inorder array.

    Input:
        inorder: List[int] - Inorder traversal of the tree.
        postorder: List[int] - Postorder traversal of the tree.

    Output:
        Optional[TreeNode] - The root of the constructed binary tree.
    """

    def buildTree_Recursive(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        """
        Approach: Recursive (Divide and Conquer)
        - Use a helper function that takes `inorder_start`, `inorder_end`, `postorder_start`, `postorder_end`
          indices to define the current sub-arrays for tree construction.
        - The `postorder_idx` will point to the current root in the `postorder` array,
          and it should be decremented after each root is used (since we're processing postorder from right to left).
        - Pre-compute a hash map for inorder values to their indices for O(1) lookups.

        T.C.: O(N) - Each node is created once. The hash map lookups are O(1).
                      The slicing of lists can make it O(N^2) if not careful.
                      By passing indices and using a hash map, it's O(N).
        S.C.: O(N) - For the recursion stack in the worst case (skewed tree) and for the hash map.
        """
        # Create a dictionary to quickly find the index of a value in inorder traversal
        inorder_map = {val: i for i, val in enumerate(inorder)}
        
        # Initialize a pointer for the postorder array, starting from the end
        self.postorder_idx = len(postorder) - 1

        def build(in_start: int, in_end: int) -> Optional[TreeNode]:
            # Base case: if the range is invalid or no elements
            if in_start > in_end:
                return None
            
            # The current root value is the last element in the current postorder sub-array
            root_val = postorder[self.postorder_idx]
            root = TreeNode(root_val)
            
            # Decrement the postorder index for the next recursive call
            self.postorder_idx -= 1
            
            # Find the root's index in the inorder traversal
            in_root_idx = inorder_map[root_val]
            
            # Recursively build the right subtree first (because postorder is Left-Right-Root)
            # The right subtree's inorder segment is from (in_root_idx + 1) to in_end
            root.right = build(in_root_idx + 1, in_end)
            
            # Recursively build the left subtree
            # The left subtree's inorder segment is from in_start to (in_root_idx - 1)
            root.left = build(in_start, in_root_idx - 1)
            
            return root

        # Start building the tree with the full inorder array range
        return build(0, len(inorder) - 1)


    def buildTree_Iterative(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        """
        Approach: Iterative (Using a Stack)
        This problem is traditionally solved recursively. An iterative approach is more complex
        and generally not preferred unless recursion depth is an issue or specific performance
        characteristics (e.g., avoiding call stack overhead) are critical.

        A common iterative approach involves using a stack to simulate the recursion.
        When processing a node:
        1. Create the root from the last element of postorder.
        2. Push the root onto a stack.
        3. If the top of the stack is not the right child of the current root (found via inorder),
           then the current root has a right child, so we process the next element from postorder
           as the right child and push it to the stack.
        4. If it is the right child, then the right subtree is complete. Pop from the stack until
           the stack top matches an element that *should* be a left child. Process the left child.

        Due to its complexity and less intuitive nature for this specific problem,
        it's less common to implement iteratively in interviews unless explicitly asked.
        The recursive solution is much more elegant. For this solution, we will stick
        to the common recursive approach.
        """
        # For this problem, the recursive solution is highly intuitive and efficient.
        # An iterative solution is significantly more complex and typically involves
        # simulating the recursion explicitly with a stack and careful state management.
        # Given the typical scope of "medium" problems and common interview expectations,
        # the recursive solution is the standard and preferred one.
        # Therefore, we will defer a detailed iterative implementation unless specifically required.
        # A placeholder is provided to match the structure.
        return self.buildTree_Recursive(inorder, postorder) # Fallback to recursive

    def buildTree(self, inorder: List[int], postorder: List[int], use_recursive: Any = True) -> Optional[TreeNode]:
        """
        Main entry point for the LeetCode problem.
        Calls the recursive solution as it's the standard and most intuitive approach.
        """
        if use_recursive:
            return self.buildTree_Recursive(inorder, postorder)
        else:
            return self.buildTree_Iterative(inorder, postorder)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    inorder1 = [9, 3, 15, 20, 7]
    postorder1 = [9, 15, 7, 20, 3]
    built_tree1 = solution.buildTree(inorder1, postorder1, use_recursive=True)
    print(f"Test Case 1 Input Inorder: {inorder1}")
    print(f"Test Case 1 Input Postorder: {postorder1}")
    print(f"Test Case 1 Output: {tree_to_list(built_tree1)}") # Expected: [3,9,20,null,null,15,7]
    print("-" * 30)

    # Test case 2
    inorder2 = [-1]
    postorder2 = [-1]
    built_tree2 = solution.buildTree(inorder2, postorder2, use_recursive=True)
    print(f"Test Case 2 Input Inorder: {inorder2}")
    print(f"Test Case 2 Input Postorder: {postorder2}")
    print(f"Test Case 2 Output: {tree_to_list(built_tree2)}") # Expected: [-1]
    print("-" * 30)

    # Test case 3 (More complex example)
    inorder3 = [4, 2, 5, 1, 6, 3, 7]
    postorder3 = [4, 5, 2, 6, 7, 3, 1]
    built_tree3 = solution.buildTree(inorder3, postorder3, use_recursive=True)
    print(f"Test Case 3 Input Inorder: {inorder3}")
    print(f"Test Case 3 Input Postorder: {postorder3}")
    print(f"Test Case 3 Output: {tree_to_list(built_tree3)}") # Expected: [1,2,3,4,None,6,7,None,None,5] or similar level-order
    # Manual check:
    # Root is 1. Inorder: [4,2,5] [1] [6,3,7] -> left: [4,2,5], right: [6,3,7]
    # Postorder: [4,5,2] [6,7,3] [1] -> left_post: [4,5,2], right_post: [6,7,3]
    # Left Child: root 2. Inorder: [4] [2] [5] -> left: [4], right: [5]
    # Postorder: [4] [5] [2] -> left_post: [4], right_post: [5]
    #   Left-Left: 4
    #   Left-Right: 5
    # Right Child: root 3. Inorder: [6] [3] [7] -> left: [6], right: [7]
    # Postorder: [6] [7] [3] -> left_post: [6], right_post: [7]
    #   Right-Left: 6
    #   Right-Right: 7
    # Expected tree (level order): [1, 2, 3, 4, None, 6, 7, None, None, 5]
    # tree_to_list should produce a canonical representation, which might be [1,2,3,4,None,6,7,None,None,5]
    print("-" * 30)

    # Test case 4 (Skewed tree - right)
    inorder4 = [1, 2, 3, 4]
    postorder4 = [4, 3, 2, 1]
    built_tree4 = solution.buildTree(inorder4, postorder4, use_recursive=True)
    print(f"Test Case 4 Input Inorder: {inorder4}")
    print(f"Test Case 4 Input Postorder: {postorder4}")
    print(f"Test Case 4 Output: {tree_to_list(built_tree4)}") # Expected: [1,null,2,null,3,null,4]
    print("-" * 30)

    # Test case 5 (Skewed tree - left)
    inorder5 = [4, 3, 2, 1]
    postorder5 = [4, 3, 2, 1] # Same as inorder for left skewed tree
    built_tree5 = solution.buildTree(inorder5, postorder5, use_recursive=True)
    print(f"Test Case 5 Input Inorder: {inorder5}")
    print(f"Test Case 5 Input Postorder: {postorder5}")
    print(f"Test Case 5 Output: {tree_to_list(built_tree5)}") # Expected: [1,2,null,3,null,4]
    print("-" * 30)