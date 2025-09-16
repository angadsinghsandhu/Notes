# File: Leetcode/Solutions/703_Kth_Largest_Element_in_a_Stream.py

"""
Problem Number: 703
Problem Name: Kth Largest Element in a Stream
Difficulty: Easy
Tags: Heap (Priority Queue), Design, Data Stream, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/kth-largest-element-in-a-stream/description/>

DESCRIPTION

Design a class to find the k-th largest element in a stream. Note that it is the k-th largest element in the sorted order, not the k-th distinct element.

* `KthLargest(int k, int[] nums)` Initializes the object with the integer k and the stream of integers nums.
* `int add(int val)` Appends the integer val to the stream and returns the element representing the k-th largest element in the stream.

Function signature example (python):

* `class KthLargest:`

  * `def __init__(self, k: int, nums: List[int]):`
  * `def add(self, val: int) -> int:`

Approaches:

* Maintain a min-heap of size k (top of heap = k-th largest).
* On add: push val and pop if heap size > k; return heap[0].
"""
