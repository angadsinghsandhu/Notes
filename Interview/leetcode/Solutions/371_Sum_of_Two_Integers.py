# File: Leetcode/Solutions/371_Sum_of_Two_Integers.py

"""
Problem Number: 371
Problem Name: Sum of Two Integers
Difficulty: Medium
Tags: Bit Manipulation, Math, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/sum-of-two-integers/description/>

DESCRIPTION

Add two integers without using '+' or '-' operators.
Approaches:

* Use bitwise XOR (sum without carry) and AND+shift for carry. Iterate until carry is zero (handle signed ints carefully).
"""
