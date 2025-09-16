# File: Leetcode/Solutions/621_Task_Scheduler.py

"""
Problem Number: 621
Problem Name: Task Scheduler
Difficulty: Medium
Tags: Greedy, Math, Simulation, Hash Table, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/task-scheduler/description/>

DESCRIPTION

Given a list of tasks represented by uppercase letters and a non-negative cooldown n, schedule tasks so that the same task has at least n intervals between two executions. Return the least number of intervals needed to finish all tasks.

Function signature example (python):

* `def leastInterval(self, tasks: List[str], n: int) -> int:`

Approaches:

* Count frequencies, use greedy formula: `(maxFreq - 1) * (n + 1) + countMaxFreq`.
* Alternatively simulate with a max-heap / cooldown queue (slower but intuitive).
"""
