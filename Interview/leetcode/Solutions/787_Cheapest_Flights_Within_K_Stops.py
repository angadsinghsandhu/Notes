# File: Leetcode/Solutions/787_Cheapest_Flights_Within_K_Stops.py

"""
Problem Number: 787
Problem Name: Cheapest Flights Within K Stops
Difficulty: Medium
Tags: Graph, BFS, Shortest Path, Dynamic Programming, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/cheapest-flights-within-k-stops/description/>

DESCRIPTION

Find cheapest flight price from src to dst with at most K stops.
Approaches:

* Modified Dijkstra or BFS layer-by-layer with price pruning; also dynamic programming (Bellman-Ford style relaxations for K+1 steps).
"""
