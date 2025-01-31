# TODO: new

# File: Leetcode/Solutions/426_Convert_Binary_Search_Tree_to_Sorted_Doubly_Linked_List.py

"""
Problem Number: 426
Problem Name: Convert Binary Search Tree to Sorted Doubly Linked List
Difficulty: Medium
Tags: Tree, Depth-First Search, Binary Search Tree, Linked List, Binary Tree, Doubly-Linked List
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/description/

DESCRIPTION

Convert a Binary Search Tree (BST) to a sorted circular doubly-linked list in-place. 
The left and right pointers of each node in the BST should be repurposed to act as the previous and next pointers in the doubly-linked list.

The list should be circular, meaning the predecessor of the first element is the last element, and the successor of the last element is the first element.

---

#### Example:
**Input:**
```plaintext
    4
   / \
  2   5
 / \
1   3
```

**Output:**
```plaintext
1 <--> 2 <--> 3 <--> 4 <--> 5
|                             |
-------------------------------
```

**Explanation:**  
The BST is converted into a sorted circular doubly-linked list. The smallest element (1) is the head of the list.

#### Constraints:
- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`
- All `Node.val` are unique.
"""

from typing import Optional, List

# Definition for a Node.
class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Thought Process:
    - The problem requires converting a BST into a sorted circular doubly-linked list in-place.
    - An in-order traversal of the BST will yield the nodes in sorted order.
    - During the traversal, we can adjust the left and right pointers of each node to create the doubly-linked list.
    - Finally, we connect the first and last nodes to make the list circular.

    Input:
        root: Node - The root of the BST.

    Output:
        Node - The head of the sorted circular doubly-linked list.
    """

    def treeToDoublyList(self, root: Optional[Node]) -> Optional[Node]:
        """
        Approach:
        - Perform an in-order traversal of the BST.
        - During the traversal, adjust the left and right pointers of each node to create the doubly-linked list.
        - Connect the first and last nodes to make the list circular.

        T.C.: O(n) - Each node is visited once during the in-order traversal.
        S.C.: O(h) - The recursion stack uses space proportional to the height of the tree.
        """
        if not root:
            return None

        # Initialize head and prev pointers
        self.head = None
        self.prev = None

        # Perform in-order traversal to convert the BST to a doubly-linked list
        self._in_order_traversal(root)

        # Connect the first and last nodes to make the list circular
        self.head.left = self.prev
        self.prev.right = self.head

        # Return the head of the doubly-linked list
        return self.head

    def _in_order_traversal(self, node: Optional[Node]) -> None:
        """
        Helper function to perform in-order traversal and adjust pointers.
        """
        if not node:
            return

        # Traverse the left subtree
        self._in_order_traversal(node.left)

        # Process the current node
        if not self.prev:
            # If prev is None, this is the smallest node (head of the list)
            self.head = node
        else:
            # Link the previous node with the current node
            self.prev.right = node
            node.left = self.prev

        # Update prev to the current node
        self.prev = node

        # Traverse the right subtree
        self._in_order_traversal(node.right)

    # in-place solution
    def treeToDoublyList_in_place(self, root: 'Node') -> 'Node':
        if not root:
            return None
        
        self.head = None
        self.prev = None
        
        def inorder(node):
            if not node:
                return
            inorder(node.left)
            
            if self.prev:
                # Link the previous node with the current node
                self.prev.right = node
                node.left = self.prev
            else:
                # The first node, set the head
                self.head = node
            self.prev = node
            
            inorder(node.right)
        
        # Perform in-order traversal to convert BST to sorted doubly linked list
        inorder(root)
        
        # Connect the head and tail to make it circular
        self.prev.right = self.head
        self.head.left = self.prev
        
        return self.head

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to create a BST from a list of values
    def create_bst(values: List[int], index: int = 0) -> Optional[Node]:
        if index >= len(values) or values[index] is None:
            return None
        root = Node(values[index])
        root.left = create_bst(values, 2 * index + 1)
        root.right = create_bst(values, 2 * index + 2)
        return root

    # Test case 1
    bst1 = create_bst([4, 2, 5, 1, 3])
    head1 = solution.treeToDoublyList(bst1)
    # Print the circular doubly-linked list
    result1 = []
    current = head1
    while True:
        result1.append(current.val)
        current = current.right
        if current == head1:
            break
    print(result1)  # Output: [1, 2, 3, 4, 5]

    # Test case 2 (Single node)
    bst2 = create_bst([1])
    head2 = solution.treeToDoublyList(bst2)
    # Print the circular doubly-linked list
    result2 = []
    current = head2
    while True:
        result2.append(current.val)
        current = current.right
        if current == head2:
            break
    print(result2)  # Output: [1]

    # Test case 3 (Empty tree)
    bst3 = create_bst([])
    head3 = solution.treeToDoublyList(bst3)
    print(head3)  # Output: None