# File: Leetcode/Solutions/652_Find_Duplicate_Subtrees.py

"""
Problem Number: 652
Problem Name: Find Duplicate Subtrees
Difficulty: Medium
Tags: Hash Table, Tree, Depth-First Search, Binary Tree
Company (Frequency): Facebook (10), Google (8), Amazon (7)
Leetcode Link: https://leetcode.com/problems/find-duplicate-subtrees/description/

DESCRIPTION

Given the `root` of a binary tree, return all duplicate subtrees.
For each kind of duplicate subtrees, you only need to return the root node of any one of them.
Two trees are duplicate if they have the same structure with the same node values.

---

#### Example 1:

Input:
root = [1,2,3,4,null,2,4,null,null,4]

Output:

[[2,4],[4]]

#### Example 2:

Input:
root = [2,1,1]

Output:

[[1]]

#### Example 3:

Input:
root = [2,2,2,3,null,3,null]

Output:

[[2,3],[3]]

#### Constraints:

  - The number of the nodes in the tree will be in the range `[1, 5000]`
  - `-200 <= Node.val <= 200`
"""

import collections
from typing import List, Optional, Any
from helpers import TreeNode, build_tree, tree_to_list

class Solution:
    """
    Thought Process:
    - The core idea is to uniquely identify each subtree and then count occurrences of these identifications.
    - If a subtree's identification (serialization) appears more than once, it's a duplicate.
    - We need a way to serialize a subtree into a string (or tuple) such that two subtrees with the same structure and values produce the same serialization.
    - A post-order traversal is suitable for serialization because it processes children first, allowing us to build the string from the bottom up.

    Input:
        root: Optional[TreeNode] - The root of the binary tree.

    Output:
        List[Optional[TreeNode]] - A list of root nodes of duplicate subtrees.
    """

    def findDuplicateSubtrees_DFS(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        """
        Approach: DFS with Serialization and Hash Map
        - Perform a post-order DFS traversal.
        - For each node, recursively get the serialization strings of its left and right children.
        - Combine these, along with the current node's value, to form the current subtree's serialization string (e.g., "val(left_ser)(right_ser)"). Use "#" for null children.
        - Store these serialization strings in a hash map (dictionary) along with their frequencies.
        - If a serialization string's frequency becomes 2, it means we've found a duplicate subtree for the first time, so add its root node to the result list.

        T.C.: O(N * L) - Where N is the number of nodes and L is the average length of a serialization string.
                          In the worst case (skewed tree), L can be O(N), leading to O(N^2).
                          For a balanced tree, L is O(log N).
                          String concatenation and hash map operations contribute to L.
        S.C.: O(N * L) - For storing all serialization strings in the hash map.
                         O(H) for recursion stack, where H is height of tree.
        """
        duplicates = []
        # Stores {serialization_string: count}
        subtree_counts = collections.defaultdict(int)

        def serialize(node: Optional[TreeNode]) -> str:
            if not node:
                return "#" # Represent null nodes with a unique marker

            # Post-order traversal: serialize left, then right, then current node
            left_ser = serialize(node.left)
            right_ser = serialize(node.right)

            # Combine them to form a unique string for the current subtree
            # Format: "current_val(left_serialization)(right_serialization)"
            current_subtree_ser = f"{node.val}({left_ser})({right_ser})"

            subtree_counts[current_subtree_ser] += 1

            # If this serialization has been seen exactly twice, it means
            # this is the first time we're identifying it as a duplicate,
            # so add the node to our result list.
            if subtree_counts[current_subtree_ser] == 2:
                duplicates.append(node)
            
            return current_subtree_ser

        serialize(root)
        return duplicates

    def findDuplicateSubtrees(self, root: Optional[TreeNode], use_dfs: Any = True) -> List[Optional[TreeNode]]:
        """
        Main entry point for the LeetCode problem.
        Currently uses the DFS with serialization approach as it's the standard.
        """
        return self.findDuplicateSubtrees_DFS(root)

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Helper to convert list of TreeNodes to list of lists for pretty printing output
    def convert_nodes_to_lists(nodes: List[Optional[TreeNode]]) -> List[List[Optional[int]]]:
        return [tree_to_list(node) for node in nodes]

    # Test case 1
    root1 = build_tree([1, 2, 3, 4, None, 2, 4, None, None, 4])
    print(f"Test Case 1 Input: {tree_to_list(root1)}")
    output1 = solution.findDuplicateSubtrees(root1)
    print(f"Test Case 1 Output: {convert_nodes_to_lists(output1)}") # Expected: [[2,4],[4]] (order might vary)
    print("-" * 30)

    # Test case 2
    root2 = build_tree([2, 1, 1])
    print(f"Test Case 2 Input: {tree_to_list(root2)}")
    output2 = solution.findDuplicateSubtrees(root2)
    print(f"Test Case 2 Output: {convert_nodes_to_lists(output2)}") # Expected: [[1]]
    print("-" * 30)

    # Test case 3
    root3 = build_tree([2, 2, 2, 3, None, 3, None])
    print(f"Test Case 3 Input: {tree_to_list(root3)}")
    output3 = solution.findDuplicateSubtrees(root3)
    print(f"Test Case 3 Output: {convert_nodes_to_lists(output3)}") # Expected: [[2,3],[3]] (order might vary)
    print("-" * 30)

    # Test case 4: No duplicates
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print(f"Test Case 4 Input: {tree_to_list(root4)}")
    output4 = solution.findDuplicateSubtrees(root4)
    print(f"Test Case 4 Output: {convert_nodes_to_lists(output4)}") # Expected: []
    print("-" * 30)

    # Test case 5: Empty tree (constraint says 1 to 5000 nodes, but good to test edge cases)
    # root5 = build_tree([]) # Constraint: 1 <= nodes <= 5000, so empty tree not valid
    # print(f"Test Case 5 Input: {tree_to_list(root5)}")
    # output5 = solution.findDuplicateSubtrees(root5)
    # print(f"Test Case 5 Output: {convert_nodes_to_lists(output5)}") # Expected: []
    # print("-" * 30)

    # Test case 6: Single node tree
    root6 = build_tree([10])
    print(f"Test Case 6 Input: {tree_to_list(root6)}")
    output6 = solution.findDuplicateSubtrees(root6)
    print(f"Test Case 6 Output: {convert_nodes_to_lists(output6)}") # Expected: []
    print("-" * 30)

    # Test case 7: Tree with multiple duplicates
    root7 = build_tree([0,0,0,0,None,None,0,None,None,None,0])
    print(f"Test Case 7 Input: {tree_to_list(root7)}")
    output7 = solution.findDuplicateSubtrees(root7)
    # Expected: [[0], [0,None,0]] or similar. Depends on which 'kind' of duplicate root is returned.
    # The output will be the root node of the first encountered duplicate.
    print(f"Test Case 7 Output: {convert_nodes_to_lists(output7)}")
    print("-" * 30)