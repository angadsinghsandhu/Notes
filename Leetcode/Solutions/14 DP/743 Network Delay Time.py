# NETWORK DELAY TIME

# Problem number: 743
# Difficulty: Medium
# Tags: Graph, Dijkstra's Algorithm, Breadth-First Search (BFS), Bellman-Ford Algorithm
# link: https://leetcode.com/problems/network-delay-time/

from typing import List

from heapq import heappop, heappush
from collections import defaultdict
import sys

class Solution:
    """
    This problem involves finding the minimum time for a signal to reach all nodes in a network starting
    from a given node. The problem can be modeled as a shortest path problem on a directed graph. We can 
    solve this problem using Dijkstra's algorithm to efficiently find the shortest paths from the 
    starting node to all other nodes.

    T.C. : O((n + times.length) * log(n))
    S.C. : O(n + times.length)

    Input:
        - times : List[List[int]] : list of directed edges, each represented as (ui, vi, wi)
        - n : int : number of nodes in the network
        - k : int : starting node

    Output:
        - int : minimum time for all nodes to receive the signal, or -1 if not all nodes can be reached
    """
    
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # initialize the graph
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        
        # initialize the priority queue and the dictionary to track the shortest times
        heap = [(0, k)]  # (time, node)
        dist = {i: sys.maxsize for i in range(1, n + 1)}
        dist[k] = 0
        
        # process the priority queue
        while heap:
            time, node = heappop(heap)
            
            # if we find a shorter path, continue
            if time > dist[node]:
                continue
            
            # update the distances for adjacent nodes
            for v, w in graph[node]:
                if time + w < dist[v]:
                    dist[v] = time + w
                    heappush(heap, (dist[v], v))
        
        # find the maximum time among all nodes
        max_time = max(dist.values())
        
        # if the maximum time is still infinity, some nodes are unreachable
        return max_time if max_time < sys.maxsize else -1

# Sample Inputs
times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
n = 4
k = 2

# Expected Output : 2
print(Solution().networkDelayTime(times, n, k))