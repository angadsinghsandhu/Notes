# 1.12 Disjoint Sets Data Structure

## Overview

In this lecture, we delve into the concept of disjoint sets, a data structure that is particularly useful in graph-related algorithms such as cycle detection and Kruskal's algorithm for finding the minimum spanning tree. We will cover fundamental operations like find and union, and explore efficient techniques like weighted union and collapsing find.

## Introduction to Disjoint Sets

- **Definition**: Disjoint sets are collections of non-overlapping sets. Two sets are disjoint if their intersection is an empty set.
- **Key Operations**: The primary operations are `find` and `union`.
  - `Find`: Determines which set a particular element belongs to.
  - `Union`: Merges two distinct sets into one.

## Detecting Cycles in Undirected Graphs

Disjoint sets are particularly useful for detecting cycles in undirected graphs, a common requirement in many graph algorithms.

### Example

Consider a graph divided into two components:

- Set S1 contains vertices {1, 2, 3, 4}.
- Set S2 contains vertices {5, 6, 7, 8}.

If we attempt to find the intersection of S1 and S2, we get an empty set, illustrating that they are disjoint.

### Cycle Detection

To detect a cycle:

1. Use `find` to determine the set memberships of the edge's vertices.
2. Use `union` to combine sets if the vertices belong to different sets.
3. If a proposed edge connects vertices within the same set, a cycle is formed.

## Graphical Representation and Array Implementation

Disjoint sets can be represented using an array where each element points to its parent element, thus forming a tree structure for each set.

### Operations Detail

- **Union by Rank**: This technique involves always attaching the smaller tree under the root of the larger tree to keep the structure balanced.
- **Collapsing Find**: This optimization reduces the path length for all nodes leading up to the root when the `find` operation is executed, speeding up future operations.

## Practical Applications

- **Kruskal's Algorithm**: Uses disjoint sets to select edges that do not form a cycle, effectively ensuring the minimum spanning tree condition.
- **Cycle Detection**: Fundamental in various graph algorithms to prevent the traversal of redundant paths.

## Summary

This lecture provided a comprehensive overview of disjoint sets, including their operations and applications in computer science. Understanding how to manage and utilize disjoint sets effectively is crucial for optimizing graph algorithms and ensuring efficient data structure management.
