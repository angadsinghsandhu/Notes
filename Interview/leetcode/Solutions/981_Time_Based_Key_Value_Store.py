# File: Leetcode/Solutions/981_Time_Based_Key_Value_Store.py

"""
Problem Number: 981
Problem Name: Time Based Key-Value Store
Difficulty: Medium
Tags: Hash Table, String, Binary Search, Design, Neetcode 150
Company (Frequency): Amazon, Google, Uber, ByteDance
Leetcode Link: https://leetcode.com/problems/time-based-key-value-store/description/

DESCRIPTION

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:

- TimeMap() Initializes the object of the data structure.
- void set(String key, String value, int timestamp): Stores the key key with the value value at the given time timestamp.
- String get(String key, int timestamp): Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".
"""
