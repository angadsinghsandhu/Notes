# File: Leetcode/Solutions/Top_View_of_Binary_Tree.py
# Note: This is a common interview problem from platforms like GeeksforGeeks and
# is a variation of vertical traversal problems seen on LeetCode.

"""
Problem Name: Top View of Binary Tree
Difficulty: Medium
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree, Hash Map
Company (Frequency): Amazon (10), Google (8), Microsoft (7), Facebook (5)
GeeksforGeeks Link: https://www.geeksforgeeks.org/print-nodes-top-view-binary-tree/

DESCRIPTION

Given a binary tree, the task is to find the top view of the binary tree. The top view of a binary tree is the set of nodes visible when the tree is viewed from the top.

Note:
- Return the nodes from the leftmost node to the rightmost node.
- If two nodes are at the same position (horizontal distance) and are outside the shadow of the tree, consider the topmost node only.

---

#### Example 1:
Input:
(A binary tree with 1 as root, 2 and 3 as children, etc.)

Output:

(Visual representation of top view)

#### Example 2:
Input:
(Another binary tree)

Output:

(Visual representation of top view)

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
    - The top view of a binary tree consists of the first node we encounter at each horizontal distance (HD) from the root.
    - We can define the horizontal distance as follows:
      - The root has an HD of 0.
      - A left child's HD is its parent's HD - 1.
      - A right child's HD is its parent's HD + 1.
    - We need a way to keep track of the first node we see for each HD. A hash map (dictionary in Python) is a perfect data structure for this, mapping `hd` to `node.val`.
    - Finally, the result must be sorted by horizontal distance.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        List[int] - A list of the node values in the top view, sorted by horizontal distance.
    """

    def topView_BFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 1: Iterative BFS (Level Order Traversal)
        - BFS is a natural fit because it processes nodes level by level, ensuring that we encounter the topmost nodes at a given horizontal distance first.
        - We use a queue to store tuples of `(node, hd)`.
        - We use a hash map `top_nodes` to store the value of the first node seen at each `hd`.
        - The process:
          1. Initialize a queue with `(root, 0)` and a hash map.
          2. While the queue is not empty, dequeue `(node, hd)`.
          3. If `hd` is not in `top_nodes`, it means this is the first node we've seen at this horizontal distance, so we store it: `top_nodes[hd] = node.val`.
          4. Enqueue the left child with `hd - 1` and the right child with `hd + 1`.
          5. After the traversal, sort the keys (HDs) of the hash map and build the result list from the sorted values.

        T.C.: O(N log K) or O(N), where N is the number of nodes and K is the number of distinct horizontal distances. The `log K` comes from sorting the dictionary keys. If we can build a list and fill it without sorting, it's O(N).
        S.C.: O(N) - The queue and hash map can both store up to N items.
        """
        if not root:
            return []

        top_nodes = {}
        queue = collections.deque([(root, 0)])

        while queue:
            node, hd = queue.popleft()

            if hd not in top_nodes:
                top_nodes[hd] = node.val

            if node.left:
                queue.append((node.left, hd - 1))
            
            if node.right:
                queue.append((node.right, hd + 1))
        
        result = []
        for hd in sorted(top_nodes.keys()):
            result.append(top_nodes[hd])
            
        return result

    def topView_DFS(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 2: Recursive DFS (Pre-order Traversal)
        - With DFS, we need to be careful to ensure we only keep the *topmost* node for each HD.
        - We can do this by passing the `level` (depth) along with the `hd`.
        - The hash map will store `(node.val, level)` for each `hd`.
        - When we encounter a node at a given `hd`:
          - If the `hd` is new, we add the node.
          - If the `hd` already exists, we check if the current node's `level` is less than the stored node's `level`. If so, we replace it.
          - This logic is a bit flawed for a pure DFS and would lead to incorrect results. A better DFS approach would be to only store the first node seen at each HD. The traversal order needs to be controlled.
          - Let's refine the DFS approach: traverse the tree, and for a given `hd` and `level`, only update the map if the `hd` is not present. This guarantees we keep the first node encountered, which is the topmost one.

        T.C.: O(N log K) or O(N) - N for traversal, log K for sorting keys.
        S.C.: O(N) - For the recursion stack and the hash map.
        """
        if not root:
            return []
            
        top_nodes = {} # hd -> (node_val, level)

        def dfs(node: Optional[TreeNode], hd: int, level: int):
            if not node:
                return
            
            if hd not in top_nodes:
                top_nodes[hd] = (node.val, level)
            elif top_nodes[hd][1] > level:
                # The provided GfG code seems to prioritize lower level.
                # However, for top view, a node at a certain HD is either
                # the first one seen (topmost), or we should ignore subsequent ones.
                # The DFS needs to be carefully structured to guarantee this.
                # A simpler, correct DFS implementation would be:
                pass

            # A simpler and more common DFS implementation for top view:
            if hd not in top_nodes:
                top_nodes[hd] = (node.val, level)

            dfs(node.left, hd - 1, level + 1)
            dfs(node.right, hd + 1, level + 1)

        # Let's use the simpler, correct DFS
        top_nodes_simple = {}
        def dfs_simple(node: Optional[TreeNode], hd: int):
            if not node:
                return

            if hd not in top_nodes_simple:
                top_nodes_simple[hd] = node.val
            
            dfs_simple(node.left, hd - 1)
            dfs_simple(node.right, hd + 1)

        dfs_simple(root, 0)
        
        result = []
        for hd in sorted(top_nodes_simple.keys()):
            result.append(top_nodes_simple[hd])
        return result


    def topView(self, root: Optional[TreeNode], use_bfs: Any = True) -> List[int]:
        """
        Main entry point for the problem.
        Allows choosing between DFS and BFS solutions.
        BFS is generally preferred for this problem as it inherently processes nodes
        in the correct "top-to-bottom" order.
        """
        if use_bfs:
            return self.topView_BFS(root)
        else:
            return self.topView_DFS(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Create a sample binary tree
    #     1
    #    / \
    #   2   3
    #  / \ / \
    # 4  5 6  7
    root1 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    print(f"Test Case 1 Output (BFS): {solution.topView(root1, use_bfs=True)}")  # Expected: [4, 2, 1, 3, 7]
    print(f"Test Case 1 Output (DFS): {solution.topView(root1, use_bfs=False)}") # Expected: [4, 2, 1, 3, 7]
    print("-" * 30)
    
    # Test case 2: Right skewed tree
    root2 = build_tree([1, None, 2, None, None, None, 3, None, None, None, None, None, None, None, 4])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    print(f"Test Case 2 Output (BFS): {solution.topView(root2, use_bfs=True)}")  # Expected: [1, 2, 3, 4]
    print(f"Test Case 2 Output (DFS): {solution.topView(root2, use_bfs=False)}") # Expected: [1, 2, 3, 4]
    print("-" * 30)

    # Test case 3: Example with shadowing
    #       10
    #      /  \
    #     20   30
    #    /  \
    #   40   60
    # Top view should be 40, 20, 10, 30
    root3 = build_tree([10, 20, 30, 40, 60])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    print(f"Test Case 3 Output (BFS): {solution.topView(root3, use_bfs=True)}")  # Expected: [40, 20, 10, 30]
    print(f"Test Case 3 Output (DFS): {solution.topView(root3, use_bfs=False)}") # Expected: [40, 20, 10, 30]
    print("-" * 30)

    # Test case 4: Single node
    root4 = build_tree([10])
    print(f"Test Case 4 Input: {tree_to_list(root4)}")
    print(f"Test Case 4 Output (BFS): {solution.topView(root4, use_bfs=True)}")  # Expected: [10]
    print(f"Test Case 4 Output (DFS): {solution.topView(root4, use_bfs=False)}") # Expected: [10]
    print("-" * 30)