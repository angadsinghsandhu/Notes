# File: Leetcode/Solutions/746_Min_Cost_Climbing_Stairs.py

"""
Problem Number: 746
Problem Name: Min Cost Climbing Stairs
Difficulty: Easy
Tags: Dynamic Programming, Array, Greedy (DP viewpoint), Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/min-cost-climbing-stairs/description/>

DESCRIPTION

Given an array `cost` where `cost[i]` is the cost of step `i`, you can start at step 0 or 1. Each move you can climb one or two steps. Return the minimum cost to reach the top (beyond last index).

Function signature example (python):

* `def minCostClimbingStairs(self, cost: List[int]) -> int:`

Approaches:

* DP with two variables: dp[i] = cost[i] + min(dp[i-1], dp[i-2]); answer = min(dp[n-1], dp[n-2]).
* O(n) time, O(1) space.
"""
