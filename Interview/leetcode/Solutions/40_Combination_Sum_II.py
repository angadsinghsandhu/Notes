# File: Leetcode/Solutions/40_Combination_Sum_II.py

"""
Problem Number: 40
Problem Name: Combination Sum II
Difficulty: Medium
Tags: Backtracking, Sorting, Recursion, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: [https://leetcode.com/problems/combination-sum-ii/description/](https://leetcode.com/problems/combination-sum-ii/description/)

DESCRIPTION

Given a collection of candidate numbers (candidates) and a target number (target), return a list of unique combinations where each candidate may only be used once. The input may contain duplicates; the output must not include duplicate combinations.

Function signature example (python):

* `def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:`

Approaches:

* Sort candidates, then backtrack while skipping duplicates at the same recursion level
* Use visited or index-based deduplication
"""
