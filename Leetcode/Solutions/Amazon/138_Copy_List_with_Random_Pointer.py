# TODO: new

# File: Leetcode/Solutions/138_Copy_List_with_Random_Pointer.py

"""
Problem Number: 138
Problem Name: Copy List with Random Pointer
Difficulty: Medium
Tags: Hash Table, Linked List
Company (Frequency): Amazon (15), Microsoft (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/copy-list-with-random-pointer/description/

DESCRIPTION

A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list or `null`.

Construct a deep copy of the list. The deep copy should consist of exactly `n` brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the `next` and `random` pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.

---

#### Example 1:
**Input:**
```plaintext
head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**Output:**
```plaintext
[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**Explanation:**  
The copied list maintains the same structure and pointers as the original list.

#### Constraints:
- `0 <= n <= 1000`
- `-10^4 <= Node.val <= 10^4`
- `Node.random` is `null` or points to a node in the linked list.
"""

# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    """
    Thought Process:
    - The problem involves creating a deep copy of a linked list where each node has a `next` and a `random` pointer.
    - A straightforward approach involves using a hash map to map original nodes to their copies, but this requires extra space.
    - An optimized approach interleaves the original and copied nodes, allowing us to set the `random` pointers without extra space.

    Input:
        head: Node - The head of the original linked list.

    Output:
        Node - The head of the deep-copied linked list.
    """

    def copyRandomList(self, head: 'Node') -> 'Node':
        """
        Approach:
        - Interleave the original and copied nodes by inserting a copy of each node right after the original node.
        - Set the `random` pointers of the copied nodes by referencing the `random` pointers of the original nodes.
        - Separate the original and copied lists to restore the original list and extract the deep copy.

        T.C.: O(n) - We traverse the list three times.
        S.C.: O(1) - No additional space is used apart from the new nodes.
        """
        if not head:
            return None

        # Step 1: Create new nodes and interleave them with the original list
        current = head
        while current:
            cloned_node = Node(current.val, current.next, None)
            current.next = cloned_node
            current = cloned_node.next

        # Step 2: Set the random pointers for the cloned nodes
        current = head
        while current:
            if current.random:
                current.next.random = current.random.next
            current = current.next.next

        # Step 3: Separate the original and cloned lists
        original_current = head
        cloned_head = head.next
        while original_current:
            cloned_current = original_current.next
            original_current.next = cloned_current.next
            if cloned_current.next:
                cloned_current.next = cloned_current.next.next
            original_current = original_current.next

        return cloned_head

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Helper function to create a linked list from a list of [val, random_index] pairs
    def create_linked_list(nodes):
        if not nodes:
            return None
        node_list = [Node(val) for val, _ in nodes]
        for i, (_, random_index) in enumerate(nodes):
            if random_index is not None:
                node_list[i].random = node_list[random_index]
            if i < len(node_list) - 1:
                node_list[i].next = node_list[i + 1]
        return node_list[0]

    # Helper function to convert a linked list to a list of [val, random_index] pairs
    def linked_list_to_list(head):
        if not head:
            return []
        node_list = []
        node_to_index = {}
        current = head
        index = 0
        while current:
            node_to_index[current] = index
            current = current.next
            index += 1
        current = head
        while current:
            random_index = node_to_index.get(current.random, None)
            node_list.append([current.val, random_index])
            current = current.next
        return node_list

    # Test case 1
    nodes1 = [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
    head1 = create_linked_list(nodes1)
    copied_head1 = solution.copyRandomList(head1)
    print(linked_list_to_list(copied_head1))  # Output: [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]

    # Test case 2
    nodes2 = [[1, 1], [2, 1]]
    head2 = create_linked_list(nodes2)
    copied_head2 = solution.copyRandomList(head2)
    print(linked_list_to_list(copied_head2))  # Output: [[1, 1], [2, 1]]

    # Test case 3
    nodes3 = [[3, None], [3, 0], [3, None]]
    head3 = create_linked_list(nodes3)
    copied_head3 = solution.copyRandomList(head3)
    print(linked_list_to_list(copied_head3))  # Output: [[3, None], [3, 0], [3, None]]