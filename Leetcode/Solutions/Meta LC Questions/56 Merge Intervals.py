# MERGE INTERVALS

# Problem number: 56
# Difficulty: Medium
# Tags: Array, Sorting, Intervals, Greedy
# Link: https://leetcode.com/problems/merge-intervals/

from typing import List

class Solution:
    """
    This problem requires merging overlapping intervals from a list.
    The most straightforward approach is to sort the intervals by their starting times and then merge them one by one.

    We will implement two methods:
    1. Sorting-based Greedy Approach
    2. Optimized Greedy Approach with early termination (if applicable)
    
    Both methods have the same input and output formats to allow comparison.
    """

    def merge_sorting_greedy(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Sorting-based greedy approach to merge intervals.
        
        T.C. : O(n log n) due to sorting the intervals where n is the number of intervals.
        S.C. : O(n) as we are storing the result list.
        """
        if not intervals:
            return []

        # Sort the intervals based on the start time
        intervals.sort(key=lambda x: x[0])
        merged = []

        for interval in intervals:
            # If merged list is empty or current interval does not overlap, simply add it
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                # There is an overlap, merge the intervals
                merged[-1][1] = max(merged[-1][1], interval[1])

        return merged

    def merge_optimized(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Optimized approach (same as sorting but can exit early based on intervals properties).
        
        T.C. : O(n log n) as sorting is needed, but can terminate early based on conditions.
        S.C. : O(n) to store the result.
        """
        if not intervals:
            return []

        # Sort the intervals based on start time
        intervals.sort(key=lambda x: x[0])
        result = []
        prev_start, prev_end = intervals[0]

        for i in range(1, len(intervals)):
            curr_start, curr_end = intervals[i]
            if curr_start > prev_end:
                # No overlap, push the previous interval
                result.append([prev_start, prev_end])
                prev_start, prev_end = curr_start, curr_end
            else:
                # Merge intervals
                prev_end = max(prev_end, curr_end)

        # Add the last merged interval
        result.append([prev_start, prev_end])

        return result

# Best Method: The sorting-based greedy approach is optimal and widely used in practice. 

# Example inputs for testing
intervals1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
intervals2 = [[1, 4], [4, 5]]

# Testing Sorting Greedy Method
print(Solution().merge_sorting_greedy(intervals1))  # Output: [[1,6],[8,10],[15,18]]
print(Solution().merge_sorting_greedy(intervals2))  # Output: [[1,5]]

# Testing Optimized Greedy Method
print(Solution().merge_optimized(intervals1))  # Output: [[1,6],[8,10],[15,18]]
print(Solution().merge_optimized(intervals2))  # Output: [[1,5]]
