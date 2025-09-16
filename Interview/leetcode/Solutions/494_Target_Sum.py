# File: Leetcode/Solutions/494_Target_Sum.py

"""
Problem Number: 494
Problem Name: Target Sum
Difficulty: Medium
Tags: Dynamic Programming, Backtracking, Subset Sum, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/target-sum/description/>

DESCRIPTION

Given nums and target, assign + or - to each to reach target; return number of ways.
Approaches:

* Reduce to subset sum: (sum + target) must be even; count subsets with sum = (sum + target)/2 using DP.
"""
