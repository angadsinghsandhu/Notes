# File: Leetcode/Solutions/198_House_Robber.py

"""
Problem Number: 198
Problem Name: House Robber
Difficulty: Medium
Tags: Dynamic Programming, Array, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/house-robber/description/>

DESCRIPTION

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount you can rob without robbing adjacent houses.

Function signature example (python):

* `def rob(self, nums: List[int]) -> int:`

Approaches:

* DP: include/exclude recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i]).
* O(n) time, O(1) space with two variables.
"""
