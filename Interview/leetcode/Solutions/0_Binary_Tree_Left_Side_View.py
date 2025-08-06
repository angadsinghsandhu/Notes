# File: Leetcode/Solutions/0_Binary_Tree_Left_Side_View.py
# Note: The problem "Left View of a Binary Tree" is a variation of LeetCode 199.
# LeetCode itself does not have a dedicated "Left View" problem, but it's a very common
# interview question. This solution will be structured similarly to a LeetCode problem.

"""
Problem Name: Left View of a Binary Tree
Difficulty: Easy/Medium
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (10), Microsoft (8), Google (7), Facebook (5)
Leetcode Link: (This is a common interview problem, but not a direct LeetCode problem)
GeeksforGeeks Link: https://www.geeksforgeeks.org/print-left-view-binary-tree/

DESCRIPTION

Given a Binary Tree, the task is to print the left view of the Binary Tree. The left view of a Binary Tree is a set of leftmost nodes for every level.

---

#### Example 1:

Input:
root = [1, 2, 3, 4, 5, null, null]

Output:

[1, 2, 4]

Explanation:
From the left side of the tree, only the nodes 1, 2, and 4 are visible.

#### Example 2:

Input:
root = [1, 2, 3, null, null, 4, null, null, 5, null, null]

Output:

[1, 2, 4, 5]

Explanation:
From the left side of the tree, the nodes 1, 2, 4, and 5 are visible.

#### Constraints:
  - The number of nodes in the tree is in the range [0, 1000].
  - -1000 <= Node.val <= 1000
"""

import collections
from typing import List, Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The left view of a binary tree consists of the first node encountered at each level when traversing the tree.
    - Two main approaches can solve this problem efficiently:
      1. Depth-First Search (DFS) or Pre-order Traversal: We can traverse the tree recursively. By keeping track of the current level and the maximum level seen so far, we can determine if a node is the first one at its level.
      2. Breadth-First Search (BFS) or Level Order Traversal: We can traverse the tree level by level. The first node we encounter at each level is guaranteed to be the leftmost one.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        List[int] - A list of the node values in the left view.
    """

    def leftView_DFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 1: Recursive DFS (Pre-order Traversal)
        - We use a recursive helper function that takes the current node, its level (depth), and the result list.
        - We also need to keep track of the maximum level we have visited so far. This can be done with an instance variable or by passing it in the function signature.
        - The traversal order is important: to get the leftmost node, we must visit the left child before the right child.
        - When we visit a node, we check if its level is greater than the current maximum level. If it is, this means we're seeing a node for a new level for the first time, and because of our traversal order, it must be the leftmost node of that level.

        T.C.: O(N) - Each node is visited once.
        S.C.: O(H) - The recursion stack depth is equal to the height of the tree.
        """
        if not root:
            return []

        result: List[int] = []
        self.max_level_visited = -1

        def preorder_dfs(node: Optional[TreeNode], level: int):
            if not node:
                return

            if level > self.max_level_visited:
                # This is the first time we've reached this level,
                # so this node is the leftmost node of the level.
                result.append(node.val)
                self.max_level_visited = level

            # Traverse left child first to ensure we find the leftmost node
            preorder_dfs(node.left, level + 1)
            # Then traverse the right child
            preorder_dfs(node.right, level + 1)

        preorder_dfs(root, 0)
        return result

    def leftView_BFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 2: Iterative BFS (Level Order Traversal)
        - A queue-based level order traversal naturally processes the tree level by level.
        - For each level, the first element dequeued from the queue will be the leftmost node of that level.
        - We can use a loop that runs `level_size` times to process all nodes at the current level. We append the value of the very first node of each level to our result.

        T.C.: O(N) - We visit each node once.
        S.C.: O(W) - Where W is the maximum width of the tree. In the worst case (a complete binary tree), this can be O(N).
        """
        if not root:
            return []

        result: List[int] = []
        queue = collections.deque([root])

        while queue:
            level_size = len(queue)
            
            for i in range(level_size):
                curr: Optional[TreeNode] = queue.popleft()

                # If it's the first node of the current level, it's in the left view
                if i == 0:
                    result.append(curr.val)
                
                if curr.left:
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)
        
        return result


    def leftView(self, root: Optional[TreeNode], use_dfs: Any = True) -> List[int]:
        """
        Main entry point for the problem.
        Allows choosing between DFS and BFS solutions.
        """
        if use_dfs:
            return self.leftView_DFS(root)
        else:
            return self.leftView_BFS(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = build_tree([1, 2, 3, 4, 5, None, None])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    print(f"Test Case 1 Output (DFS): {solution.leftView(root1, use_dfs=True)}")  # Expected: [1, 2, 4]
    print(f"Test Case 1 Output (BFS): {solution.leftView(root1, use_dfs=False)}") # Expected: [1, 2, 4]
    print("-" * 30)

    # Test case 2
    root2 = build_tree([1, 2, 3, None, None, 4, None, None, 5, None, None])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    print(f"Test Case 2 Output (DFS): {solution.leftView(root2, use_dfs=True)}")  # Expected: [1, 2, 4, 5]
    print(f"Test Case 2 Output (BFS): {solution.leftView(root2, use_dfs=False)}") # Expected: [1, 2, 4, 5]
    print("-" * 30)

    # Test case 3: Right skewed tree
    root3 = build_tree([1, None, 2, None, None, None, 3, None, None, None, None, None, None, None, 4])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    print(f"Test Case 3 Output (DFS): {solution.leftView(root3, use_dfs=True)}")  # Expected: [1, 2, 3, 4]
    print(f"Test Case 3 Output (BFS): {solution.leftView(root3, use_dfs=False)}") # Expected: [1, 2, 3, 4]
    print("-" * 30)

    # Test case 4: Single node
    root4 = build_tree([10])
    print(f"Test Case 4 Input: {tree_to_list(root4)}")
    print(f"Test Case 4 Output (DFS): {solution.leftView(root4, use_dfs=True)}")  # Expected: [10]
    print(f"Test Case 4 Output (BFS): {solution.leftView(root4, use_dfs=False)}") # Expected: [10]
    print("-" * 30)

    # Test case 5: Empty tree
    root5 = build_tree([])
    print(f"Test Case 5 Input: {tree_to_list(root5)}")
    print(f"Test Case 5 Output (DFS): {solution.leftView(root5, use_dfs=True)}")  # Expected: []
    print(f"Test Case 5 Output (BFS): {solution.leftView(root5, use_dfs=False)}") # Expected: []
    print("-" * 30)