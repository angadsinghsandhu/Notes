# TODO: new

# File: Leetcode/Solutions/108_Convert_Sorted_Array_to_Binary_Search_Tree.py

"""
Problem Number: 108
Problem Name: Convert Sorted Array to Binary Search Tree
Difficulty: Easy
Tags: Tree, Binary Search Tree, Array, Divide and Conquer, Binary Tree
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

DESCRIPTION

Given an integer array `nums` where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.

A height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.

---

#### Example 1:
**Input:**
```plaintext
nums = [-10,-3,0,5,9]
```

**Output:**
```plaintext
[0,-3,9,-10,null,5]
```

**Explanation:**  
One possible height-balanced BST is:
```
      0
     / \
   -3   9
   /   /
-10  5
```

#### Example 2:
**Input:**
```plaintext
nums = [1,3]
```

**Output:**
```plaintext
[3,1]
```

**Explanation:**  
One possible height-balanced BST is:
```
      3
     /
    1
```
Alternatively, `[1,null,3]` is also a valid height-balanced BST.

#### Constraints:
- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is sorted in a strictly increasing order.
"""

from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem requires converting a sorted array into a height-balanced binary search tree (BST).
    - A height-balanced BST can be constructed by selecting the middle element of the array as the root and recursively building the left and right subtrees from the left and right halves of the array.

    Input:
        nums: List[int] - A sorted array of integers.

    Output:
        TreeNode - The root of the height-balanced BST.
    """

    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        """
        Approach:
        - Use a recursive helper function to build the BST.
        - Select the middle element of the array as the root.
        - Recursively build the left subtree from the left half of the array.
        - Recursively build the right subtree from the right half of the array.

        T.C.: O(n) - Each element is visited once to construct the BST.
        S.C.: O(log n) - The recursion stack uses space proportional to the height of the tree.
        """
        def buildBST(left: int, right: int) -> Optional[TreeNode]:
            # Base case: If the left index exceeds the right index, return None
            if left > right:
                return None

            # Find the middle index
            mid = (left + right) // 2

            # Create the root node with the middle element
            root = TreeNode(nums[mid])

            # Recursively build the left and right subtrees
            root.left = buildBST(left, mid - 1)
            root.right = buildBST(mid + 1, right)

            return root

        # Start the recursive process with the full range of the array
        return buildBST(0, len(nums) - 1)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to print the tree in level-order traversal (BFS)
    def print_tree(root: Optional[TreeNode]) -> List[Optional[int]]:
        if not root:
            return []
        from collections import deque
        queue = deque([root])
        result = []
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        return result

    # Test case 1
    nums1 = [-10, -3, 0, 5, 9]
    bst1 = solution.sortedArrayToBST(nums1)
    print(print_tree(bst1))  # Output: [0, -3, 9, -10, None, 5]

    # Test case 2
    nums2 = [1, 3]
    bst2 = solution.sortedArrayToBST(nums2)
    print(print_tree(bst2))  # Output: [3, 1] or [1, None, 3]

    # Test case 3 (Single element)
    nums3 = [1]
    bst3 = solution.sortedArrayToBST(nums3)
    print(print_tree(bst3))  # Output: [1]

    # Test case 4 (Empty array)
    nums4 = []
    bst4 = solution.sortedArrayToBST(nums4)
    print(print_tree(bst4))  # Output: []