# File: Leetcode/Solutions/252_Meeting_Rooms.py

"""
Problem Number: 252
Problem Name: Meeting Rooms
Difficulty: Easy
Tags: Sorting, Intervals, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/meeting-rooms/description/>

DESCRIPTION

Given an array of meeting time intervals, determine if a person could attend all meetings (i.e., no overlaps).
Approaches:

* Sort by start time and check if current start < previous end.
* O(n log n) time.
"""
