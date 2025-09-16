# File: Leetcode/Solutions/1483_Minimum_Interval_to_Include_Each_Query.py

"""
Problem Number: 1483
Problem Name: Minimum Interval to Include Each Query
Difficulty: Hard
Tags: Heap (Priority Queue), Sorting, Intervals, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/minimum-interval-to-include-each-query/description/>

DESCRIPTION

Given intervals and queries, for each query return the length of the smallest interval that contains it, or -1 if none.
Approaches:

* Sort queries and intervals; use min-heap of candidate intervals (by length) while sweeping queries.
* O((n + q) log n) time.
"""
