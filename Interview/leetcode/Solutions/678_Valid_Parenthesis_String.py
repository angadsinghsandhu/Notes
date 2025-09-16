# File: Leetcode/Solutions/678_Valid_Parenthesis_String.py

"""
Problem Number: 678
Problem Name: Valid Parenthesis String
Difficulty: Medium
Tags: Greedy, Stack, String, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/valid-parenthesis-string/description/>

DESCRIPTION

String contains '(' , ')', and '*' where '*' can be '(', ')', or empty. Determine if string can be valid.
Approaches:

* Track range of possible open counts (low, high) while scanning; ensure low never < 0; final low == 0 for valid.
* O(n) time, O(1) space.
"""
