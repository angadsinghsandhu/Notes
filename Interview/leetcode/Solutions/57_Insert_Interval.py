# File: Leetcode/Solutions/57_Insert_Interval.py

"""
Problem Number: 57
Problem Name: Insert Interval
Difficulty: Medium
Tags: Array, Sorting, Intervals, Two Pointers, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/insert-interval/description/>

DESCRIPTION

Given a list of non-overlapping intervals sorted by start time and a new interval, insert the new interval into the list and merge if necessary. Return the resulting merged intervals.
Approaches:

* Iterate intervals and add non-overlapping left intervals, merge overlapping ones, then add remaining intervals.
* O(n) time, O(n) output space.
"""
