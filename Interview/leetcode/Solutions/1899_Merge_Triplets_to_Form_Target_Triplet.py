# File: Leetcode/Solutions/1899_Merge_Triplets_to_Form_Target_Triplet.py

"""
Problem Number: 1899
Problem Name: Merge Triplets to Form Target Triplet
Difficulty: Medium
Tags: Array, Greedy, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/merge-triplets-to-form-target-triplet/description/>

DESCRIPTION

Given triplets and target triplet, check whether you can select some triplets and merge them (element-wise max) to form target.
Approaches:

* Keep candidates that do not exceed target; accumulate max across indices; check equality.
* O(n) time.
"""
