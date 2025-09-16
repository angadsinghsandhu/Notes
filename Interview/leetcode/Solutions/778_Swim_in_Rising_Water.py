# File: Leetcode/Solutions/778_Swim_in_Rising_Water.py

"""
Problem Number: 778
Problem Name: Swim in Rising Water
Difficulty: Hard
Tags: Binary Search, Graph, Union-Find, BFS, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/swim-in-rising-water/description/>

DESCRIPTION

Given grid of heights, you can enter cells only when water level >= height; find minimum time to reach bottom-right from top-left.
Approaches:

* Binary search on time + BFS/DFS to check reachability, or Dijkstra-like min-max path (minimize max height along path).
"""
