# File: Leetcode/Solutions/199_Binary_Tree_Right_Side_View.py

"""
Problem Number: 199
Problem Name: Binary Tree Right Side View
Difficulty: Medium
Tags: Tree, Depth-First Search, Breadth-First Search, Binary Tree, Neetcode 150
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/binary-tree-right-side-view/description/

DESCRIPTION

Given the root of a binary tree, imagine yourself standing on the right side of it. Return the values of the nodes you can see ordered from top to bottom.

---

#### Example 1:
**Input:**
```plaintext
root = [1,2,3,null,5,null,4]
```

**Output:**
```plaintext
[1,3,4]
```

**Explanation:**  
The right side view of the tree is `[1,3,4]`.

#### Example 2:
**Input:**
```plaintext
root = [1,2,3,4,null,null,null,5]
```

**Output:**
```plaintext
[1,3,4,5]
```

**Explanation:**  
The right side view of the tree is `[1,3,4,5]`.

#### Constraints:
- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`
"""

from collections import deque
from typing import List, Optional
from helpers import TreeNode, build_tree

class Solution:
    """
    Thought Process:
    - The problem requires returning the values of nodes visible from the right side of the binary tree.
    - This can be achieved by performing a level-order traversal (BFS) and recording the last node at each level.
    - Alternatively, a depth-first search (DFS) approach can be used to traverse the tree and keep track of the rightmost node at each depth.

    Input:
        root: TreeNode - The root of the binary tree.

    Output:
        List[int] - The values of the nodes visible from the right side of the tree.
    """

    def rightSideView_Iterative(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 1: BFS (Level-Order Traversal)
        - Use a queue to perform a level-order traversal.
        - At each level, record the value of the last node in the queue.
        - This ensures that we capture the rightmost node at each level.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(n) - The queue can hold up to n/2 nodes in the worst case (last level of a balanced tree).
        """
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.popleft()
                # Record the last node in the current level
                if i == level_size - 1:
                    result.append(node.val)
                # Add children to the queue
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result

    def rightSideView_Recursive(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach 2: DFS (Depth-First Search)
        - Perform a DFS traversal, prioritizing the right subtree.
        - Keep track of the current depth and record the first node encountered at each depth.
        - This ensures that we capture the rightmost node at each depth.

        T.C.: O(n) - Each node is visited once.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        result = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            # If this is the first node at the current depth, add it to the result
            if depth == len(result):
                result.append(node.val)
            # Traverse the right subtree first
            dfs(node.right, depth + 1)
            # Traverse the left subtree
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return result
    
    def rightSideView(self, root: Optional[TreeNode], flag=True) -> List[int]:
        """
        Main entry point for the LeetCode problem.
        Calls the iterative solution as a standard optimal approach.
        """
        if flag: 
            return self.rightSideView_Recursive(root)
        else: 
            return self.rightSideView_Iterative(root)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    tree1 = build_tree([1, 2, 3, None, 5, None, 4])
    print(solution.rightSideView(tree1, True))  # Output: [1, 3, 4]
    print(solution.rightSideView(tree1, False))  # Output: [1, 3, 4]

    # Test case 2
    tree2 = build_tree([1, 2, 3, 4, None, None, None, 5])
    print(solution.rightSideView(tree2, True))  # Output: [1, 3, 4, 5]
    print(solution.rightSideView(tree2, False))  # Output: [1, 3, 4, 5]

    # Test case 3 (Single node)
    tree3 = build_tree([1])
    print(solution.rightSideView(tree3, True))  # Output: [1]
    print(solution.rightSideView(tree3, False))  # Output: [1]

    # Test case 4 (Empty tree)
    tree4 = build_tree([])
    print(solution.rightSideView(tree4, True))  # Output: []
    print(solution.rightSideView(tree4, False))  # Output: []
