# File: Leetcode/Solutions/416_Partition_Equal_Subset_Sum.py

"""
Problem Number: 416
Problem Name: Partition Equal Subset Sum
Difficulty: Medium
Tags: Dynamic Programming, Subset Sum, Knapsack, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/partition-equal-subset-sum/description/>

DESCRIPTION

Given a non-empty array of positive integers, determine if it can be partitioned into two subsets with equal sum.

Function signature example (python):

* `def canPartition(self, nums: List[int]) -> bool:`

Approaches:

* Reduce to subset sum: target = total // 2. Use DP boolean 1D array dp[t] indicating achievable sums.
* O(n * target) time, O(target) space.
"""
