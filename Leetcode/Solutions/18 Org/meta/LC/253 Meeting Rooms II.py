# MEETING ROOMS II

# Problem number: 253
# Difficulty: Medium
# Tags: Heap, Greedy, Sorting, Interval Scheduling
# Link: https://leetcode.com/problems/meeting-rooms-ii/

from typing import List
import heapq

class Solution:
    """
    This problem requires finding the minimum number of conference rooms required to schedule all meetings.
    We need to determine how many rooms are needed at the peak point when the most meetings are taking place simultaneously.

    The solution can be approached by sorting the intervals based on start times and using a min-heap (priority queue) 
    to keep track of the end times of the meetings.

    We will implement:
    1. Heap-based Greedy Approach

    This method efficiently handles the meeting scheduling problem and ensures we only allocate rooms as needed.
    """

    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Heap-based Greedy Approach to find the minimum number of meeting rooms.
        
        T.C. : O(n log n), where n is the number of intervals. Sorting takes O(n log n) and heap operations take O(log n).
        S.C. : O(n), as we use a heap to store end times of meetings.
        """
        if not intervals:
            return 0
        
        # Sort intervals based on start times
        intervals.sort(key=lambda x: x[0])

        # Min-heap to track the end times of meetings
        heap = []
        
        # Add the first meeting's end time to the heap
        heapq.heappush(heap, intervals[0][1])

        # Iterate over the remaining intervals
        for i in range(1, len(intervals)):
            # If the room is free (earliest meeting ends before or when the next meeting starts)
            if heap[0] <= intervals[i][0]:
                heapq.heappop(heap)  # Remove the room (free it up)
            
            # Allocate a new room (push the current meeting's end time to the heap)
            heapq.heappush(heap, intervals[i][1])
        
        # The size of the heap tells us the minimum number of rooms required
        return len(heap)

# Best Method: The heap-based greedy approach is optimal, as it allows us to minimize room allocation while keeping track of meeting end times.

# Sample Inputs for Testing
intervals_1 = [[0, 30], [5, 10], [15, 20]]
intervals_2 = [[7, 10], [2, 4]]

# Testing the solution
print(Solution().minMeetingRooms(intervals_1))  # Output should be 2
print(Solution().minMeetingRooms(intervals_2))  # Output should be 1
