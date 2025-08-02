# File: Leetcode/Solutions/1373_Maximum_Sum_BST_in_Binary_Tree.py

"""
Problem Number: 1373
Problem Name: Maximum Sum BST in Binary Tree
Difficulty: Hard
Tags: Dynamic Programming, Tree, Depth-First Search, Binary Search Tree, Binary Tree
Company (Frequency): Google (5), Amazon (3), Facebook (2)
Leetcode Link: https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/description/

DESCRIPTION

Given a binary tree `root`, return the maximum sum of all keys of any sub-tree which is also a Binary Search Tree (BST).

Assume a BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

---

#### Example 1:

Input:
root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]

Output:

20

Explanation:
Maximum sum in a valid Binary search tree is obtained in root node with key equal to 3.

#### Example 2:

Input:
root = [4,3,null,1,2]

Output:

2

Explanation:
Maximum sum in a valid Binary search tree is obtained in a single root node with key equal to 2.

#### Example 3:

Input:
root = [-4,-2,-5]

Output:

0

Explanation:
All values are negatives. Return an empty BST.

#### Constraints:

  - The number of nodes in the tree is in the range `[1, 4 * 10^4]`.
  - `-4 * 10^4 <= Node.val <= 4 * 10^4`.
"""

from typing import Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - This problem requires checking for BST properties and calculating sums for all subtrees.
    - A naive approach would be to iterate through every node, and for each node, check if the subtree rooted at it is a BST. If it is, calculate its sum. This would be inefficient, likely O(N^2).
    - A more efficient approach is to use a single post-order traversal. This allows us to gather information from children before processing the parent.
    - For each node, we need to gather information from its left and right children to determine if the current subtree is a BST and, if so, what its sum is.
    - The information we need from a child subtree is:
      1. Is it a valid BST?
      2. If it is, what is its minimum value?
      3. If it is, what is its maximum value?
      4. If it is, what is the sum of its nodes?
    - We can define a recursive helper function that returns a tuple of these four values: `(is_bst, min_val, max_val, sum)`.
    - The `min_val` and `max_val` are crucial for validating the BST property at the parent node.
    - We'll maintain a global `max_sum` variable to keep track of the maximum sum found so far.
    - The iterative approach for post-order traversal uses a stack to simulate recursion.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        int - The maximum sum of all keys of any BST subtree.
    """

    def maxSumBST_Recursive(self, root: Optional[TreeNode]) -> int:
        """
        Approach: Post-order DFS (Recursive)
        - Use a recursive helper function that processes nodes from bottom up (post-order).
        - The helper function returns `(is_bst, min_val, max_val, sum)`.
        - Base case: For a null node, it's a valid BST with sum 0. The min/max values should be set to `inf` and `-inf` respectively to not interfere with parent checks.
        - Recursive step for a node:
          - Call the helper on its left and right children.
          - Use the returned values to determine if the current node forms a valid BST.
            - `is_current_bst` is true if:
              - Left and right subtrees are BSTs.
              - `left_max < node.val < right_min`.
          - If it's a BST, calculate its sum (`left_sum + right_sum + node.val`) and update the global `max_sum`.
          - If it's not a BST, we can return `(False, ...)` to signal failure up the call stack.

        T.C.: O(N) - We visit each node exactly once.
        S.C.: O(H) - For the recursion stack, where H is the height of the tree.
        """
        self.max_sum = 0
        
        def postorder_traversal(node: Optional[TreeNode]) -> tuple[bool, int, int, int]:
            if not node:
                return (True, float('inf'), float('-inf'), 0)
            
            is_left_bst, left_min, left_max, left_sum = postorder_traversal(node.left)
            is_right_bst, right_min, right_max, right_sum = postorder_traversal(node.right)
            
            is_current_bst = (is_left_bst and is_right_bst and 
                              left_max < node.val < right_min)
            
            if is_current_bst:
                current_sum = left_sum + right_sum + node.val
                self.max_sum = max(self.max_sum, current_sum)
                
                return (True, min(left_min, node.val), max(right_max, node.val), current_sum)
            else:
                return (False, 0, 0, 0)
        
        postorder_traversal(root)
        return self.max_sum

    def maxSumBST_Iterative(self, root: Optional[TreeNode]) -> int:
        """
        Approach: Iterative Post-order Traversal
        - This approach simulates the recursive post-order DFS using a stack.
        - Instead of returning a tuple, we'll store the results for each processed subtree in a hash map.
        - We need to perform a post-order traversal, which can be done with a single stack by pushing
          nodes twice or with two stacks. A simpler approach is to use a single stack and a `last_visited` node.
        - The core logic remains the same: for each node, check if its children's subtrees were valid BSTs
          and if the current node's value fits between their min/max values.

        T.C.: O(N) - Each node is pushed and popped from the stack a constant number of times.
        S.C.: O(N) - The stack and a dictionary to store subtree results can hold up to N elements.
        """
        if not root:
            return 0
        
        max_sum = 0
        # State map stores (is_bst, min_val, max_val, sum) for each node
        state_map = {None: (True, float('inf'), float('-inf'), 0)}
        stack = []
        last_visited = None
        current = root

        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                peek_node = stack[-1]
                # If right child exists and hasn't been visited yet, go right
                if peek_node.right and peek_node.right != last_visited:
                    current = peek_node.right
                else:
                    # Otherwise, process the node (post-order logic)
                    node = stack.pop()
                    
                    is_left_bst, left_min, left_max, left_sum = state_map.get(node.left, (False, 0, 0, 0))
                    is_right_bst, right_min, right_max, right_sum = state_map.get(node.right, (False, 0, 0, 0))
                    
                    is_current_bst = (is_left_bst and is_right_bst and
                                      left_max < node.val < right_min)
                    
                    if is_current_bst:
                        current_sum = left_sum + right_sum + node.val
                        max_sum = max(max_sum, current_sum)
                        
                        current_min = min(left_min, node.val)
                        current_max = max(right_max, node.val)
                        state_map[node] = (True, current_min, current_max, current_sum)
                    else:
                        state_map[node] = (False, 0, 0, 0)
                    
                    last_visited = node
        
        return max_sum


    def maxSumBST(self, root: Optional[TreeNode], use_recursive: Any = True) -> int:
        """
        Main entry point for the LeetCode problem.
        Allows choosing between recursive (DFS) and iterative solutions.
        """
        if use_recursive:
            return self.maxSumBST_Recursive(root)
        else:
            return self.maxSumBST_Iterative(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = build_tree([1,4,3,2,4,2,5,None,None,None,None,None,None,4,6])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    print(f"Test Case 1 Output (Recursive): {solution.maxSumBST(root1, use_recursive=True)}") # Expected: 20
    print(f"Test Case 1 Output (Iterative): {solution.maxSumBST(root1, use_recursive=False)}") # Expected: 20
    print("-" * 30)

    # Test case 2
    root2 = build_tree([4,3,None,1,2])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    print(f"Test Case 2 Output (Recursive): {solution.maxSumBST(root2, use_recursive=True)}") # Expected: 2
    print(f"Test Case 2 Output (Iterative): {solution.maxSumBST(root2, use_recursive=False)}") # Expected: 2
    print("-" * 30)

    # Test case 3
    root3 = build_tree([-4,-2,-5])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    print(f"Test Case 3 Output (Recursive): {solution.maxSumBST(root3, use_recursive=True)}") # Expected: 0
    print(f"Test Case 3 Output (Iterative): {solution.maxSumBST(root3, use_recursive=False)}") # Expected: 0
    print("-" * 30)
    
    # Test case 4: Single node BST
    root4 = build_tree([10])
    print(f"Test Case 4 Input: {tree_to_list(root4)}")
    print(f"Test Case 4 Output (Recursive): {solution.maxSumBST(root4, use_recursive=True)}") # Expected: 10
    print(f"Test Case 4 Output (Iterative): {solution.maxSumBST(root4, use_recursive=False)}") # Expected: 10
    print("-" * 30)

    # Test case 5: Tree is a valid BST
    root5 = build_tree([2,1,3])
    print(f"Test Case 5 Input: {tree_to_list(root5)}")
    print(f"Test Case 5 Output (Recursive): {solution.maxSumBST(root5, use_recursive=True)}") # Expected: 6
    print(f"Test Case 5 Output (Iterative): {solution.maxSumBST(root5, use_recursive=False)}") # Expected: 6
    print("-" * 30)

    # Test case 6: Large tree with mixed BSTs
    root6 = build_tree([5, 3, 7, 2, 4, 6, 8]) # A full BST
    print(f"Test Case 6 Input: {tree_to_list(root6)}")
    print(f"Test Case 6 Output (Recursive): {solution.maxSumBST(root6, use_recursive=True)}") # Expected: 35
    print(f"Test Case 6 Output (Iterative): {solution.maxSumBST(root6, use_recursive=False)}") # Expected: 35
    print("-" * 30)
