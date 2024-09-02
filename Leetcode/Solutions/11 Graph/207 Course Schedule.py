# COURSE SCHEDULE

# Problem number: 207
# Difficulty: Medium
# Tags: Graph, Topological Sort, Depth-First Search, Breadth-First Search
# Link: https://leetcode.com/problems/course-schedule/

from typing import List
from collections import defaultdict, deque

class Solution:
    """
    This problem involves determining whether it is possible to complete all courses given the 
    prerequisites. The problem can be modeled as a Directed Acyclic Graph (DAG) and solved using 
    topological sorting.

    There are two primary approaches to solve this problem:
    1. Using Depth-First Search (DFS) to detect cycles in the graph.
    2. Using Breadth-First Search (BFS) to perform topological sorting via Kahn's algorithm.

    The best method depends on the specific use case, but generally, BFS is preferred because it is 
    easier to implement and understand.
    
    T.C. : O(V + E) where V is the number of courses (vertices) and E is the number of prerequisites (edges)
    S.C. : O(V + E) for storing the graph and auxiliary structures

    Input:
        - numCourses : int : total number of courses
        - prerequisites : List[List[int]] : list of prerequisite pairs

    Output:
        - bool : True if all courses can be finished, otherwise False
    """

    def canFinishDFS(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Method 1: Depth-First Search (DFS) approach.
        We detect cycles in the graph, which would indicate that it is impossible to complete all courses.
        """
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        # states: 0 = unvisited, 1 = visiting, 2 = visited
        visited = [0] * numCourses
        
        def dfs(course):
            if visited[course] == 1:  # cycle detected
                return False
            if visited[course] == 2:  # already fully processed node
                return True
            
            visited[course] = 1  # mark as visiting
            for next_course in graph[course]:
                if not dfs(next_course):
                    return False
            visited[course] = 2  # mark as visited
            return True
        
        for i in range(numCourses):
            if not dfs(i):
                return False
        return True

    def canFinishBFS(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Method 2: Breadth-First Search (BFS) approach using Kahn's Algorithm for topological sorting.
        This approach uses an in-degree array to track the number of prerequisites for each course.
        """
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1
        
        # Queue for courses with no prerequisites (in-degree of 0)
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        count = 0
        
        while queue:
            current = queue.popleft()
            count += 1
            for next_course in graph[current]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        
        return count == numCourses  # If count equals numCourses, all courses can be finished

# Sample Inputs
numCourses1 = 2
prerequisites1 = [[1, 0]]
numCourses2 = 2
prerequisites2 = [[1, 0], [0, 1]]

# Expected Output : True
print(Solution().canFinishDFS(numCourses1, prerequisites1))  # True
print(Solution().canFinishBFS(numCourses1, prerequisites1))  # True

# Expected Output : False
print(Solution().canFinishDFS(numCourses2, prerequisites2))  # False
print(Solution().canFinishBFS(numCourses2, prerequisites2))  # False
