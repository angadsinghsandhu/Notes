# File: Leetcode/Solutions/131_Palindrome_Partitioning.py

"""
Problem Number: 131
Problem Name: Palindrome Partitioning
Difficulty: Medium
Tags: Backtracking, Dynamic Programming, String, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/palindrome-partitioning/description/>

DESCRIPTION

Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of `s`.

Function signature example (python):

* `def partition(self, s: str) -> List[List[str]]:`

Approaches:

* Backtracking with a helper to check palindrome (O(n) check)
* Precompute palindrome DP table `isPal[i][j]` to reduce repeated checks
"""
