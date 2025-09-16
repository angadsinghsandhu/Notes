# File: Leetcode/Solutions/97_Interleaving_String.py

"""
Problem Number: 97
Problem Name: Interleaving String
Difficulty: Medium
Tags: Dynamic Programming, String, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/interleaving-string/description/>

DESCRIPTION

Check if s3 is formed by interleaving s1 and s2.
Approaches:

* 2D DP dp[i][j] indicates whether s1[:i] and s2[:j] can form s3[:i+j]; optimize to 1D.
"""
