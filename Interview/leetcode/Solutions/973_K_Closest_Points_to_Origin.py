# File: Leetcode/Solutions/973_K_Closest_Points_to_Origin.py

"""
Problem Number: 973
Problem Name: K Closest Points to Origin
Difficulty: Medium
Tags: Heap (Priority Queue), Divide and Conquer, Sorting, Geometry, Neetcode 150
Company (Frequency): Amazon, Microsoft, Google, Apple, Facebook (High)
Leetcode Link: https://leetcode.com/problems/k-closest-points-to-origin/

DESCRIPTION

Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)^2 + (y1 - y2)^2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

Example 1:
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]

Example 2:
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]

Constraints:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4
"""

from typing import List
import heapq

class Solution:
    """
    Thought Process:
    - Calculate the squared distance for each point (avoid sqrt for efficiency).
    - Identify the k smallest distances using various methods: sorting, max-heap, or built-in heap functions.

    Approach:
    - Three methods are provided: sorting, max-heap, and using heapq.nsmallest.
    - All methods leverage the squared distance to avoid computational overhead.
    """

    def kClosest_sorting(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Approach:
        - Sort the points based on their squared distances and return the first k.
        
        Time Complexity: O(n log n) due to sorting.
        Space Complexity: O(n) for storing sorted list.
        """
        points.sort(key=lambda p: p[0]**2 + p[1]**2)
        return points[:k]

    def kClosest_max_heap(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Approach:
        - Maintain a max-heap of size k to track the k closest points.
        - Push negative distances to simulate a max-heap using Python's min-heap.
        
        Time Complexity: O(n log k) for heap operations.
        Space Complexity: O(k) for storing the heap.
        """
        heap = []
        for (x, y) in points:
            dist = -(x**2 + y**2)  # Store negative to simulate max-heap
            if len(heap) < k:
                heapq.heappush(heap, (dist, x, y))
            else:
                # Replace the largest element if current is smaller
                heapq.heappushpop(heap, (dist, x, y))
        return [[x, y] for (dist, x, y) in heap]

    def kClosest_heapq_nsmallest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Approach:
        - Use Python's heapq.nsmallest to directly get the k closest points.
        
        Time Complexity: O(n log k) for small k, optimized by the heapq module.
        Space Complexity: O(k) for storing the result.
        """
        return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    points1 = [[1,3], [-2,2]]
    k1 = 1
    print(solution.kClosest_sorting(points1, k1))          # Expected Output: [[-2, 2]]
    print(solution.kClosest_max_heap(points1, k1))         # Expected Output: [[-2, 2]]
    print(solution.kClosest_heapq_nsmallest(points1, k1))  # Expected Output: [[-2, 2]]

    # Test case 2
    points2 = [[3,3], [5,-1], [-2,4]]
    k2 = 2
    print(solution.kClosest_sorting(points2, k2))          # Expected Output: [[3,3], [-2,4]]
    print(solution.kClosest_max_heap(points2, k2))         # Expected Output: [[3,3], [-2,4]]
    print(solution.kClosest_heapq_nsmallest(points2, k2))  # Expected Output: [[3,3], [-2,4]]