# File: Leetcode/Solutions/133_Clone_Graph.py

"""
Problem Number: 133
Problem Name: Clone Graph
Difficulty: Medium
Tags: DFS, BFS, Graph, Hash Table, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/clone-graph/description/>

DESCRIPTION

Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node contains a value and a list of its neighbors.

Function signature example (python):

* `def cloneGraph(self, node: 'Node') -> 'Node':`

Approaches:

* DFS recursion with a hashmap mapping original -> clone.
* BFS with queue and hashmap to map clones.
"""
