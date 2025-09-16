# File: Leetcode/Solutions/1 Array/215_Kth_Largest_Element_in_an_Array.py

"""
Problem Number: 215
Problem Name: Kth Largest Element in an Array
Difficulty: Medium
Tags: Sorting, Quickselect, Heap (Priority Queue), Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: https://leetcode.com/problems/kth-largest-element-in-an-array/

DESCRIPTION

Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?

---

#### Example 1:

Input:
nums = [3,2,1,5,6,4], k = 2

Output:
5

#### Example 2:

Input:
nums = [3,2,3,1,2,4,5,5,6], k = 4

Output:
4

#### Constraints:

* 1 <= k <= nums.length <= 10^5
* -10^4 <= nums[i] <= 10^4
"""

from typing import List
import heapq
import random

class Solution:
    """
    Thought Process:
    - Brute Force: Sort the array in descending order and pick the (k-1)th element.
    - Optimized:
    1) Min-heap of size k: maintain the k largest elements in O(n log k) time.
    2) Quickselect: average O(n) time, worst-case O(n^2), O(1) extra space.
    """


    def brute_force(self, nums: List[int], k: int) -> int:
        """
        Approach:
        - Sort nums in descending order and return the element at index k-1.

        T.C.: O(n log n)
        S.C.: O(n)
        """
        sorted_nums = sorted(nums, reverse=True)
        return sorted_nums[k - 1]

    def heap_solution(self, nums: List[int], k: int) -> int:
        """
        Approach:
        - Maintain a min-heap of size k. Push each num; if heap exceeds k, pop the smallest.
        
        T.C.: O(n log k)
        S.C.: O(k)
        """
        min_heap: List[int] = []
        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        return min_heap[0]

    def quickselect(self, nums: List[int], k: int) -> int:
        """
        Approach:
        - Use quickselect to find the (n-k)th smallest element (i.e., kth largest).

        T.C.: Average O(n), Worst O(n^2)
        S.C.: O(1) extra (in-place)
        """
        n = len(nums)
        target = n - k

        def partition(left: int, right: int, pivot_index: int) -> int:
            pivot_value = nums[pivot_index]
            # Move pivot to end
            nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
            store_index = left
            for i in range(left, right):
                if nums[i] < pivot_value:
                    nums[store_index], nums[i] = nums[i], nums[store_index]
                    store_index += 1
            # Move pivot to its final place
            nums[store_index], nums[right] = nums[right], nums[store_index]
            return store_index

        def select(left: int, right: int) -> int:
            if left == right:
                return nums[left]
            pivot_index = random.randint(left, right)
            pivot_index = partition(left, right, pivot_index)
            if pivot_index == target:
                return nums[pivot_index]
            elif pivot_index < target:
                return select(pivot_index + 1, right)
            else:
                return select(left, pivot_index - 1)

        # Work on a copy to preserve original nums
        nums_copy = nums[:]
        nums[:] = nums_copy
        return select(0, n - 1)

if __name__ == "__main__":
    solution = Solution()

    # Example 1
    nums1, k1 = [3, 2, 1, 5, 6, 4], 2
    print(solution.brute_force(nums1, k1))     # 5
    print(solution.heap_solution(nums1, k1))   # 5
    print(solution.quickselect(nums1, k1))     # 5

    # Example 2
    nums2, k2 = [3, 2, 3, 1, 2, 4, 5, 5, 6], 4
    print(solution.brute_force(nums2, k2))     # 4
    print(solution.heap_solution(nums2, k2))   # 4
    print(solution.quickselect(nums2, k2))     # 4

    # Additional tests
    print(solution.brute_force([1], 1))        # 1
    print(solution.heap_solution([2, 1], 1))   # 2
    print(solution.quickselect([2, 1], 2))     # 1
