# File: Leetcode/Solutions/115_Distinct_Subsequences.py

"""
Problem Number: 115
Problem Name: Distinct Subsequences
Difficulty: Hard
Tags: Dynamic Programming, String, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/distinct-subsequences/description/>

DESCRIPTION

Count how many distinct subsequences of s equal t.
Approaches:

* DP: dp[i][j] = ways s[:i] -> t[:j]; careful with indices and large counts.
"""
