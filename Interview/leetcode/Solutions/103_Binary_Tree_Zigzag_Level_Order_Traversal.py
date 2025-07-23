# File: Leetcode/Solutions/Amazon/103_Binary_Tree_Zigzag_Level_Order_Traversal.py

"""
Problem Number: 103
Problem Name: Binary Tree Zigzag Level Order Traversal
Difficulty: Medium
Tags: Tree, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (30)
Leetcode Link: https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

DESCRIPTION

Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

---

#### Example 1:
**Input:**
```plaintext
root = [3,9,20,null,null,15,7]
```

**Output:**
```plaintext
[[3],[20,9],[15,7]]
```

**Explanation:**  
The tree is traversed level by level, starting from the root (3), then the next level from right to left (20, 9), and finally the next level from left to right (15, 7).

#### Constraints:
- The number of nodes in the tree is in the range [0, 2000].
- -100 <= Node.val <= 100
"""

from typing import List, Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem involves traversing a binary tree level by level and returning the nodes' values in a list of lists, alternating the direction of traversal for each level.
    - A Breadth-First Search (BFS) approach is suitable for this problem because BFS processes nodes level by level.
    - We can use a queue to keep track of nodes at each level and process them in order. For each level, we alternate the direction of traversal by reversing the list of values if necessary.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        List[List[int]] - A list of lists containing the nodes' values level by level, alternating the direction of traversal.
    """

    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach:
        - Use a queue to perform a BFS traversal of the tree.
        - For each level, process all nodes in the queue and add their children to the queue for the next level.
        - Store the values of nodes at each level in a separate list and append it to the result.
        - Alternate the direction of traversal for each level by reversing the list of values if necessary.

        T.C.: O(n) - We visit each node once.
        S.C.: O(w) - The space used by the queue, where w is the maximum width of the tree.
        """
        # Initialize the result list
        result = []
        
        # If the tree is empty, return the empty list
        if not root:
            return result
        
        # Use a queue to perform BFS
        queue = deque([root])
        
        # Variable to control the direction of traversal
        left_to_right = True
        
        # Loop until the queue is empty
        while queue:
            # Temporary list to store values of nodes at the current level
            level_values = []
            
            # Process all nodes at the current level
            for _ in range(len(queue)):
                # Dequeue the node
                current_node = queue.popleft()
                
                # Add the node's value to the temporary list
                level_values.append(current_node.val)
                
                # Enqueue the left child if it exists
                if current_node.left:
                    queue.append(current_node.left)
                
                # Enqueue the right child if it exists
                if current_node.right:
                    queue.append(current_node.right)
            
            # Append the current level's values to the result, reversing if necessary
            if not left_to_right:
                level_values.reverse()
            result.append(level_values)
            
            # Toggle the direction for the next level
            left_to_right = not left_to_right
        
        # Return the result
        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    root1 = TreeNode(3)
    root1.left = TreeNode(9)
    root1.right = TreeNode(20)
    root1.right.left = TreeNode(15)
    root1.right.right = TreeNode(7)
    print(solution.zigzagLevelOrder(root1))  # Output: [[3], [20, 9], [15, 7]]

    # Test case 2
    root2 = TreeNode(1)
    print(solution.zigzagLevelOrder(root2))  # Output: [[1]]

    # Test case 3
    root3 = None
    print(solution.zigzagLevelOrder(root3))  # Output: []