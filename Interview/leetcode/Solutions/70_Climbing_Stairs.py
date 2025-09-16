# File: Leetcode/Solutions/70_Climbing_Stairs.py

"""
Problem Number: 70
Problem Name: Climbing Stairs
Difficulty: Easy
Tags: Dynamic Programming, Math, Memoization, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/climbing-stairs/description/>

DESCRIPTION

You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Function signature example (python):

* `def climbStairs(self, n: int) -> int:`

Approaches:

* Fibonacci DP (iterative O(n) time, O(1) space using two variables).
* Recursion + memoization (top-down).
* Closed-form (Binet) — rarely used in interviews.
"""
