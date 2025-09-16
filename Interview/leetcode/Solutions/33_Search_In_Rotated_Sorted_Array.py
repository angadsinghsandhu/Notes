# File: Leetcode/Solutions/33_Search_In_Rotated_Sorted_Array.py

"""
Problem Number: 33
Problem Name: Search In Rotated Sorted Array
Difficulty: Medium
Tags: Array, Binary Search, Neetcode 150
Company (Frequency): Amazon, Apple, Facebook, Google, Microsoft
Leetcode Link: https://leetcode.com/problems/search-in-rotated-sorted-array/description/

DESCRIPTION

There is an integer array `nums` sorted in ascending order (with distinct values).

Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (`0 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). For example, `[0,1,2,4,5,6,7]` rotated at pivot index 3 becomes `[4,5,6,7,0,1,2]`.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or -1 if it is not in `nums`.

You must write an algorithm with $O(log n)$ runtime complexity.
"""