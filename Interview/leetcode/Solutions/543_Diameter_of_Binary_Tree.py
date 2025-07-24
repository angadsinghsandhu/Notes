# File: Leetcode/Solutions/Tree/543_Diameter_of_Binary_Tree.py

"""
Problem Number: 543
Problem Name: Diameter of Binary Tree
Difficulty: Easy
Tags: Tree, Depth-First Search, Binary Tree
Company (Frequency): Common tree problem, frequently seen in interviews.
Leetcode Link: <https://leetcode.com/problems/diameter-of-binary-tree/description/>

DESCRIPTION

Given the `root` of a binary tree, return the length of the `diameter` of the tree.
The `diameter` of a binary tree is the `length` of the longest path between any two nodes in a tree. This path may or may not pass through the `root`.
The `length` of a path between two nodes is represented by the number of edges between them.

---

#### Example 1:

Input:
root = [1,2,3,4,5]

Output:
3

Explanation:
3 is the length of the path [4,2,1,3] or [5,2,1,3].

---

#### Example 2:

Input:
root = [1,2]

Output:
1

---

#### Constraints:

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-100 <= Node.val <= 100`
"""

from typing import Optional
from helpers import TreeNode, build_tree

class Solution:
    """
    Thought Process for Diameter of Binary Tree:

    The diameter of a binary tree is the length of the longest path between any two nodes. This path can either:
    1. Pass through the root of the entire tree.
    2. Be entirely contained within the left subtree.
    3. Be entirely contained within the right subtree.

    The problem asks for the *length* of the path, which is defined as the number of edges.

    Key Idea:
    For any given node in the tree, the longest path passing *through* that node will be the sum of the "height" of its left subtree and the "height" of its right subtree, plus two edges (one connecting to the left child, one to the right child).
    Here, "height" of a subtree rooted at `child` is the number of edges on the longest path from `child` down to a leaf within that subtree.

    Definition of Height for this problem:
    - Height of an empty tree (None node): -1 (This is a conventional choice that makes a leaf node have height 0).
    - Height of a leaf node: 0 (0 edges from the leaf to itself).
    - Height of any other node `u`: `1 + max(height(u.left), height(u.right))` (1 edge from `u` to its taller child, plus the height of that child's subtree).

    The overall diameter of the tree is the maximum such path length calculated for *any* node in the tree.

    ---

    Approach 1: Recursive Depth-First Search (DFS) - Optimal

    We can solve this problem efficiently using a recursive DFS traversal. During the traversal, for each node, we will:
    1. Recursively calculate the height of its left subtree.
    2. Recursively calculate the height of its right subtree.
    3. Calculate the potential diameter passing *through* the current node: `(height_of_left_subtree + 1) + (height_of_right_subtree + 1) - 1` edges.
       This simplifies to `height_of_left_subtree + height_of_right_subtree + 1` edges. No, actually it is:
       `left_height + right_height + 2` because `left_height` is edges from left child to deep leaf and `right_height` is edges from right child to deep leaf, and we add the 2 edges connecting the current node to its children. This matches `max_depth_node(X.left) + max_depth_node(X.right)` where `max_depth_node` returns `1 + max(depths of children)`.

    Let's re-verify the definition of height for the recursive solution:
    `height(node)` returns the longest path in terms of *edges* from `node` to a leaf in its subtree.
    `height(None)` returns -1.
    `height(leaf_node)` returns 0.
    `height(parent_node)` returns `1 + max(height(parent_node.left), height(parent_node.right))`.

    Then, the diameter `through` a `current_node` is `(height(current_node.left) + 1) + (height(current_node.right) + 1)`. This counts the total edges if path passes through `current_node` and extends to deepest leaves on both sides. Example 1: path [4,2,1,3] has 3 edges.
    `height(4)` = 0, `height(5)` = 0.
    `height(2)` = `1 + max(height(4), height(5))` = `1 + max(0, 0)` = 1.
    `height(3)` = `1 + max(height(None), height(None))` = `1 + max(-1, -1)` = 0.
    `height(1)` = `1 + max(height(2), height(3))` = `1 + max(1, 0)` = 2.

    Now, diameter calculation:
    `diameter_through_node_X = height(X.left) + height(X.right) + 2` (edges).
    This counts `height(X.left)` edges from X.left down, plus 1 edge from X to X.left, plus `height(X.right)` edges from X.right down, plus 1 edge from X to X.right.
    So, total edges: `height(X.left) + height(X.right) + 2`.

    Algorithm:
    1. Initialize `self.max_diameter = 0` (to store the maximum diameter found so far).
    2. Define a helper function `_dfs_height(node: Optional[TreeNode]) -> int`:
        a. Base Case: If `node` is `None`, return -1.
        b. Recursive Step:
           i. Recursively call `left_height = _dfs_height(node.left)`.
           ii. Recursively call `right_height = _dfs_height(node.right)`.
           iii. Update `self.max_diameter`: The diameter passing through the current `node` is `left_height + right_height + 2`. Update `self.max_diameter = max(self.max_diameter, left_height + right_height + 2)`.
           iv. Return the height of the current subtree: `1 + max(left_height, right_height)`.
    3. Call `_dfs_height(root)`.
    4. Return `self.max_diameter`.

    T.C.: O(N) - Each node is visited exactly once.
    S.C.: O(H) - For the recursion stack, where H is the height of the tree. In the worst case (skewed tree), H = N, so O(N). In the best case (balanced tree), H = logN, so O(logN).

    ---

    Approach 2: Iterative Depth-First Search (DFS) - Optimal

    An iterative approach can mimic the post-order traversal used in the recursive solution. We need to process children before processing the parent to correctly calculate heights. A stack can be used for DFS, and a dictionary can store the computed heights of subtrees.

    Algorithm:
    1. Initialize `max_diameter = 0`.
    2. Handle edge case: If `root` is `None`, return 0.
    3. Initialize a stack to manage DFS traversal. Each element in the stack will be a tuple: `(node, state)`.
       - `state 0`: Node just pushed, need to process left child.
       - `state 1`: Left child processed, need to process right child.
       - `state 2`: Both children processed, ready to calculate height/diameter for this node.
    4. Initialize `height_map = {None: -1}`. This dictionary will store the computed height (edges) for each node.
    5. Push `(root, 0)` onto the stack.

    6. While the stack is not empty:
        a. Pop `(node, state)` from the stack.
        b. If `state == 0`:
           i. Push `(node, 1)` back onto the stack (mark for next stage: process right child).
           ii. If `node.left` exists, push `(node.left, 0)` onto the stack.
        c. Else if `state == 1`:
           i. Push `(node, 2)` back onto the stack (mark for final stage: process current node).
           ii. If `node.right` exists, push `(node.right, 0)` onto the stack.
        d. Else (`state == 2`): (This means both children (if any) have been processed, and their heights are in `height_map`).
           i. Retrieve `left_height = height_map.get(node.left, -1)`
           ii. Retrieve `right_height = height_map.get(node.right, -1)`
           iii. Update `max_diameter = max(max_diameter, left_height + right_height + 2)`.
           iv. Calculate and store the height of the current node: `height_map[node] = 1 + max(left_height, right_height)`.

    7. Return `max_diameter`.

    T.C.: O(N) - Each node is pushed onto the stack and processed a constant number of times.
    S.C.: O(N) - For the stack (in worst case skewed tree) and `height_map` dictionary (stores height for up to N nodes).
    """

    def diameterOfBinaryTree_Recursive(self, root: Optional[TreeNode]) -> int:
        """
        Recursive solution to find the diameter of a binary tree.
        T.C.: O(N), S.C.: O(H) (where H is tree height, max N in worst case).
        """
        self.max_diameter = 0  # Stores the maximum diameter found (in edges)

        def _dfs_height(node: Optional[TreeNode]) -> int:
            """
            Calculates the height of the subtree rooted at `node`.
            Height is defined as the number of edges on the longest path from `node` to a leaf.
            An empty tree (None node) has height -1.
            A leaf node has height 0.
            """
            if not node:
                return -1  # Height of an empty subtree (base case for edges)

            left_height = _dfs_height(node.left)
            right_height = _dfs_height(node.right)

            # Calculate the diameter passing through the current node:
            # (edges from left child to deepest leaf) + 1 (edge from node to left child)
            # + (edges from right child to deepest leaf) + 1 (edge from node to right child)
            # Sums up to left_height + right_height + 2
            self.max_diameter = max(self.max_diameter, left_height + right_height + 2)

            # Return the height of the current subtree (for its parent's calculation):
            # 1 (edge from current node to its taller child) + max(height of children subtrees)
            return 1 + max(left_height, right_height)
        
        _dfs_height(root)  # Start the DFS from the root
        return self.max_diameter

    def diameterOfBinaryTree_Iterative(self, root: Optional[TreeNode]) -> int:
        """
        Iterative solution to find the diameter of a binary tree using DFS (post-order traversal simulation).
        T.C.: O(N), S.C.: O(N) (for stack and height_map in worst case).
        """
        if not root:
            return 0

        max_diameter = 0
        
        # Stack for DFS traversal. Each element: (node, state)
        # state 0: initial visit, process left child
        # state 1: left child processed, process right child
        # state 2: both children processed, calculate height and update diameter for this node
        stack = [(root, 0)] 
        
        # Dictionary to store heights of processed subtrees.
        # Key: TreeNode, Value: height (number of edges from node to deepest leaf).
        # Initialize with None having height -1, consistent with recursive base case.
        height_map = {None: -1} 
        
        while stack:
            node, state = stack[-1] # Peek at the top element

            if state == 0: # First time visiting node: explore left child
                stack[-1] = (node, 1) # Update state for next visit
                if node.left:
                    stack.append((node.left, 0))
            elif state == 1: # Left child processed: explore right child
                stack[-1] = (node, 2) # Update state for next visit
                if node.right:
                    stack.append((node.right, 0))
            else: # state == 2: Both children processed (or non-existent): calculate this node's height and diameter
                stack.pop() # Remove node from stack as it's fully processed

                # Get heights of left and right subtrees from the map
                left_height = height_map.get(node.left, -1)
                right_height = height_map.get(node.right, -1)
                
                # Calculate the diameter passing through the current node and update max_diameter
                # This formula matches the recursive solution's logic.
                max_diameter = max(max_diameter, left_height + right_height + 2)
                
                # Calculate and store the height of the current node's subtree
                height_map[node] = 1 + max(left_height, right_height)
        
        return max_diameter

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Main entry point for the LeetCode problem.
        Utilizes the recursive DFS approach, which is often cleaner for tree problems.
        """
        return self.diameterOfBinaryTree_Recursive(root)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases: (input_tree_list, expected_diameter)
    test_cases = [
        ([1, 2, 3, 4, 5], 3),  # Example 1: path [4,2,1,3] or [5,2,1,3]
        ([1, 2], 1),           # Example 2: path [2,1]
        ([1], 0),              # Single node tree
        ([], 0),               # Empty tree
        ([1, None, 2, 3], 2),  # Skewed right: path [3,2,1]
        ([1, 2, None, 3, None, 4], 3), # Skewed left then right: [4,3,2,1]
        ([4,-7,-3,None,None,-9,-3,9,-7,-4,None,6,None,-6,-6,None,None,0,6,5,None,9,None,None,-1,-4,None,None,None,-2], 8), # Larger tree example
        ([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 6) # Full balanced tree of height 3
    ]

    print("--- Recursive Solution ---")
    for tree_list, expected_diameter in test_cases:
        root = build_tree(tree_list)
        result = solution.diameterOfBinaryTree_Recursive(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Diameter: {result}")
        print(f"Expected Diameter: {expected_diameter}")
        print(f"Status: {'Pass' if result == expected_diameter else 'Fail'}")
        print("-" * 30)

    print("\n--- Iterative Solution ---")
    for tree_list, expected_diameter in test_cases:
        root = build_tree(tree_list)
        result = solution.diameterOfBinaryTree_Iterative(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Diameter: {result}")
        print(f"Expected Diameter: {expected_diameter}")
        print(f"Status: {'Pass' if result == expected_diameter else 'Fail'}")
        print("-" * 30)

    print("\n--- Main Entry Point (Recursive Optimal) ---")
    for tree_list, expected_diameter in test_cases:
        root = build_tree(tree_list)
        result = solution.diameterOfBinaryTree(root)
        print(f"Input Tree: {tree_list}")
        print(f"Output Diameter: {result}")
        print(f"Expected Diameter: {expected_diameter}")
        print(f"Status: {'Pass' if result == expected_diameter else 'Fail'}")
        print("-" * 30)