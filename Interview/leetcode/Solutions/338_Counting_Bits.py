# File: Leetcode/Solutions/338_Counting_Bits.py

"""
Problem Number: 338
Problem Name: Counting Bits
Difficulty: Easy
Tags: Dynamic Programming, Bit Manipulation, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/counting-bits/description/>

DESCRIPTION

Given n, return array of bit counts for 0..n.
Approaches:

* DP relation: dp[i] = dp[i >> 1] + (i & 1).
"""
