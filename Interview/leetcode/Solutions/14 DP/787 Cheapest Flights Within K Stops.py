# CHEAPEST FLIGHTS WITHIN K STOPS

# Problem number: 787
# Difficulty: Medium
# Tags: Dynamic Programming, Graph, Breadth-First Search (BFS), Dijkstra's Algorithm
# link: https://leetcode.com/problems/cheapest-flights-within-k-stops/

from typing import List

from heapq import heappop, heappush
from collections import defaultdict
import sys


class Solution:
    """
    This problem involves finding the cheapest flight path from a source city to a destination city 
    with at most K stops. We can approach this problem using a variation of Dijkstra's algorithm, 
    specifically tailored to handle the constraint on the number of stops. We use a priority queue 
    (min-heap) to explore the cheapest flights first and a 2D DP array to track the minimum cost to 
    reach a city with a specific number of stops.

    T.C. : O((n + flights.length) * log(n))
    S.C. : O(n * (k + 1))

    Input:
        - n : int : number of cities
        - flights : List[List[int]] : list of flights, each represented as [fromi, toi, pricei]
        - src : int : source city
        - dst : int : destination city
        - k : int : maximum number of stops allowed

    Output:
        - int : the cheapest price from src to dst with at most k stops, or -1 if no such route exists
    """
    
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # initialize graph
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))
        
        # initialize the priority queue and a list to store the best prices
        heap = [(0, src, 0)]  # (cost, current city, stops)
        best = [[sys.maxsize] * (k + 2) for _ in range(n)]
        best[src][0] = 0
        
        # process the priority queue
        while heap:
            cost, city, stops = heappop(heap)
            
            # if we reach the destination, return the cost
            if city == dst:
                return cost
            
            # if we can still make more stops
            if stops <= k:
                for next_city, price in graph[city]:
                    next_cost = cost + price
                    if next_cost < best[next_city][stops + 1]:
                        best[next_city][stops + 1] = next_cost
                        heappush(heap, (next_cost, next_city, stops + 1))
        
        # if we cannot find a valid route
        return -1

# Sample Inputs
n = 4
flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
src = 0
dst = 3
k = 1

# Expected Output : 700
print(Solution().findCheapestPrice(n, flights, src, dst, k))