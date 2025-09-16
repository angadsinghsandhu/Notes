# File: Leetcode/Solutions/51_N_Queens.py

"""
Problem Number: 51
Problem Name: N Queens
Difficulty: Hard
Tags: Backtracking, Bit Manipulation, Recursion, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/n-queens/description/>

DESCRIPTION

The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard so that no two queens attack each other. Return all distinct solutions. Each solution contains a distinct board configuration of the n-queens' placement, using 'Q' and '.'.

Function signature example (python):

* `def solveNQueens(self, n: int) -> List[List[str]]:`

Approaches:

* Backtracking with sets (cols, diag1, diag2) to track attacked positions
* Optimized bitmask solution for faster enumeration (useful for larger n)
"""
