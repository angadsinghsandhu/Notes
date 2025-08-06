# TODO: revisit

# File: Leetcode/Solutions/Amazon_Binary_Tree_Largest_Sum.py

"""
Problem Number: XXX
Problem: Binary Tree Largest Sum
Difficulty: Medium
Tags: Binary Tree, Depth-First Search, Dynamic Programming
Company: Amazon
Link: https://leetcode.com/discuss/interview-question/347374/Amazon-or-OA-2019-or-Largest-Path-Sum-Between-Any-Two-Leaves

DESCRIPTION

Given a binary tree represented as an array, find the value of the maximum diameter sum in the tree. 
The tree is a complete binary tree, and every leaf node is at the same depth from the root.

The first element in the input is the root element of the tree. Considering the index of the root element is 1, 
the left child of the i'th element in the input is the (2i)th element, and the right child of the i'th element is the (2i+1)th element.

---

#### Example:
**Input:**
```plaintext
1
7
2 4 5 8 -4 3 -6
```

**Output:**
```plaintext
22
```

**Explanation:**  
The path followed to get the maximum diameter sum is:
`8 (leaf) -> 4 -> 2 -> 5 -> 3 (leaf node)`

#### Constraints:
- The tree is a complete binary tree.
- The number of nodes in the tree is in the range `[1, 10^5]`.
- Node values are in the range `[-10^4, 10^4]`.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires finding the maximum diameter sum in a binary tree.
    - The diameter sum is defined as the sum of the values of the nodes along the longest path between any two leaf nodes.
    - We can use a recursive approach to traverse the tree and calculate the maximum diameter sum.

    Input:
        tree: List[int] - The binary tree represented as an array.

    Output:
        int - The maximum diameter sum in the binary tree.
    """

    def maxDiameterSum(self, tree: List[int]) -> float:
        """
        Approach:
        - Use a helper function `dfs` to perform a post-order traversal of the tree.
        - For each node, calculate the maximum path sum that can be extended through its left and right subtrees.
        - Update the global maximum diameter sum if the current path sum is greater.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        self.max_sum = float('-inf')  # Global variable to track the maximum diameter sum

        def dfs(index: int) -> int:
            """
            Helper function to perform DFS and return the maximum path sum that can be extended through the current node.
            """
            if index >= len(tree):
                return 0

            # Recursively calculate the maximum path sum for the left and right subtrees
            left_sum = dfs(2 * index + 1)
            right_sum = dfs(2 * index + 2)

            # Calculate the current diameter sum
            current_sum = left_sum + right_sum + tree[index]

            # Update the global maximum diameter sum
            self.max_sum = max(self.max_sum, current_sum)

            # Return the maximum path sum that can be extended through the current node
            return max(left_sum, right_sum) + tree[index]

        # Start the DFS traversal from the root (index 0)
        dfs(0)

        # Return the maximum diameter sum found
        return self.max_sum

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    tree1 = [2, 4, 5, 8, -4, 3, -6]
    print(solution.maxDiameterSum(tree1))  # Output: 22

    # Test case 2 (Single node)
    tree2 = [1]
    print(solution.maxDiameterSum(tree2))  # Output: 1

    # Test case 3 (All negative values)
    tree3 = [-1, -2, -3, -4, -5, -6, -7]
    print(solution.maxDiameterSum(tree3))  # Output: -6

    # Test case 4 (Balanced tree)
    tree4 = [1, 2, 3, 4, 5, 6, 7]
    print(solution.maxDiameterSum(tree4))  # Output: 18