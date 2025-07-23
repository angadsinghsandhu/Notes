# File: Leetcode/Solutions/Amazon/56_Merge_Intervals.py

"""
Problem Number: 56
Problem Name: Merge Intervals
Difficulty: Medium
Tags: Array, Sorting
Company (Frequency): Amazon (87)
Leetcode Link: https://leetcode.com/problems/merge-intervals/description/

DESCRIPTION

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the intervals in the input.

---

#### Example 1:
**Input:**
```plaintext
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
```

**Output:**
```plaintext
[[1, 6], [8, 10], [15, 18]]
```

**Explanation:**  
Intervals `[1, 3]` and `[2, 6]` overlap, so they are merged into `[1, 6]`.

#### Constraints:
- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves merging overlapping intervals into a single interval.
    - A brute-force approach involves checking every pair of intervals for overlap, but this is inefficient.
    - An optimized approach sorts the intervals by their start time and iterates through them, merging overlapping intervals on the fly.

    Input:
        intervals: List[List[int]] - A list of intervals, where each interval is represented as [start, end].

    Output:
        List[List[int]] - A list of merged intervals.
    """

    def brute_force_solution(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Approach:
        - Check every pair of intervals for overlap.
        - If two intervals overlap, merge them and repeat the process until no more overlaps are found.

        T.C.: O(n^2) - Checking every pair of intervals.
        S.C.: O(n) - Storing the merged intervals.
        """
        if not intervals:
            return []
        
        def _overlap(self, interval1: List[int], interval2: List[int]) -> bool:
            """
            Helper function to check if two intervals overlap.
            """
            return interval1[1] >= interval2[0] and interval2[1] >= interval1[0]
        
        def _merge(self, interval1: List[int], interval2: List[int]) -> List[int]:
            """
            Helper function to merge two overlapping intervals.
            """
            return [min(interval1[0], interval2[0]), max(interval1[1], interval2[1])]

        merged = []
        for interval in intervals:
            new_interval = interval
            i = 0
            while i < len(merged):
                if _overlap(merged[i], new_interval):
                    new_interval = _merge(merged[i], new_interval)
                    merged.pop(i)
                else:
                    i += 1
            merged.append(new_interval)
        return merged

    def optimized_solution(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Approach:
        - Sort the intervals by their start time.
        - Iterate through the sorted intervals and merge overlapping intervals on the fly.

        T.C.: O(n log n) - Sorting takes O(n log n), and merging takes O(n).
        S.C.: O(n) - Storing the merged intervals.
        """
        if not intervals:
            return []
        
        # Sort intervals based on the start time
        intervals.sort(key=lambda x: x[0])
        
        merged = [intervals[0]]
        
        for current_start, current_end in intervals[1:]:
            last_start, last_end = merged[-1]
            
            # Check if the current interval overlaps with the last merged interval
            if current_start <= last_end:
                # Merge the intervals by updating the end of the last interval
                merged[-1][1] = max(last_end, current_end)
            else:
                # No overlap, add the current interval to merged
                merged.append([current_start, current_end])
        
        return merged

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    intervals1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(solution.brute_force_solution([x[:] for x in intervals1]))  # Output: [[1, 6], [8, 10], [15, 18]]
    print(solution.optimized_solution([x[:] for x in intervals1]))    # Output: [[1, 6], [8, 10], [15, 18]]

    # Test case 2
    intervals2 = [[1, 4], [4, 5]]
    print(solution.brute_force_solution([x[:] for x in intervals2]))  # Output: [[1, 5]]
    print(solution.optimized_solution([x[:] for x in intervals2]))    # Output: [[1, 5]]