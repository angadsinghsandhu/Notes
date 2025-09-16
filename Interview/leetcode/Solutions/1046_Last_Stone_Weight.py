# File: Leetcode/Solutions/1046_Last_Stone_Weight.py

"""
Problem Number: 1046
Problem Name: Last Stone Weight
Difficulty: Easy
Tags: Heap (Priority Queue), Greedy, Simulation, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/last-stone-weight/description/>

DESCRIPTION

We have stones with positive integer weights. Each turn, choose the two heaviest stones and smash them:

* If they are equal, both stones are destroyed.
* If not equal, the smaller is destroyed and the larger becomes (larger - smaller).
  Return the weight of the last remaining stone. If no stones remain, return 0.

Function signature example (python):

* `def lastStoneWeight(self, stones: List[int]) -> int:`

Approaches:

* Use a max-heap (or min-heap of negatives). Repeatedly pop two largest, push difference if non-zero.
* O(n log n) overall.
"""