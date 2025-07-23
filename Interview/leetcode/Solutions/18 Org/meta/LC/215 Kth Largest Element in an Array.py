# KTH LARGEST ELEMENT IN AN ARRAY

# Problem number: 215
# Difficulty: Medium
# Tags: Array, Heap (Priority Queue), Quickselect
# Link: https://leetcode.com/problems/kth-largest-element-in-an-array/

from typing import List
import heapq

class Solution:
    """
    This problem requires finding the kth largest element in an unsorted array.
    We will provide multiple approaches to solve this problem, including a 
    heap-based approach and a quickselect approach.
    
    The input is an array of integers, and the output is the kth largest element.
    
    We will implement two methods:
    1. Min-Heap Approach
    2. Quickselect Approach
    
    Both methods have different time and space complexities.
    """

    def findKthLargest_heap(self, nums: List[int], k: int) -> int:
        """
        Min-Heap approach using a heap of size k.
        
        T.C. : O(n log k) where n is the number of elements in the array
        S.C. : O(k) for the heap storage
        """
        # Use a min-heap with size k
        min_heap = nums[:k]
        heapq.heapify(min_heap)  # Create a heap from the first k elements

        for num in nums[k:]:
            if num > min_heap[0]:
                heapq.heappushpop(min_heap, num)  # Maintain heap of size k

        return min_heap[0]

    def findKthLargest_quickselect(self, nums: List[int], k: int) -> int:
        """
        Quickselect approach to find the kth largest element.
        Quickselect is a variation of QuickSort that selects the kth element in O(n) average time.
        
        T.C. : O(n) average, O(n^2) worst case
        S.C. : O(1), as we sort the array in place
        """
        def partition(left: int, right: int, pivot_index: int) -> int:
            pivot_value = nums[pivot_index]
            # Move pivot to the end
            nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
            store_index = left

            # Move all elements smaller than the pivot to the left
            for i in range(left, right):
                if nums[i] < pivot_value:  # We're looking for the kth largest
                    nums[store_index], nums[i] = nums[i], nums[store_index]
                    store_index += 1

            # Move pivot to its final place
            nums[right], nums[store_index] = nums[store_index], nums[right]
            return store_index

        def quickselect(left: int, right: int, k_smallest: int) -> int:
            if left == right:
                return nums[left]

            # Select a random pivot
            pivot_index = partition(left, right, left + (right - left) // 2)

            # The pivot is in its final sorted position
            if k_smallest == pivot_index:
                return nums[k_smallest]
            elif k_smallest < pivot_index:
                return quickselect(left, pivot_index - 1, k_smallest)
            else:
                return quickselect(pivot_index + 1, right, k_smallest)

        # kth largest is the (len(nums) - k)th smallest element
        return quickselect(0, len(nums) - 1, len(nums) - k)

# Best Method: Quickselect is the most optimal approach for average case, with O(n) time complexity.
