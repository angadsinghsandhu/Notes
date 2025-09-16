# File: Leetcode/Solutions/763_Partition_Labels.py

"""
Problem Number: 763
Problem Name: Partition Labels
Difficulty: Medium
Tags: Greedy, Two Pointers, String, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/partition-labels/description/>

DESCRIPTION

Partition string into as many parts so that each letter appears in at most one part; return sizes of parts.
Approaches:

* Record last index of each char; scan and cut when current index reaches max last seen for current partition.
* O(n) time.
"""
