# File: Leetcode/Solutions/90_Subsets_II.py

"""
Problem Number: 90
Problem Name: Subsets II
Difficulty: Medium
Tags: Backtracking, Sorting, Recursion, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/subsets-ii/description/>

DESCRIPTION

Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set) without duplicate subsets. Order of subsets does not matter.

Function signature example (python):

* `def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:`

Approaches:

* Sort nums then backtrack while skipping duplicates at the same recursion level
* Iterative expansion with duplicate checking
"""