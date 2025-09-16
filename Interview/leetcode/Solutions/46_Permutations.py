# File: Leetcode/Solutions/46_Permutations.py

"""
Problem Number: 46
Problem Name: Permutations
Difficulty: Medium
Tags: Backtracking, Recursion, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: [https://leetcode.com/problems/permutations/description/](https://leetcode.com/problems/permutations/description/)

DESCRIPTION

Given a list of distinct integers `nums`, return all possible permutations. You can return the permutations in any order.

Function signature example (python):

* `def permute(self, nums: List[int]) -> List[List[int]]:`

Approaches:

* Backtracking with in-place swapping
* Backtracking building current permutation + used-set boolean array
"""
