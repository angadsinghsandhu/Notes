# File: Leetcode/Solutions/518_Coin_Change_II.py

"""
Problem Number: 518
Problem Name: Coin Change II
Difficulty: Medium
Tags: Dynamic Programming, Knapsack, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/coin-change-2/description/>

DESCRIPTION

Given coin denominations and amount, count number of combinations to make amount (order doesn't matter).
Approaches:

* 1D DP (unbounded knapsack): for coin in coins: for amt from coin..amount: dp[amt] += dp[amt - coin].
"""
