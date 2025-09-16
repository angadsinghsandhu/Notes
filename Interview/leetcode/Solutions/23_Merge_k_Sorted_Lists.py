# File: Leetcode/Solutions/23_Merge_k_Sorted_Lists.py

"""
Problem Number: 23
Problem Name: Merge k Sorted Lists
Difficulty: Hard
Tags: Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort, Neetcode 150
Company (Frequency): Amazon (89), Apple, Facebook, Google, Microsoft
Leetcode Link: <https://leetcode.com/problems/merge-k-sorted-lists/description/>

DESCRIPTION

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

---

#### Example 1:
**Input:**
```plaintext
lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
```

**Output:**
```plaintext
[1, 1, 2, 3, 4, 4, 5, 6]
```

**Explanation:**  
The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
Merging them into one sorted list:
1->1->2->3->4->4->5->6

#### Example 2:
**Input:**
```plaintext
lists = []
```

**Output:**
```plaintext
[]
```

#### Example 3:
**Input:**
```plaintext
lists = [[]]
```

**Output:**
```plaintext
[]
```

#### Constraints:
- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` will not exceed `10^4`.
"""

from typing import List, Optional
import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        # Override the less-than operator for heap comparison
        return self.val < other.val

class Solution:
    """
    Thought Process:
    - The problem involves merging `k` sorted linked lists into one sorted linked list.
    - A brute force solution would involve collecting all values, sorting them, and creating a new linked list.
    - Optimized solutions include using a min-heap (priority queue) or a divide-and-conquer approach (merge sort).

    Input:
        lists: List[Optional[ListNode]] - An array of `k` sorted linked lists.

    Output:
        Optional[ListNode] - The head of the merged sorted linked list.
    """

    def brute_force_solution(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Approach:
        - Collect all values from the linked lists into a single list.
        - Sort the list and create a new linked list from the sorted values.

        T.C.: O(N log N), where N is the total number of nodes.
        S.C.: O(N) for storing all values.
        """
        nodes = []
        for lst in lists:
            while lst:
                nodes.append(lst.val)
                lst = lst.next

        nodes.sort()
        dummy = ListNode()
        current = dummy

        for val in nodes:
            current.next = ListNode(val)
            current = current.next

        return dummy.next

    def optimized_solution_heap(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Approach:
        - Use a min-heap to efficiently merge the linked lists.
        - Push the head of each linked list into the heap.
        - Continuously pop the smallest element from the heap and add it to the result linked list.
        - Push the next node of the popped element into the heap if it exists.

        T.C.: O(N log k), where N is the total number of nodes and k is the number of linked lists.
        S.C.: O(k) for the heap.
        """
        heap = []
        dummy = ListNode()
        current = dummy

        # Initialize the heap with the head of each linked list
        for lst in lists:
            if lst:
                heapq.heappush(heap, (lst.val, lst))

        while heap:
            val, node = heapq.heappop(heap)
            current.next = ListNode(val)
            current = current.next

            if node.next:
                heapq.heappush(heap, (node.next.val, node.next))

        return dummy.next

    def optimized_solution_divide_conquer(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Approach:
        - Use a divide-and-conquer strategy to merge the linked lists in pairs.
        - Recursively merge two linked lists at a time until all lists are merged into one.

        T.C.: O(N log k), where N is the total number of nodes and k is the number of linked lists.
        S.C.: O(1) (ignoring recursion stack space).
        """
        def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
            dummy = ListNode()
            current = dummy

            while l1 and l2:
                if l1.val < l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next

            if l1:
                current.next = l1
            if l2:
                current.next = l2

            return dummy.next

        if not lists:
            return None

        interval = 1
        n = len(lists)

        while interval < n:
            for i in range(0, n - interval, interval * 2):
                lists[i] = merge_two_lists(lists[i], lists[i + interval])
            interval *= 2

        return lists[0]

# Helper function to convert a list to a linked list
def list_to_linked_list(lst):
    dummy = ListNode()
    current = dummy
    for val in lst:
        current.next = ListNode(val)
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
    lists1 = [
        list_to_linked_list([1, 4, 5]),
        list_to_linked_list([1, 3, 4]),
        list_to_linked_list([2, 6])
    ]
    result1 = solution.optimized_solution_heap(lists1)
    print(linked_list_to_list(result1))  # Output: [1, 1, 2, 3, 4, 4, 5, 6]

    lists2 = []
    result2 = solution.optimized_solution_heap(lists2)
    print(linked_list_to_list(result2))  # Output: []

    lists3 = [list_to_linked_list([])]
    result3 = solution.optimized_solution_heap(lists3)
    print(linked_list_to_list(result3))  # Output: []