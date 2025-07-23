# REORDER LIST

# Problem number: 143
# Difficulty: Medium
# Tags: Linked List, Two Pointers, Recursion
# Link: https://leetcode.com/problems/reorder-list/

from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """
    This problem requires rearranging the linked list in a specific order without modifying 
    the node values. The solution involves three main steps:
    
    1. Find the middle of the linked list.
    2. Reverse the second half of the list.
    3. Merge the two halves by alternating nodes.
    
    This ensures the list is reordered to the desired format.
    """

    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Reorders the linked list in-place.
        
        T.C. : O(n) where n is the number of nodes in the list
        S.C. : O(1) since we only modify the pointers and do not use extra space
        """

        if not head:
            return

        # Step 1: Find the middle of the linked list using the slow and fast pointers
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse the second half of the list
        prev, curr = None, slow
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        # Step 3: Merge the two halves
        first, second = head, prev
        while second.next:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next = temp1
            first, second = temp1, temp2

# Best Method: This method uses the optimal approach with O(n) time complexity and O(1) space complexity.

# Sample Inputs for Testing
# Input: head = [1,2,3,4]
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)

# Test the method
Solution().reorderList(head)

# Output should be [1,4,2,3] when printed or traversed
