# File: Leetcode/Solutions/323_Number_of_Connected_Components_in_an_Undirected_Graph.py

"""
Problem Number: 323
Problem Name: Number of Connected Components in an Undirected Graph
Difficulty: Medium
Tags: Union-Find, DFS, BFS, Graph, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/>

DESCRIPTION

Given `n` nodes labeled from `0` to `n-1` and a list of undirected edges, return the number of connected components in the graph.

Function signature example (python):

* `def countComponents(self, n: int, edges: List[List[int]]) -> int:`

Approaches:

* Union-Find to merge components.
* DFS/BFS to explore components and count.
"""
