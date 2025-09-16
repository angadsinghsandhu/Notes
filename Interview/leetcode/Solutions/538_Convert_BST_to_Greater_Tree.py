# File: Leetcode/Solutions/538_Convert_BST_to_Greater_Tree.py
# This problem is identical to LeetCode 1038.

"""
Problem Number: 538
Problem Name: Convert BST to Greater Tree
Difficulty: Medium
Tags: Tree, Depth-First Search, Binary Search Tree, Binary Tree
Company (Frequency): Amazon (10), Google (8), Facebook (7), Microsoft (6)
Leetcode Link: https://leetcode.com/problems/convert-bst-to-greater-tree/description/
Note: This question is the same as 1038: https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/

DESCRIPTION

Given the `root` of a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed to the original key plus the sum of all keys greater than the original key in BST.

As a reminder, a binary search tree is a tree that satisfies these constraints:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

---

#### Example 1:

Input:
root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]

Output:

[30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]

Explanation:
Original node values:
  4 -> becomes 4 + (6+5+7+8) = 30
  1 -> becomes 1 + (4+6+5+7+8+2+3) = 36
  etc.

#### Example 2:

Input:
root = [0,null,1]

Output:

[1,null,1]

Explanation:
Original node values:
  0 -> becomes 0 + 1 = 1
  1 -> stays 1 (no values greater than 1)

#### Constraints:

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-10^4 <= Node.val <= 10^4`.
- All the values in the tree are unique.
- `root` is guaranteed to be a valid binary search tree.
"""

from typing import Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The problem asks us to modify a BST in-place. Each node's new value is its original value plus the sum of all larger values.
    - The key property of a BST is that an in-order traversal visits nodes in ascending order.
    - To get the sum of all larger values, we should traverse the tree in **reverse in-order** (Right -> Root -> Left). This visits nodes in descending order of their values.
    - We can use a variable to keep a running sum of all the nodes we have already visited. Since we're visiting from largest to smallest, this running sum will always represent the sum of all values greater than the current node.

    Input:
        root: Optional[TreeNode] - The root of the BST.

    Output:
        Optional[TreeNode] - The root of the modified Greater Tree.
    """

    def convertBST_Recursive(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Approach 1: Recursive Reverse In-order Traversal
        - We use a recursive helper function that traverses the tree in `Right -> Root -> Left` order.
        - We maintain a `running_sum` variable, initialized to 0. Since this sum needs to be shared across recursive calls, we can use an instance variable or pass it by reference (not a direct feature in Python, so a mutable object or instance variable is needed). An instance variable is a clean way to do this.
        - The helper function `reverse_inorder` takes a node as input:
          - Base case: if `node` is `None`, return.
          - Recursive step:
            - Recurse on the right child: `reverse_inorder(node.right)`.
            - Process the current node:
              - Add the current node's value to the `running_sum`.
              - Update the current node's value to the new `running_sum`.
            - Recurse on the left child: `reverse_inorder(node.left)`.

        T.C.: O(N) - Each node is visited exactly once.
        S.C.: O(H) - The recursion stack depth is equal to the height of the tree.
        """
        if not root:
            return None

        self.running_sum = 0

        def reverse_inorder(node: Optional[TreeNode]):
            if not node:
                return

            # Traverse the right subtree first (reverse in-order)
            reverse_inorder(node.right)

            # Update the running sum and the current node's value
            self.running_sum += node.val
            node.val = self.running_sum

            # Traverse the left subtree
            reverse_inorder(node.left)

        reverse_inorder(root)
        return root

    def convertBST_Iterative(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Approach 2: Iterative Reverse In-order Traversal
        - This approach uses an explicit stack to simulate the recursion.
        - The traversal order is `Right -> Root -> Left`.
        - The algorithm:
          1. Initialize a stack and a `running_sum` to 0.
          2. Start at the root and go to the rightmost node, pushing nodes onto the stack.
          3. Once the rightmost path is explored, pop a node from the stack.
          4. Process the popped node: update its value with the `running_sum`.
          5. Then, move to the popped node's left child and repeat the process (go to the rightmost node of the left subtree, etc.).
        - This is essentially an iterative implementation of the reverse in-order traversal.

        T.C.: O(N) - Each node is pushed and popped from the stack once.
        S.C.: O(H) - The stack can hold up to H nodes, where H is the height of the tree.
        """
        if not root:
            return None
        
        stack = []
        running_sum = 0
        current = root

        while current or stack:
            # Go to the rightmost node
            while current:
                stack.append(current)
                current = current.right
            
            # Pop the next largest node
            current = stack.pop()
            
            # Update the running sum and node value
            running_sum += current.val
            current.val = running_sum
            
            # Move to the left child to find the next largest node
            current = current.left
            
        return root

    def convertBST(self, root: Optional[TreeNode], use_recursive: Any = True) -> Optional[TreeNode]:
        """
        Main entry point for the problem.
        The recursive solution is more concise, but the iterative solution avoids recursion depth limits.
        """
        if use_recursive:
            return self.convertBST_Recursive(root)
        else:
            return self.convertBST_Iterative(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    #       4
    #      / \
    #     1   6
    #    / \ / \
    #   0  2 5  7
    #         \  \
    #          3  8
    root1 = build_tree([4,1,6,0,2,5,7,None,None,None,3,None,None,None,8])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    # Using recursive approach
    solution.convertBST(root1, use_recursive=True)
    print(f"Test Case 1 Output (Recursive): {tree_to_list(root1)}") # Expected: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
    
    # Rebuild tree for iterative test
    root1_iter = build_tree([4,1,6,0,2,5,7,None,None,None,3,None,None,None,8])
    solution.convertBST(root1_iter, use_recursive=False)
    print(f"Test Case 1 Output (Iterative): {tree_to_list(root1_iter)}")
    print("-" * 30)

    # Test case 2
    root2 = build_tree([0, None, 1])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    solution.convertBST(root2, use_recursive=True)
    print(f"Test Case 2 Output (Recursive): {tree_to_list(root2)}") # Expected: [1,null,1]
    
    root2_iter = build_tree([0, None, 1])
    solution.convertBST(root2_iter, use_recursive=False)
    print(f"Test Case 2 Output (Iterative): {tree_to_list(root2_iter)}")
    print("-" * 30)
    
    # Test case 3: Single node
    root3 = build_tree([5])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    solution.convertBST(root3, use_recursive=True)
    print(f"Test Case 3 Output (Recursive): {tree_to_list(root3)}") # Expected: [5]
    
    root3_iter = build_tree([5])
    solution.convertBST(root3_iter, use_recursive=False)
    print(f"Test Case 3 Output (Iterative): {tree_to_list(root3_iter)}")
    print("-" * 30)
