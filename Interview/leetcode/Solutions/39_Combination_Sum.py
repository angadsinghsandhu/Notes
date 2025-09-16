# File: Leetcode/Solutions/39_Combination_Sum.py

"""
Problem Number: 39
Problem Name: Combination Sum
Difficulty: Medium
Tags: Backtracking, Recursion, Array, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/combination-sum/description/>

DESCRIPTION

Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. The same number may be chosen from `candidates` an unlimited number of times. Combinations may be returned in any order.

Function signature example (python):

* `def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:`

Approaches:

* DFS/backtracking with pruning (sort candidates, early stop)
* Use recursion building combination and subtracting remaining target
"""
