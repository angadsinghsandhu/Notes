# File: Leetcode/Solutions/300_Longest_Increasing_Subsequence.py

"""
Problem Number: 300
Problem Name: Longest Increasing Subsequence
Difficulty: Medium
Tags: Dynamic Programming, Binary Search, Patience Sorting, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/longest-increasing-subsequence/description/>

DESCRIPTION

Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

Function signature example (python):

* `def lengthOfLIS(self, nums: List[int]) -> int:`

Approaches:

* DP O(n^2): dp[i] = max(dp[j]) + 1 for j < i and nums[j] < nums[i].
* Patience sorting / tails + binary search O(n log n): maintain tails array.
"""
