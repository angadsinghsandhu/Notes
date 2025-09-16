# File: Leetcode/Solutions/213_House_Robber_II.py

"""
Problem Number: 213
Problem Name: House Robber II
Difficulty: Medium
Tags: Dynamic Programming, Array, Circular Array, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/house-robber-ii/description/>

DESCRIPTION

Houses are arranged in a circle (first and last adjacent). Return maximum stealable amount without robbing adjacent houses.

Function signature example (python):

* `def rob(self, nums: List[int]) -> int:`

Approaches:

* Reduce to two linear House Robber problems: exclude last or exclude first (max of the two).
* Handle small n edge cases.
"""
