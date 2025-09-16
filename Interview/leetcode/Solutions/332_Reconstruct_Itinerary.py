# File: Leetcode/Solutions/332_Reconstruct_Itinerary.py

"""
Problem Number: 332
Problem Name: Reconstruct Itinerary
Difficulty: Hard
Tags: Graph, Eulerian Path, DFS, Heap, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/reconstruct-itinerary/description/>

DESCRIPTION

Given flight tickets [from,to], reconstruct itinerary starting at "JFK" using all tickets exactly once and lexicographically smallest route.
Approaches:

* Hierholzer's algorithm (Eulerian path) with adjacency lists stored as min-heaps or sorted lists; post-order reverse.
"""
