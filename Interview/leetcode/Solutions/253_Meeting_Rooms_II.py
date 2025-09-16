# TODO: revisit

# File: Leetcode/Solutions/253_Meeting_Rooms_II.py

"""
Problem Number: 253
Problem Name: Meeting Rooms II
Difficulty: Medium
Tags: Greedy, Array, Two Pointers, Prefix Sum, Sorting, Heap (Priority Queue), Neetcode 150
Company (Frequency): Amazon, Microsoft, Google, Apple, Adobe (High)
Leetcode Link: https://leetcode.com/problems/meeting-rooms-ii/
Lintcode Link: https://www.lintcode.com/problem/919/

DESCRIPTION

Given an array of meeting time intervals consisting of start and end times [[s1,e1],[s2,e2],...] (si < ei), find the minimum number of conference rooms required.

Example 1:
Input: intervals = [[0, 30],[5, 10],[15, 20]]
Output: 2

Example 2:
Input: intervals = [[7,10],[2,4]]
Output: 1

Constraints:
- 1 <= intervals.length <= 10^4
- 0 <= start_i < end_i <= 10^6
"""

from typing import List
from itertools import accumulate

class Solution:
    """
    Thought Process:
    - Track room occupancy changes using a timeline approach (sweep line algorithm).
    - For each meeting start, increment a counter; for each end, decrement.
    - Calculate the maximum concurrent meetings using a prefix sum.

    Approach:
    - Use a delta array to mark start and end times with +1 and -1.
    - Compute the prefix sum of the delta array to find peak occupancy.

    Time Complexity: O(N + T), where N is the number of intervals and T is the maximum time (10^6).
    Space Complexity: O(T), optimized to fixed size for given constraints.
    """

    def brute_force_solution(self, intervals: List[List[int]]) -> int:
        # Initialize delta array to cover all possible times up to 1e6
        max_time = 10**6
        delta = [0] * (max_time + 2)  # +2 to safely handle end times at max_time

        for start, end in intervals:
            delta[start] += 1
            delta[end] -= 1

        # Compute prefix sum and find the maximum value
        return max(accumulate(delta))
    
    def optimized_solution(self, intervals: List[List[int]]) -> int:
        # using 2 pointers in 2 arrays to decide the max meetings happening simultanously
        start, end = [], []

        for start_time, end_time in intervals:
            start.append(start_time)
            end.append(end_time)

        start.sort()
        end.sort()

        res, cnt = 0, 0
        s, e = 0, 0

        while s < len(intervals):
            if start[s] < end[e]:
                s += 1
                cnt += 1
            else:
                e += 1
                cnt -= 1
            res = max(res, cnt)

        return res


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    print(solution.brute_force_solution(intervals1))  # Expected Output: 2
    print(solution.optimized_solution(intervals1))  # Expected Output: 2

    # Test case 2
    intervals2 = [[7, 10], [2, 4]]
    print(solution.brute_force_solution(intervals2))  # Expected Output: 1
    print(solution.optimized_solution(intervals2))  # Expected Output: 1

    # Test case 3 (Edge case: back-to-back meetings)
    intervals3 = [[1, 3], [3, 5]]
    print(solution.brute_force_solution(intervals3))  # Expected Output: 1
    print(solution.optimized_solution(intervals3))  # Expected Output: 1