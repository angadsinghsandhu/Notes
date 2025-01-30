# File: Leetcode/Solutions/Amazon/2_Add_Two_Numbers.py

"""
Problem Number: 2
Problem Name: Add Two Numbers
Difficulty: Medium
Tags: Linked List, Math, Recursion
Company (Frequency): Amazon (89)
Leetcode Link: <https://leetcode.com/problems/add-two-numbers/description/>

DESCRIPTION

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

---

#### Example 1:
**Input:**
```plaintext
l1 = [2, 4, 3], l2 = [5, 6, 4]
```

**Output:**
```plaintext
[7, 0, 8]
```

**Explanation:**  
342 + 465 = 807.

#### Example 2:
**Input:**
```plaintext
l1 = [0], l2 = [0]
```

**Output:**
```plaintext
[0]
```

#### Example 3:
**Input:**
```plaintext
l1 = [9, 9, 9, 9, 9, 9, 9], l2 = [9, 9, 9, 9]
```

**Output:**
```plaintext
[8, 9, 9, 9, 0, 0, 0, 1]
```

#### Constraints:
- The number of nodes in each linked list is in the range [1, 100].
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros.
"""

from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """
    Thought Process:
    - The problem involves adding two numbers represented as linked lists in reverse order.
    - We need to handle the addition digit by digit, keeping track of the carry.
    - The result should also be a linked list in reverse order.

    Input:
        l1: Optional[ListNode] - The first linked list representing a number.
        l2: Optional[ListNode] - The second linked list representing a number.

    Output:
        Optional[ListNode] - The linked list representing the sum of the two numbers.
    """

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:
        - Initialize a dummy node to simplify the handling of the result linked list.
        - Use a carry variable to keep track of the overflow from the addition of digits.
        - Iterate through both linked lists, adding corresponding digits along with the carry.
        - If one list is longer than the other, continue adding the remaining digits.
        - If there is a carry left after the last addition, add it as a new node.

        T.C.: O(max(n, m)) where n and m are the lengths of l1 and l2.
        S.C.: O(max(n, m)) for the result linked list.
        """
        # initialize vars
        dummy = ListNode()
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            # get current values in lists
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # arithmatic
            total = val1 + val2 + carry
            carry = total // 10

            # add to next node
            current.next = ListNode(total % 10)
            current = current.next

            # continue to the next nodes
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next

# Helper function to convert a list to a linked list
def list_to_linked_list(lst):
    dummy = ListNode()
    current = dummy
    for num in lst:
        current.next = ListNode(num)
        current = current.next
    return dummy.next

# Helper function to convert a linked list to a list
def linked_list_to_list(node):
    lst = []
    while node:
        lst.append(node.val)
        node = node.next
    return lst

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    l1 = list_to_linked_list([2, 4, 3])
    l2 = list_to_linked_list([5, 6, 4])
    result = solution.addTwoNumbers(l1, l2)
    print(linked_list_to_list(result))  # Output: [7, 0, 8]

    l1 = list_to_linked_list([0])
    l2 = list_to_linked_list([0])
    result = solution.addTwoNumbers(l1, l2)
    print(linked_list_to_list(result))  # Output: [0]

    l1 = list_to_linked_list([9, 9, 9, 9, 9, 9, 9])
    l2 = list_to_linked_list([9, 9, 9, 9])
    result = solution.addTwoNumbers(l1, l2)
    print(linked_list_to_list(result))  # Output: [8, 9, 9, 9, 0, 0, 0, 1]