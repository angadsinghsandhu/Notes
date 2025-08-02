# File: Leetcode/Solutions/426_Convert_Binary_Search_Tree_to_Sorted_Doubly_Linked_List.py

"""
Problem Number: 426 (LeetCode) / 1534 (LintCode)
Problem Name: Convert Binary Search Tree to Sorted Doubly Linked List
Difficulty: Medium
Tags: Binary Search Tree, Linked List, Binary Tree, Divide and Conquer
Company (Frequency): Amazon (15), Facebook (10), Microsoft (8), Lyft (5), Google (4)
Leetcode Link: https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/
LintCode Link: https://www.lintcode.com/problem/1534/

DESCRIPTION

Convert a BST to a sorted circular doubly-linked list in-place. Think of the left and right pointers as synonymous to the previous and next pointers in a doubly-linked list.

Let's take the following BST as an example, it may help you understand the problem better:
       4
      /  \
     2    5
    / \
   1   3

We want to transform this BST into a circular doubly linked list. Each node in a doubly linked list has a predecessor and successor. For a circular doubly linked list, the predecessor of the first element is the last element, and the successor of the last element is the first element.

Specifically, we want to do the transformation in-place. After the transformation, the left pointer of the tree node should point to its predecessor, and the right pointer should point to its successor. We should return the pointer to the first element of the linked list.

The figure below shows the transformed BST. The solid line indicates the successor relationship, while the dashed line means the predecessor relationship.

Example 1:
Input: {4,2,5,1,3}
Output: "left:1->5->4->3->2  right:1->2->3->4->5"
Explanation: The output shows the doubly linked list from both directions, starting from the smallest node (1).

Example 2:
Input: {2,1,3}
Output: "left:1->3->2  right:1->2->3"

Constraints:
- The number of nodes in the tree is in the range [0, 100].
- -1000 <= Node.val <= 1000
"""

from typing import Optional, Any

# Definition for a Node.
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Helper to build a tree from a list (for testing)
def build_tree_from_list(values):
    if not values:
        return None
    nodes = [Node(val) if val is not None else None for val in values]
    root = nodes[0]
    queue = collections.deque([root])
    i = 1
    while queue and i < len(nodes):
        node = queue.popleft()
        if node:
            if i < len(nodes) and nodes[i]:
                node.left = nodes[i]
                queue.append(node.left)
            i += 1
            if i < len(nodes) and nodes[i]:
                node.right = nodes[i]
                queue.append(node.right)
            i += 1
    return root

# Helper to print the doubly linked list (for testing)
def print_doubly_linked_list(head: Optional[Node]):
    if not head:
        return "Empty list"
    
    # Print forward traversal
    forward_list = []
    current = head
    while True:
        forward_list.append(str(current.val))
        current = current.right
        if current == head:
            break
    
    # Print backward traversal
    backward_list = []
    current = head.left # Start from the last node
    while True:
        backward_list.append(str(current.val))
        current = current.left
        if current == head.left:
            break
    
    return f"left:{'->'.join(backward_list)}  right:{'->'.join(forward_list)}"

class Solution:
    """
    Thought Process:
    - The problem asks us to convert a Binary Search Tree (BST) into a sorted circular doubly linked list in-place.
    - The key property of a BST is that an in-order traversal (Left -> Node -> Right) visits the nodes in sorted order.
    - We can leverage this to build the linked list. As we visit each node in the in-order traversal, we can link it with the previously visited node.
    - We need two pointers to manage the linked list:
      - `head`: A pointer to the smallest node, which will be the head of the list.
      - `prev`: A pointer to the last node processed in the traversal, which will be the predecessor of the current node.
    - The conversion can be done either recursively or iteratively.

    Input:
        root: Optional[Node] - The root of the BST.

    Output:
        Optional[Node] - The head of the resulting circular doubly linked list.
    """

    def treeToDoublyList_Recursive(self, root: Optional[Node]) -> Optional[Node]:
        """
        Approach 1: Recursive In-order Traversal
        - Use a recursive helper function to perform the in-order traversal.
        - We'll need to maintain `head` and `prev` pointers. Since they need to be modified across recursive calls, they can be instance variables or passed by reference. Using instance variables is common in Python for this pattern.
        - The helper function `_inorder` takes a `node` as input.
          - Base case: If `node` is `None`, return.
          - Recurse on `node.left`.
          - Process the current `node`:
            - If `prev` is `None`, it means this is the first node we're visiting (the smallest element), so set `head = node`.
            - Otherwise, link `prev` to `node`: `prev.right = node` and `node.left = prev`.
            - Update `prev` to the current `node`.
          - Recurse on `node.right`.
        - After the traversal, the `head` and `prev` (which is now the largest node) will point to the ends of the list. We just need to connect them to make the list circular: `head.left = prev` and `prev.right = head`.
        - Finally, return the `head`.

        T.C.: O(N) - Each node is visited exactly once.
        S.C.: O(H) - For the recursion stack, where H is the height of the tree.
        """
        if not root:
            return None

        # Instance variables to keep track of the head and previous node
        self.head = None
        self.prev = None

        def _inorder(node: Optional[Node]):
            if not node:
                return

            _inorder(node.left)

            # Process the current node
            if not self.prev:
                # This is the first node (smallest element)
                self.head = node
            else:
                # Link the previous node to the current node
                self.prev.right = node
                node.left = self.prev
            
            # Update the previous node pointer
            self.prev = node

            _inorder(node.right)

        _inorder(root)
        
        # Connect the head and tail to form a circular list
        self.head.left = self.prev
        self.prev.right = self.head

        return self.head

    def treeToDoublyList_Iterative(self, root: Optional[Node]) -> Optional[Node]:
        """
        Approach 2: Iterative In-order Traversal
        - Use a stack to simulate the in-order traversal.
        - Maintain `head` and `prev` pointers as in the recursive approach.
        - The iterative in-order traversal logic is as follows:
          1. Go left as far as possible, pushing each node onto the stack.
          2. Pop a node from the stack. This is the next smallest element in the BST.
          3. Process the popped node (link it to the previous one).
          4. Then, go to the right child of the popped node and repeat the process.
        - After the loop finishes, connect the `head` and `prev` (tail) to complete the circular list.

        T.C.: O(N) - Each node is pushed and popped from the stack once.
        S.C.: O(H) - The stack can hold up to H nodes, where H is the height of the tree.
        """
        if not root:
            return None

        stack = []
        head = None
        prev = None
        current = root

        while current or stack:
            # Go left as far as possible
            while current:
                stack.append(current)
                current = current.left
            
            # Pop the next node to process (in-order)
            current = stack.pop()

            # Process the current node (link it)
            if not head:
                head = current
            
            if prev:
                prev.right = current
                current.left = prev
            
            # Update previous pointer
            prev = current
            
            # Go right to find the next node
            current = current.right

        # Connect the head and tail to form a circular list
        head.left = prev
        prev.right = head

        return head

    def treeToDoublyList(self, root: Optional[Node], use_recursive: Any = True) -> Optional[Node]:
        """
        Main entry point for the problem.
        Allows choosing between recursive and iterative solutions.
        """
        if use_recursive:
            return self.treeToDoublyList_Recursive(root)
        else:
            return self.treeToDoublyList_Iterative(root)

# Run and print sample test cases

if __name__ == "__main__":
    import collections
    solution = Solution()

    # Test case 1
    root1 = build_tree_from_list([4, 2, 5, 1, 3])
    print("Test Case 1 Input: [4,2,5,1,3]")
    dll1_recursive = solution.treeToDoublyList(root1, use_recursive=True)
    print(f"Test Case 1 Output (Recursive): {print_doubly_linked_list(dll1_recursive)}") # Expected: "left:1->5->4->3->2  right:1->2->3->4->5"
    root1 = build_tree_from_list([4, 2, 5, 1, 3]) # Rebuild for iterative test
    dll1_iterative = solution.treeToDoublyList(root1, use_recursive=False)
    print(f"Test Case 1 Output (Iterative): {print_doubly_linked_list(dll1_iterative)}") # Expected: "left:1->5->4->3->2  right:1->2->3->4->5"
    print("-" * 30)

    # Test case 2
    root2 = build_tree_from_list([2, 1, 3])
    print("Test Case 2 Input: [2,1,3]")
    dll2_recursive = solution.treeToDoublyList(root2, use_recursive=True)
    print(f"Test Case 2 Output (Recursive): {print_doubly_linked_list(dll2_recursive)}") # Expected: "left:1->3->2  right:1->2->3"
    root2 = build_tree_from_list([2, 1, 3]) # Rebuild for iterative test
    dll2_iterative = solution.treeToDoublyList(root2, use_recursive=False)
    print(f"Test Case 2 Output (Iterative): {print_doubly_linked_list(dll2_iterative)}") # Expected: "left:1->3->2  right:1->2->3"
    print("-" * 30)

    # Test case 3: Single node
    root3 = build_tree_from_list([10])
    print("Test Case 3 Input: [10]")
    dll3_recursive = solution.treeToDoublyList(root3, use_recursive=True)
    print(f"Test Case 3 Output (Recursive): {print_doubly_linked_list(dll3_recursive)}") # Expected: "left:10  right:10"
    root3 = build_tree_from_list([10])
    dll3_iterative = solution.treeToDoublyList(root3, use_recursive=False)
    print(f"Test Case 3 Output (Iterative): {print_doubly_linked_list(dll3_iterative)}") # Expected: "left:10  right:10"
    print("-" * 30)

    # Test case 4: Empty tree
    root4 = build_tree_from_list([])
    print("Test Case 4 Input: []")
    dll4_recursive = solution.treeToDoublyList(root4, use_recursive=True)
    print(f"Test Case 4 Output (Recursive): {print_doubly_linked_list(dll4_recursive)}") # Expected: "Empty list"
    dll4_iterative = solution.treeToDoublyList(root4, use_recursive=False)
    print(f"Test Case 4 Output (Iterative): {print_doubly_linked_list(dll4_iterative)}") # Expected: "Empty list"
    print("-" * 30)
