# File: Leetcode/Solutions/Amazon/102_Binary_Tree_Level_Order_Traversal.py

"""
Problem Number: 102
Problem Name: Binary Tree Level Order Traversal
Difficulty: Medium
Tags: Tree, Breadth-First Search, Binary Tree
Company (Frequency): Amazon (35)
Leetcode Link: https://leetcode.com/problems/binary-tree-level-order-traversal/description/

DESCRIPTION

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

---

#### Example 1:
**Input:**
```plaintext
root = [3,9,20,null,null,15,7]
```

**Output:**
```plaintext
[[3],[9,20],[15,7]]
```

**Explanation:**  
The tree is traversed level by level, starting from the root (3), then its children (9 and 20), and finally the next level (15 and 7).

#### Constraints:
- The number of nodes in the tree is in the range [0, 2000].
- -1000 <= Node.val <= 1000
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
    - The problem involves traversing a binary tree level by level and returning the nodes' values in a list of lists.
    - A Breadth-First Search (BFS) approach is suitable for this problem because BFS processes nodes level by level.
    - We can use a queue to keep track of nodes at each level and process them in order.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        List[List[int]] - A list of lists containing the nodes' values level by level.
    """

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach:
        - Use a queue to perform a BFS traversal of the tree.
        - For each level, process all nodes in the queue and add their children to the queue for the next level.
        - Store the values of nodes at each level in a separate list and append it to the result.

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
            
            # Append the current level's values to the result
            result.append(level_values)
        
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
    print(solution.levelOrder(root1))  # Output: [[3], [9, 20], [15, 7]]

    # Test case 2
    root2 = TreeNode(1)
    print(solution.levelOrder(root2))  # Output: [[1]]

    # Test case 3
    root3 = None
    print(solution.levelOrder(root3))  # Output: []