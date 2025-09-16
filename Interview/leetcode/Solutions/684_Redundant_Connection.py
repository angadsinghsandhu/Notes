# File: Leetcode/Solutions/684_Redundant_Connection.py

"""
Problem Number: 684
Problem Name: Redundant Connection
Difficulty: Medium
Tags: Union-Find, Graph, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/redundant-connection/description/>

DESCRIPTION

Given a graph of `n` nodes with `n` edges forming a tree plus one extra edge, return the edge that can be removed so that the resulting graph is a tree of `n` nodes.

Function signature example (python):

* `def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:`

Approaches:

* Union-Find (return the first edge that connects two nodes already in the same set).
"""
