# File: Leetcode/Solutions/Bottom_View_of_Binary_Tree.py
# Note: This is a common interview problem from platforms like GeeksforGeeks and
# is a variation of vertical traversal problems.

"""
Problem Name: Bottom View of a Binary Tree
Difficulty: Medium
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree, Hash Map
Company (Frequency): Amazon (10), Google (8), Microsoft (7), Facebook (5)
GeeksforGeeks Link: https://www.geeksforgeeks.org/bottom-view-of-a-binary-tree/

DESCRIPTION

Given a binary tree, return an array of its nodes representing the bottom view of the binary tree from left to right.

Note:
- The bottom view of a binary tree is the set of nodes visible when the tree is viewed from the bottom.
- If there are multiple bottom-most nodes for a horizontal distance from the root, then the latter one in the level traversal is considered.

---

#### Example 1:
Input:
(A binary tree visual, with 20 at root)

Output:

[5, 10, 3, 14, 25]

Explanation:
The nodes 5, 10, 3, 14, 25 are the bottom-most nodes at their respective horizontal distances.

#### Example 2:
(Another binary tree visual)

Output:

(Visual representation of bottom view)

#### Constraints:
- The number of nodes in the tree can be in the range [0, 1000].
- Node values are typically in a reasonable integer range.
"""

import collections
from typing import List, Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The bottom view of a binary tree consists of the last node we encounter at each horizontal distance (HD) from the root.
    - As with top view and vertical traversal, horizontal distance is the key:
      - The root has an HD of 0.
      - A left child's HD is its parent's HD - 1.
      - A right child's HD is its parent's HD + 1.
    - We use a hash map (dictionary) to store the value of the node for each horizontal distance. The value in the map will be continuously overwritten, ensuring we have the "bottom-most" node.
    - The order of traversal matters to get the correct result when nodes have the same horizontal distance.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        List[int] - A list of the node values in the bottom view, sorted by horizontal distance.
    """

    def bottomView_BFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 1: Iterative BFS (Level Order Traversal)
        - BFS processes nodes level by level, from top to bottom.
        - As we iterate through the nodes, we'll use a dictionary `hd_map` to store the node's value for its horizontal distance.
        - Each time we encounter a node at a certain horizontal distance, we update the value in the dictionary.
        - Because BFS processes nodes from top to bottom, the last node seen at a particular HD will be the one at the deepest level, which is the definition of a bottom view node.
        - We use a queue to store tuples of `(node, hd)`.

        T.C.: O(N log K) or O(N) - N for traversal, log K for sorting the dictionary keys at the end.
        S.C.: O(N) - The queue and hash map can both store up to N items.
        """
        if not root:
            return []

        hd_map = {}
        queue = collections.deque([(root, 0)])

        while queue:
            node, hd = queue.popleft()

            # Always update the map with the current node's value.
            # This ensures that for a given HD, we store the deepest node
            # seen so far in a top-down traversal.
            hd_map[hd] = node.val

            if node.left:
                queue.append((node.left, hd - 1))
            
            if node.right:
                queue.append((node.right, hd + 1))
        
        # After traversal, collect the nodes in order of their horizontal distance
        result = []
        for hd in sorted(hd_map.keys()):
            result.append(hd_map[hd])
            
        return result

    def bottomView_DFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 2: Recursive DFS
        - With DFS, we need to keep track of both the horizontal distance and the depth (level) to determine the bottom-most node.
        - We use a hash map `hd_map` where the key is the horizontal distance and the value is a tuple of `(node_val, depth)`.
        - The process:
          1. Perform a pre-order traversal (or any DFS traversal).
          2. For each node, if the `hd` is not in the map, add it.
          3. If the `hd` is already in the map, check if the current node's `depth` is greater than the stored node's `depth`. If so, update the map.
        - This ensures that for each horizontal distance, we store the node at the maximum depth.

        T.C.: O(N log K) or O(N) - N for traversal, log K for sorting keys.
        S.C.: O(N) - For the recursion stack and the hash map.
        """
        if not root:
            return []
            
        hd_map = {} # hd -> (node_val, depth)

        def dfs(node: Optional[TreeNode], hd: int, depth: int):
            if not node:
                return
            
            # If hd is new, or if the current node is deeper than the stored node, update.
            if hd not in hd_map or depth >= hd_map[hd][1]:
                hd_map[hd] = (node.val, depth)

            dfs(node.left, hd - 1, depth + 1)
            dfs(node.right, hd + 1, depth + 1)

        dfs(root, 0, 0)
        
        result = []
        for hd in sorted(hd_map.keys()):
            result.append(hd_map[hd][0])
        return result


    def bottomView(self, root: Optional[TreeNode], use_bfs: Any = True) -> List[int]:
        """
        Main entry point for the problem.
        Allows choosing between DFS and BFS solutions. BFS is often simpler to reason about.
        """
        if use_bfs:
            return self.bottomView_BFS(root)
        else:
            return self.bottomView_DFS(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case from problem description
    #       20
    #      /  \
    #     8   22
    #    / \    \
    #   5   3   25
    #      / \
    #     10 14
    root1 = build_tree([20, 8, 22, 5, 3, None, 25, None, None, 10, 14])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    print(f"Test Case 1 Output (BFS): {solution.bottomView(root1, use_bfs=True)}")  # Expected: [5, 10, 3, 14, 25]
    print(f"Test Case 1 Output (DFS): {solution.bottomView(root1, use_bfs=False)}") # Expected: [5, 10, 3, 14, 25]
    print("-" * 30)

    # Test case with multiple nodes at the same HD
    #       1
    #      / \
    #     2   3
    #      \
    #       4
    #        \
    #         5
    #          \
    #           6
    # HDs: -1(2), 0(1, 4), 1(3, 5), 2(6)
    # Bottom view should be 2, 4, 5, 6
    root2 = build_tree([1, 2, 3, None, 4, None, None, None, None, None, 5, None, None, None, 6])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    print(f"Test Case 2 Output (BFS): {solution.bottomView(root2, use_bfs=True)}")  # Expected: [2, 4, 5, 6]
    print(f"Test Case 2 Output (DFS): {solution.bottomView(root2, use_bfs=False)}") # Expected: [2, 4, 5, 6]
    print("-" * 30)

    # Test case 3: Empty tree
    root3 = build_tree([])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    print(f"Test Case 3 Output (BFS): {solution.bottomView(root3, use_bfs=True)}")  # Expected: []
    print(f"Test Case 3 Output (DFS): {solution.bottomView(root3, use_bfs=False)}") # Expected: []
    print("-" * 30)
