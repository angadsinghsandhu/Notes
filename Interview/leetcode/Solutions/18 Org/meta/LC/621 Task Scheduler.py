# TASK SCHEDULER

# Problem number: 621
# Difficulty: Medium
# Tags: Array, Hash Table, Greedy, Sorting, Heap (Priority Queue)
# Link: https://leetcode.com/problems/task-scheduler/

from typing import List
from collections import Counter

class Solution:
    """
    This problem requires scheduling tasks with a cooldown period. The task can be repeated 
    only after n intervals, which means we need to minimize the CPU idle time. The most optimal 
    approach involves counting task frequencies and calculating the least number of intervals 
    required, considering the most frequent tasks.

    We will implement a greedy approach to calculate the minimum time required to schedule tasks.
    """

    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Greedy approach to minimize CPU idle time.
        
        T.C. : O(t) where t is the number of tasks (len(tasks))
        S.C. : O(1) constant space for tracking the task counts (limited to 26 letters)
        """
        task_counts = Counter(tasks)
        max_freq = max(task_counts.values())
        
        # Calculate the number of idle slots based on the most frequent task
        max_count = sum(1 for task, freq in task_counts.items() if freq == max_freq)
        
        # The formula for the result is based on the maximum frequency task:
        # We use: (max_freq - 1) * (n + 1) + max_count
        idle_slots = (max_freq - 1) * (n + 1) + max_count
        
        # The result is the max of total tasks or the calculated idle slots.
        return max(idle_slots, len(tasks))

# Best Method: This greedy approach is optimal, as it ensures we minimize idle times by scheduling 
# the most frequent tasks first.

# Example Tests
tasks1 = ["A","A","A","B","B","B"]
n1 = 2
print(Solution().leastInterval(tasks1, n1))  # Output: 8

tasks2 = ["A","C","A","B","D","B"]
n2 = 1
print(Solution().leastInterval(tasks2, n2))  # Output: 6

tasks3 = ["A","A","A","B","B","B"]
n3 = 3
print(Solution().leastInterval(tasks3, n3))  # Output: 10
