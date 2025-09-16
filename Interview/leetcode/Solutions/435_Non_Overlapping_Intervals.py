# File: Leetcode/Solutions/435_Non_Overlapping_Intervals.py

"""
Problem Number: 435
Problem Name: Non Overlapping Intervals
Difficulty: Medium
Tags: Greedy, Intervals, Sorting, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/non-overlapping-intervals/description/>

DESCRIPTION

Given intervals, remove the minimum number so that the remaining intervals are non-overlapping. Return the minimum removals.
Approaches:

* Greedy by sorting on end time and selecting maximum non-overlapping intervals; answer = total - selected.
* O(n log n) time.
"""
