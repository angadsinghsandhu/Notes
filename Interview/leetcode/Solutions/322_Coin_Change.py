# File: Leetcode/Solutions/322_Coin_Change.py

"""
Problem Number: 322
Problem Name: Coin Change
Difficulty: Medium
Tags: Dynamic Programming, Unbounded Knapsack, BFS (alternate), Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/coin-change/description/>

DESCRIPTION

Given coin denominations and an amount, return the fewest number of coins needed to make up that amount. Return -1 if not possible.

Function signature example (python):

* `def coinChange(self, coins: List[int], amount: int) -> int:`

Approaches:

* DP 1D array dp[a] = min(dp[a], dp[a - coin] + 1).
* BFS on amounts (shortest path) as alternate approach.
* O(amount * len(coins)) time.
"""
