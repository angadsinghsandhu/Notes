# File: Leetcode/Solutions/695_Max_Area_of_Island.py

"""
Problem Number: 695
Problem Name: Max Area of Island
Difficulty: Medium
Tags: DFS, BFS, Grid, Graph, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/max-area-of-island/description/>

DESCRIPTION

Given a 2D grid of 0s and 1s, return the maximum area (number of connected 1s) of an island in the grid. If there is no island, return 0.

Function signature example (python):

* `def maxAreaOfIsland(self, grid: List[List[int]]) -> int:`

Approaches:

* DFS flood-fill counting connected component size.
* BFS level traversal per island.
"""
