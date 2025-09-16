# File: Leetcode/Solutions/91_Decode_Ways.py

"""
Problem Number: 91
Problem Name: Decode Ways
Difficulty: Medium
Tags: Dynamic Programming, String, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/decode-ways/description/>

DESCRIPTION

A message containing letters A-Z is encoded to numbers with 'A'->'1', ..., 'Z'->'26'. Given a digit string, return the number of ways to decode it.

Function signature example (python):

* `def numDecodings(self, s: str) -> int:`

Approaches:

* DP: dp[i] = ways up to i; consider one-digit and two-digit valid decodes.
* Handle zeros carefully (invalid alone).
* O(n) time, O(1) space with rolling variables.
"""
