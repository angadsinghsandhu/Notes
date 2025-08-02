# File: Leetcode/Solutions/113_Path_Sum_II.py

"""
Problem Number: 113
Problem Name: Path Sum II
Difficulty: Medium
Tags: Backtracking, Tree, Depth-First Search, Binary Tree
Company (Frequency): Amazon (10), Microsoft (7), Google (5)
Leetcode Link: https://leetcode.com/problems/path-sum-ii/description/

DESCRIPTION

Given the `root` of a binary tree and an integer `targetSum`, return all root-to-leaf paths where the sum of the node values in the path equals `targetSum`. Each path should be returned as a list of the node values, not node references.

A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.

---

#### Example 1:

Input:
root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22

Output:

[[5,4,11,2],[5,8,4,5]]

Explanation:
There are two paths whose sum equals targetSum:
5 + 4 + 11 + 2 = 22
5 + 8 + 4 + 5 = 22

#### Example 2:

Input:
root = [1,2,3], targetSum = 5

Output:

[]

#### Example 3:

Input:
root = [1,2], targetSum = 0

Output:

[]

#### Constraints:

  - The number of nodes in the tree is in the range `[0, 5000]`.
  - `-1000 <= Node.val <= 1000`.
  - `-1000 <= targetSum <= 1000`.
"""

from typing import List, Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The problem asks for all root-to-leaf paths that sum to a specific target.
    - This is a classic backtracking problem on a tree. We explore all possible paths from the root.
    - A Depth-First Search (DFS) approach is ideal for traversing all root-to-leaf paths.
    - We can use a recursive helper function that keeps track of:
      - The current node.
      - The remaining sum needed to reach the target.
      - The current path taken so far.
    - The recursive function will explore the left and right children.
    - A base case is when a leaf node is reached. At a leaf node, we check if the remaining sum is equal to the leaf's value. If so, we've found a valid path, and we add it to our results list.
    - The key to backtracking is to remove the current node from the path when we return from a recursive call, to allow exploration of other branches. In a recursive solution, this "backtracking" is implicitly handled by the function call stack.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.
        targetSum: int - The target sum for the paths.

    Output:
        List[List[int]] - A list of all valid root-to-leaf paths.
    """

    def pathSum_Recursive(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        """
        Approach 1: Recursive (DFS) with Backtracking
        - We'll define a helper function that performs the DFS traversal.
        - The main function initializes the result list and calls the helper.

        T.C.: O(N) - We visit each node once.
        S.C.: O(H) - For the recursion stack, where H is the height of the tree.
        """
        result = []
        path = []

        def dfs(node: Optional[TreeNode], current_sum: int) -> None:
            if not node:
                return

            path.append(node.val)
            current_sum += node.val

            # Check for a leaf node
            if not node.left and not node.right:
                if current_sum == targetSum:
                    # Found a valid path, add a copy to the result
                    result.append(list(path))
            else:
                # Recurse on children
                dfs(node.left, current_sum)
                dfs(node.right, current_sum)

            # Backtrack: remove the current node from the path
            path.pop()

        dfs(root, 0)
        return result

    def pathSum_Iterative(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        """
        Approach 2: Iterative DFS using a Stack
        - This approach uses an explicit stack to simulate the recursion.
        - The stack will store tuples of `(node, current_path, current_sum)`.
        - We will need to handle path building and sum calculation manually.

        T.C.: O(N) - Each node is pushed and popped from the stack once.
        S.C.: O(H) - The stack can hold up to H nodes in the worst case.
        """
        if not root:
            return []

        result = []
        # Stack stores (node, path_list, current_sum)
        stack = [(root, [root.val], root.val)]

        while stack:
            node, path, current_sum = stack.pop()

            # Check if it's a leaf node and if the sum is correct
            if not node.left and not node.right and current_sum == targetSum:
                result.append(path)
                continue

            # Push children to the stack (with updated path and sum)
            if node.right:
                new_path = list(path)
                new_path.append(node.right.val)
                stack.append((node.right, new_path, current_sum + node.right.val))
            
            if node.left:
                new_path = list(path)
                new_path.append(node.left.val)
                stack.append((node.left, new_path, current_sum + node.left.val))

        return result

    def pathSum(self, root: Optional[TreeNode], targetSum: int, use_recursive: Any = True) -> List[List[int]]:
        """
        Main entry point for the LeetCode problem.
        Allows choosing between recursive (DFS) and iterative (DFS) solutions.
        """
        if use_recursive:
            return self.pathSum_Recursive(root, targetSum)
        else:
            return self.pathSum_Iterative(root, targetSum)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    target1 = 22
    print(f"Test Case 1 Input: root={tree_to_list(root1)}, targetSum={target1}")
    print(f"Test Case 1 Output (Recursive): {solution.pathSum(root1, target1, use_recursive=True)}")  # Expected: [[5,4,11,2],[5,8,4,5]]
    print(f"Test Case 1 Output (Iterative): {solution.pathSum(root1, target1, use_recursive=False)}")  # Expected: [[5,4,11,2],[5,8,4,5]] (order might vary)
    print("-" * 30)

    # Test case 2
    root2 = build_tree([1, 2, 3])
    target2 = 5
    print(f"Test Case 2 Input: root={tree_to_list(root2)}, targetSum={target2}")
    print(f"Test Case 2 Output (Recursive): {solution.pathSum(root2, target2, use_recursive=True)}")  # Expected: []
    print(f"Test Case 2 Output (Iterative): {solution.pathSum(root2, target2, use_recursive=False)}")  # Expected: []
    print("-" * 30)

    # Test case 3
    root3 = build_tree([1, 2])
    target3 = 0
    print(f"Test Case 3 Input: root={tree_to_list(root3)}, targetSum={target3}")
    print(f"Test Case 3 Output (Recursive): {solution.pathSum(root3, target3, use_recursive=True)}")  # Expected: []
    print(f"Test Case 3 Output (Iterative): {solution.pathSum(root3, target3, use_recursive=False)}")  # Expected: []
    print("-" * 30)

    # Test case 4: Empty tree
    root4 = build_tree([])
    target4 = 1
    print(f"Test Case 4 Input: root={tree_to_list(root4)}, targetSum={target4}")
    print(f"Test Case 4 Output (Recursive): {solution.pathSum(root4, target4, use_recursive=True)}")  # Expected: []
    print(f"Test Case 4 Output (Iterative): {solution.pathSum(root4, target4, use_recursive=False)}")  # Expected: []
    print("-" * 30)

    # Test case 5: Single node
    root5 = build_tree([10])
    target5 = 10
    print(f"Test Case 5 Input: root={tree_to_list(root5)}, targetSum={target5}")
    print(f"Test Case 5 Output (Recursive): {solution.pathSum(root5, target5, use_recursive=True)}")  # Expected: [[10]]
    print(f"Test Case 5 Output (Iterative): {solution.pathSum(root5, target5, use_recursive=False)}")  # Expected: [[10]]
    print("-" * 30)
