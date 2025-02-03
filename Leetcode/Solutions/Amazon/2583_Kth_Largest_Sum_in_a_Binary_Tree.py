# File: Leetcode/Solutions/2583_Kth_Largest_Sum_in_a_Binary_Tree.py

"""
Problem Number: 2583
Problem Name: Kth Largest Sum in a Binary Tree
Difficulty: Medium
Tags: Tree, Breadth-First Search, Binary Search
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/kth-largest-sum-in-a-binary-tree/description/

DESCRIPTION

Given the root of a binary tree and a positive integer k, return the kth largest level sum in the tree. 
The level sum is the sum of the values of all nodes at the same level. If there are fewer than k levels in the tree, return -1.

---

#### Example 1:
**Input:**
```plaintext
root = [5,8,9,2,1,3,7,4,6], k = 2
```

**Output:**
```plaintext
13
```

**Explanation:**  
The level sums are:
- Level 1: 5.
- Level 2: 8 + 9 = 17.
- Level 3: 2 + 1 + 3 + 7 = 13.
- Level 4: 4 + 6 = 10.
The 2nd largest level sum is 13.

#### Example 2:
**Input:**
```plaintext
root = [1,2,null,3], k = 1
```

**Output:**
```plaintext
3
```

**Explanation:**  
The largest level sum is 3.

#### Constraints:
- The number of nodes in the tree is `n`.
- `2 <= n <= 10^5`
- `1 <= Node.val <= 10^6`
- `1 <= k <= n`
"""

from collections import deque
from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem requires finding the kth largest level sum in a binary tree.
    - We can use a breadth-first search (BFS) approach to traverse the tree level by level and calculate the sum of each level.
    - After collecting the sums of all levels, we sort them in descending order and return the kth largest sum.

    Input:
        root: TreeNode - The root of the binary tree.
        k: int - The kth largest level sum to find.

    Output:
        int - The kth largest level sum, or -1 if there are fewer than k levels.
    """

    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        """
        Approach:
        - Use a queue to perform a level-order traversal (BFS) of the tree.
        - For each level, calculate the sum of the node values and store it in a list.
        - Sort the list of level sums in descending order and return the kth largest sum.
        - If there are fewer than k levels, return -1.

        T.C.: O(n) - Each node is visited once during BFS.
        S.C.: O(n) - The queue and the list of level sums can hold up to n nodes.
        """
        if not root:
            return -1

        level_sums = []  # List to store the sum of each level
        queue = deque([root])  # Queue for BFS

        while queue:
            level_size = len(queue)
            level_sum = 0  # Sum of the current level

            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val

                # Add children to the queue
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            level_sums.append(level_sum)

        # If there are fewer than k levels, return -1
        if len(level_sums) < k:
            return -1

        # Sort the level sums in descending order and return the kth largest sum
        # Use heap to optimize the sorting process
        level_sums.sort(reverse=True)
        return level_sums[k - 1]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to create a binary tree from a list of values
    def create_tree(values: List[int], index: int = 0) -> Optional[TreeNode]:
        if index >= len(values) or values[index] is None:
            return None
        root = TreeNode(values[index])
        root.left = create_tree(values, 2 * index + 1)
        root.right = create_tree(values, 2 * index + 2)
        return root

    # Test case 1
    tree1 = create_tree([5, 8, 9, 2, 1, 3, 7, 4, 6])
    print(solution.kthLargestLevelSum(tree1, 2))  # Output: 13

    # Test case 2
    tree2 = create_tree([1, 2, None, 3])
    print(solution.kthLargestLevelSum(tree2, 1))  # Output: 3

    # Test case 3 (Fewer than k levels)
    tree3 = create_tree([1, 2, 3])
    print(solution.kthLargestLevelSum(tree3, 4))  # Output: -1

    # Test case 4 (Single node)
    tree4 = create_tree([1])
    print(solution.kthLargestLevelSum(tree4, 1))  # Output: 1