# TODO: new

# File: Leetcode/Solutions/Amazon/105_Construct_Binary_Tree_from_Preorder_and_Inorder_Traversal.py

"""
Problem Number: 105
Problem Name: Construct Binary Tree from Preorder and Inorder Traversal
Difficulty: Medium
Tags: Tree, Array, Hash Table, Divide and Conquer, Binary Tree
Company (Frequency): Amazon (40)
Leetcode Link: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

DESCRIPTION

Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

---

#### Example 1:
**Input:**
```plaintext
preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
```

**Output:**
```plaintext
[3,9,20,null,null,15,7]
```

**Explanation:**  
The binary tree is constructed as follows:
- The first element in `preorder` (3) is the root.
- In `inorder`, the elements before 3 (9) form the left subtree, and the elements after 3 (15, 20, 7) form the right subtree.
- Recursively apply the same logic to construct the left and right subtrees.

#### Constraints:
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values.
- Each value of inorder also appears in preorder.
- preorder is guaranteed to be the preorder traversal of the tree.
- inorder is guaranteed to be the inorder traversal of the tree.
"""

from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem involves constructing a binary tree from its preorder and inorder traversals.
    - The first element in the preorder traversal is always the root of the tree.
    - The root divides the inorder traversal into left and right subtrees.
    - We can recursively construct the left and right subtrees using the same logic.

    Input:
        preorder: List[int] - The preorder traversal of the tree.
        inorder: List[int] - The inorder traversal of the tree.

    Output:
        TreeNode - The root of the constructed binary tree.
    """

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """
        Approach:
        - Use a hash map to store the indices of elements in the inorder traversal for quick lookup.
        - Recursively construct the tree by dividing the preorder and inorder arrays based on the root.
        - The root is the first element in the preorder array.
        - The left subtree is constructed from the elements before the root in the inorder array.
        - The right subtree is constructed from the elements after the root in the inorder array.

        T.C.: O(n) - We visit each node once.
        S.C.: O(n) - The hash map stores all the indices of the inorder array.
        """
        # Create a hash map to store the indices of elements in the inorder array
        inorder_map = {val: idx for idx, val in enumerate(inorder)}

        def build(pre_start: int, pre_end: int, in_start: int, in_end: int) -> Optional[TreeNode]:
            # Base case: if there are no elements to construct the tree
            if pre_start > pre_end:
                return None

            # The first element in the preorder array is the root
            root_val = preorder[pre_start]
            root = TreeNode(root_val)

            # Find the index of the root in the inorder array
            in_root_idx = inorder_map[root_val]

            # Calculate the number of elements in the left subtree
            left_subtree_size = in_root_idx - in_start

            # Recursively construct the left subtree
            root.left = build(pre_start + 1, pre_start + left_subtree_size, in_start, in_root_idx - 1)

            # Recursively construct the right subtree
            root.right = build(pre_start + left_subtree_size + 1, pre_end, in_root_idx + 1, in_end)

            return root

        # Start the recursive construction of the tree
        return build(0, len(preorder) - 1, 0, len(inorder) - 1)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    preorder1 = [3, 9, 20, 15, 7]
    inorder1 = [9, 3, 15, 20, 7]
    root1 = solution.buildTree(preorder1, inorder1)

    # Helper function to print the tree in level order
    def print_tree(root: Optional[TreeNode]) -> List[Optional[int]]:
        if not root:
            return []
        result = []
        queue = [root]
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
        return result

    print(print_tree(root1))  # Output: [3, 9, 20, None, None, 15, 7]

    # Test case 2
    preorder2 = [-1]
    inorder2 = [-1]
    root2 = solution.buildTree(preorder2, inorder2)
    print(print_tree(root2))  # Output: [-1]