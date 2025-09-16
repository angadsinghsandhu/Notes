# File: Leetcode/Solutions/17_Letter_Combinations_of_a_Phone_Number.py

"""
Problem Number: 17
Problem Name: Letter Combinations of a Phone Number
Difficulty: Medium
Tags: Backtracking, String, DFS, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/>

DESCRIPTION

Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent (mapping like old phone keypad). Return the answer in any order.

Function signature example (python):

* `def letterCombinations(self, digits: str) -> List[str]`

Approaches:

* DFS/backtracking building a current string
* Iterative BFS-like expansion starting from ['']
"""
