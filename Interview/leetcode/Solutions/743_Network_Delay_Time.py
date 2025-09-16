# File: Leetcode/Solutions/743_Network_Delay_Time.py

"""
Problem Number: 743
Problem Name: Network Delay Time
Difficulty: Medium
Tags: Graph, Dijkstra, Shortest Path, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/network-delay-time/description/>

DESCRIPTION

Given directed weighted edges and start node K, return time it takes for all nodes to receive signal or -1 if impossible.
Approaches:

* Dijkstra (priority queue) for shortest paths; or Bellman-Ford if negative edges (not needed here).
* O(E log V).
"""
