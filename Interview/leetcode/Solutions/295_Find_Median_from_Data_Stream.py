# File: Leetcode/Solutions/295_Find_Median_from_Data_Stream.py

"""
Problem Number: 295
Problem Name: Find Median from Data Stream
Difficulty: Hard
Tags: Heap (Priority Queue), Data Stream, Design, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/find-median-from-data-stream/description/>

DESCRIPTION

Design a data structure that supports adding numbers from a data stream and finding the median of all elements:

* `addNum(int num)` adds a number to the data structure.
* `findMedian()` returns the median of all elements so far.

Function signature example (python):

* `class MedianFinder:`

  * `def addNum(self, num: int) -> None:`
  * `def findMedian(self) -> float:`

Approaches:

* Maintain two heaps: a max-heap for the lower half and a min-heap for the upper half. Balance sizes to compute median in O(1).
* Alternatively maintain a balanced BST (multiset) but heaps are preferred for simplicity and speed.
"""
