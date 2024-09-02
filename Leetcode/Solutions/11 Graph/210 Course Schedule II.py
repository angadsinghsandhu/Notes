# COURSE SCHEDULE II

# Problem number: 210
# Difficulty: Medium
# Tags: Graph, Topological Sort, BFS, DFS
# Link: https://leetcode.com/problems/course-schedule-ii/

from typing import List
from collections import deque, defaultdict

class Solution:
    """
    This problem requires finding a valid order to complete a list of courses given their prerequisites. 
    The problem can be solved using topological sorting, which can be implemented using either BFS (Kahn's Algorithm) 
    or DFS. The BFS approach uses an in-degree array and a queue to process nodes with zero in-degree, 
    while the DFS approach uses a recursive function to detect cycles and perform the sorting.

    T.C. : O(V + E) where V is the number of courses (vertices) and E is the number of dependencies (edges)
    S.C. : O(V + E) for storing the graph and additional data structures

    Input:
        - numCourses : int : the total number of courses
        - prerequisites : List[List[int]] : list of prerequisite pairs [ai, bi] where course ai depends on course bi

    Output:
        - List[int] : a valid ordering of courses to finish all courses, or an empty list if it is impossible
    """

    def findOrder_BFS(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Method 1: Kahn's Algorithm (BFS Approach)
        """
        # Step 1: Initialize the graph and in-degree array
        in_degree = [0] * numCourses
        adj_list = defaultdict(list)
        
        # Step 2: Build the graph and fill the in-degree array
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
        
        # Step 3: Initialize the queue with nodes having in-degree of 0
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        result = []
        
        # Step 4: Process nodes in the queue
        while queue:
            course = queue.popleft()
            result.append(course)
            
            for neighbor in adj_list[course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # If we processed all courses, return the result, otherwise return an empty list
        return result if len(result) == numCourses else []

    def findOrder_DFS(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Method 2: DFS Approach
        """
        # Step 1: Initialize the graph and visit array
        adj_list = defaultdict(list)
        for dest, src in prerequisites:
            adj_list[src].append(dest)
        
        visited = [0] * numCourses  # 0: not visited, 1: visiting, 2: visited
        result = []
        
        def dfs(course):
            if visited[course] == 1:
                return False  # Cycle detected
            if visited[course] == 2:
                return True  # Already processed
            
            # Mark the node as visiting
            visited[course] = 1
            
            # Recursively visit all neighbors
            for neighbor in adj_list[course]:
                if not dfs(neighbor):
                    return False
            
            # Mark the node as visited and add to the result
            visited[course] = 2
            result.append(course)
            return True
        
        # Step 2: Start DFS for each course
        for course in range(numCourses):
            if not dfs(course):
                return []
        
        # Return the reverse of the result since we added nodes after visiting their dependencies
        return result[::-1]

# Sample Inputs
numCourses = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]

# Expected Outputs : [0, 1, 2, 3] or [0, 2, 1, 3]

# Testing both methods
sol = Solution()
print("BFS Method Output:", sol.findOrder_BFS(numCourses, prerequisites))
print("DFS Method Output:", sol.findOrder_DFS(numCourses, prerequisites))
