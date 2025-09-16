# File: Leetcode/Solutions/62_Unique_Paths.py

"""
Problem Number: 62
Problem Name: Unique Paths
Difficulty: Medium
Tags: Dynamic Programming, Combinatorics, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/unique-paths/description/>

DESCRIPTION

Count number of unique paths from top-left to bottom-right in m x n grid moving only right or down.
Approaches:

* DP dp[i][j] = dp[i-1][j] + dp[i][j-1]; or combinatorics nCr; O(mn) or O(1) with math.
"""
