# File: Leetcode/Solutions/987_Vertical_Order_Traversal_of_a_Binary_Tree.py

"""
Problem Number: 987
Problem Name: Vertical Order Traversal of a Binary Tree
Difficulty: Hard
Tags: Hash Table, Tree, Depth-First Search, Breadth-First Search, Sorting, Binary Tree
Company (Frequency): Google (12), Facebook (8), Amazon (5)
Leetcode Link: https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/description/

DESCRIPTION

Given the root of a binary tree, calculate the vertical order traversal of the binary tree.

For each node at position (row, col), its left and right children will be at positions (row + 1, col - 1) and (row + 1, col + 1) respectively. The root of the tree is at (0, 0).

The vertical order traversal of a binary tree is a list of top-to-bottom orderings for each column index starting from the leftmost column and ending on the rightmost column. There may be multiple nodes in the same row and same column. In such a case, sort these nodes by their values.

Return the vertical order traversal of the binary tree.

---

#### Example 1:

Input:
root = [3,9,20,null,null,15,7]

Output:

[[9],[3,15],[20],[7]]

Explanation:

Column -1: Only node 9 is in this column.
Column 0: Nodes 3 and 15 are in this column in that order from top to bottom.
Column 1: Only node 20 is in this column.
Column 2: Only node 7 is in this column.

#### Example 2:

Input:

root = [1,2,3,4,5,6,7]

Output:

[[4],[2],[1,5,6],[3],[7]]

Explanation:

Column -2: Only node 4 is in this column.
Column -1: Only node 2 is in this column.
Column 0: Nodes 1, 5, and 6 are in this column.
1 is at the top, so it comes first.
5 and 6 are at the same position (2, 0), so we order them by their value, 5 before 6.
Column 1: Only node 3 is in this column.
Column 2: Only node 7 is in this column.

#### Constraints:

  - The number of nodes in the tree is in the range [1, 1000].
  - 0 <= Node.val <= 1000
"""

import collections
from typing import List, Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The problem asks for a vertical order traversal, which means grouping nodes by their column index.
    - Nodes at the same column and row should be sorted by their value.
    - We need to keep track of the (row, col) for each node. The root is (0,0).
      - Left child: (row + 1, col - 1)
      - Right child: (row + 1, col + 1)
    - Since we need to process by column, then by row (top-to-bottom), and then by value, a BFS approach combined with a way to store and sort results seems appropriate.
    - A DFS approach can also be used, but requires careful handling of node sorting, as DFS does not inherently guarantee level-by-level processing. We'll store (row, value) for each column and sort later.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        List[List[int]] - The vertical order traversal of the tree.
    """

    def verticalTraversal_Recursive(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach: DFS (Depth-First Search) with Coordinate Tracking and Sorting.
        - Use a recursive helper function to perform DFS.
        - Pass `node`, `row`, and `col` to the recursive function.
        - Store nodes in a dictionary `column_map = {col: [(row, val), ...]}`.
        - Since DFS doesn't guarantee top-to-bottom order for nodes in the same column,
          we will need to sort the list of `(row, val)` pairs for each column after the traversal.

        T.C.: O(N log N)
              - O(N) for DFS traversal.
              - O(N log N) for sorting: Similar to BFS, sorting all nodes within their respective columns.
        S.C.: O(N)
              - Recursion stack can go up to height of tree (H), worst case H=N.
              - `column_map` stores all N nodes.
        """
        if not root:
            return []

        # Map to store nodes by column: {col: [(row, val), ...]}
        column_map = collections.defaultdict(list)
        min_col = float('inf')
        max_col = float('-inf')

        def dfs(node: Optional[TreeNode], row: int, col: int) -> None:
            nonlocal min_col, max_col # To modify min_col and max_col from the outer scope
            if not node:
                return

            column_map[col].append((row, node.val))
            min_col = min(min_col, col)
            max_col = max(max_col, col)

            if node.left:
                dfs(node.left, row + 1, col - 1)
            if node.right:
                dfs(node.right, row + 1, col + 1)

        dfs(root, 0, 0)

        result = []
        # Iterate through columns from min_col to max_col
        for col in range(min_col, max_col + 1):
            # Sort nodes within each column: first by row, then by value
            column_nodes = sorted(column_map[col])
            
            # Extract just the values
            result.append([val for row, val in column_nodes])
            
        return result


    def verticalTraversal_Itreative(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach: BFS (Level-Order Traversal) with Coordinate Tracking and Sorting.
        - Use a queue for BFS, storing tuples of (node, row, col).
        - Use a defaultdict (or a dictionary) to store nodes grouped by their column index.
        For each column, we'll store a list of (row, value) pairs.
        - After BFS, iterate through the columns in sorted order.
        - For each column, sort the (row, value) pairs first by row, then by value.
        - Extract just the values into the final result list.

        T.C.: O(N log N)
            - O(N) for BFS traversal.
            - O(N log N) for sorting: In the worst case, all nodes might be in one column,
                or distributed such that sorting each column's list (which could be up to N elements) dominates.
                Specifically, if 'C' is the number of distinct columns and 'N_c' is the number of nodes in column 'c',
                the sorting complexity is sum(N_c * log N_c) over all 'c'. In the worst case, this approaches O(N log N).
        S.C.: O(N)
            - Queue can hold up to N/2 nodes.
            - `column_map` stores all N nodes.
        """
        if not root:
            return []

        # Map to store nodes by column: {col: [(row, val), ...]}
        column_map = collections.defaultdict(list)
        # Queue for BFS: [(node, row, col)]
        queue = collections.deque([(root, 0, 0)])

        min_col = float('inf')
        max_col = float('-inf')

        while queue:
            node, row, col = queue.popleft()
            
            column_map[col].append((row, node.val))
            
            min_col = min(min_col, col)
            max_col = max(max_col, col)

            if node.left:
                queue.append((node.left, row + 1, col - 1))
            if node.right:
                queue.append((node.right, row + 1, col + 1))
        
        result = []
        # Iterate through columns from min_col to max_col
        for col in range(min_col, max_col + 1):
            # Sort nodes within each column: first by row, then by value
            # The lambda function defines the sorting key: (row, value)
            column_nodes = sorted(column_map[col])
            
            # Extract just the values
            result.append([val for row, val in column_nodes])
            
        return result

    def verticalTraversal(self, root: Optional[TreeNode], use_recursive: Any = True) -> List[List[int]]:
        """
        Main entry point for the LeetCode problem.
        Allows choosing between recursive (DFS) and iterative (BFS) solutions.
        """
        if use_recursive:
            return self.verticalTraversal_Recursive(root)
        else:
            return self.verticalTraversal_Itreative(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    print(f"Test Case 1 Output (Recursive): {solution.verticalTraversal(root1, use_recursive=True)}") # Expected: [[9],[3,15],[20],[7]]
    print(f"Test Case 1 Output (Iterative): {solution.verticalTraversal(root1, use_recursive=False)}") # Expected: [[9],[3,15],[20],[7]]
    print("-" * 30)

    # Test case 2
    root2 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    print(f"Test Case 2 Output (Recursive): {solution.verticalTraversal(root2, use_recursive=True)}") # Expected: [[4],[2],[1,5,6],[3],[7]]
    print(f"Test Case 2 Output (Iterative): {solution.verticalTraversal(root2, use_recursive=False)}") # Expected: [[4],[2],[1,5,6],[3],[7]]
    print("-" * 30)

    # Test case 3 (Same as example 2, but 5 and 6 swapped to test value sorting)
    root3 = build_tree([1, 2, 3, 4, 6, 5, 7]) # Nodes 5 and 6 swapped in input list
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    print(f"Test Case 3 Output (Recursive): {solution.verticalTraversal(root3, use_recursive=True)}") # Expected: [[4],[2],[1,5,6],[3],[7]]
    print(f"Test Case 3 Output (Iterative): {solution.verticalTraversal(root3, use_recursive=False)}") # Expected: [[4],[2],[1,5,6],[3],[7]]
    print("-" * 30)

    # Test case 4 (Single node)
    root4 = build_tree([10])
    print(f"Test Case 4 Input: {tree_to_list(root4)}")
    print(f"Test Case 4 Output (Recursive): {solution.verticalTraversal(root4, use_recursive=True)}") # Expected: [[10]]
    print(f"Test Case 4 Output (Iterative): {solution.verticalTraversal(root4, use_recursive=False)}") # Expected: [[10]]
    print("-" * 30)

    # Test case 5 (Empty tree)
    root5 = build_tree([])
    print(f"Test Case 5 Input: {tree_to_list(root5)}")
    print(f"Test Case 5 Output (Recursive): {solution.verticalTraversal(root5, use_recursive=True)}") # Expected: []
    print(f"Test Case 5 Output (Iterative): {solution.verticalTraversal(root5, use_recursive=False)}") # Expected: []
    print("-" * 30)
