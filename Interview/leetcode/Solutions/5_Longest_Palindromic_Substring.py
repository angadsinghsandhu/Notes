# File: Leetcode/Solutions/5_Longest_Palindromic_Substring.py

"""
Problem Number: 5
Problem Name: Longest Palindromic Substring
Difficulty: Medium
Tags: String, Dynamic Programming, Two Pointers, Expand Around Center, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/longest-palindromic-substring/description/>

DESCRIPTION

Given a string `s`, return the longest palindromic substring in `s`.

Function signature example (python):

* `def longestPalindrome(self, s: str) -> str:`

Approaches:

* Expand-around-center for each index (O(n^2) time, O(1) space).
* DP table `isPal[i][j]` (O(n^2) time & space).
* Manacher's algorithm for O(n) time (advanced).
"""
