# FIND THE CITY WITH THE SMALLEST NUMBER OF NEIGHBORS AT A THRESHOLD DISTANCE

# Problem number: 1334
# Difficulty: Medium
# Tags: Graph, Dynamic Programming, Floyd-Warshall
# link: https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/

from typing import List

class Solution:
    """
    This problem involves finding the city with the smallest number of reachable cities within a given distance threshold.
    To solve this, we can use the Floyd-Warshall algorithm, which efficiently computes the shortest paths between all pairs of cities.
    We initialize a distance matrix where each city is only directly connected to its neighbors, then iteratively update the matrix to account for indirect connections.
    Finally, we count the number of cities within the distance threshold for each city and return the city with the smallest count, breaking ties by selecting the city with the greatest index.

    T.C. : O(n^3)
    S.C. : O(n^2)

    Input:
        - n : int : number of cities
        - edges : List[List[int]] : list of edges, where each edge is represented as [from, to, weight]
        - distanceThreshold : int : the maximum distance within which cities are considered neighbors

    Output:
        - int : the city with the smallest number of reachable cities within the distance threshold
    """
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # Initialize distance matrix with infinity
        dist = [[float('inf')] * n for _ in range(n)]
        
        # Distance to self is 0
        for i in range(n):
            dist[i][i] = 0
        
        # Fill the distance matrix with given edges
        for u, v, w in edges:
            dist[u][v] = w
            dist[v][u] = w
        
        # Floyd-Warshall algorithm to find all pairs shortest paths
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        # Find the city with the minimum number of neighbors within the distance threshold
        min_neighbors = float('inf')
        result_city = -1
        
        for i in range(n):
            count = sum(1 for j in range(n) if dist[i][j] <= distanceThreshold)
            if count < min_neighbors or (count == min_neighbors and i > result_city):
                min_neighbors = count
                result_city = i
        
        return result_city
    
# Sample Inputs
n = 4
edges = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
distanceThreshold = 4

# Expected Output : 3
print(Solution().findTheCity(n, edges, distanceThreshold))