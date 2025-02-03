# TODO: revisit

# File: Leetcode/Solutions/Amazon/207_Course_Schedule.py

"""
Problem Number: 207
Problem Name: Course Schedule
Difficulty: Medium
Tags: Depth-First Search, Breadth-First Search, Graph, Topological Sort
Company (Frequency): Amazon (45)
Leetcode Link: https://leetcode.com/problems/course-schedule/description/

DESCRIPTION

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you must take course `bi` first if you want to take course `ai`.

Return `true` if you can finish all courses. Otherwise, return `false`.

---

#### Example 1:
**Input:**
```plaintext
numCourses = 2, prerequisites = [[1,0]]
```

**Output:**
```plaintext
true
```

**Explanation:**  
There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.

#### Constraints:
- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- All the pairs `prerequisites[i]` are unique.
"""

from collections import defaultdict, deque
from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves determining whether it is possible to complete all courses given their prerequisites.
    - This can be modeled as a directed graph where each course is a node, and prerequisites are directed edges.
    - We need to detect if there is a cycle in the graph. If there is a cycle, it is impossible to complete all courses.
    - We can use topological sorting to determine if the graph is a Directed Acyclic Graph (DAG).

    Input:
        numCourses: int - The total number of courses.
        prerequisites: List[List[int]] - A list of prerequisite pairs.

    Output:
        bool - True if all courses can be completed, False otherwise.
    """

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Approach:
        - Build a graph representation of the courses and their prerequisites.
        - Calculate the in-degree (number of prerequisites) for each course.
        - Use a queue to perform a BFS-based topological sort.
        - Start with courses that have no prerequisites (in-degree = 0).
        - Process each course, reduce the in-degree of its neighbors, and add them to the queue if their in-degree becomes 0.
        - If all courses are processed, return True; otherwise, return False.

        T.C.: O(V + E) - Where V is the number of courses and E is the number of prerequisites.
        S.C.: O(V + E) - Space for the graph and auxiliary data structures.
        """
        # Initialize the graph and in-degree count
        graph = defaultdict(list)
        in_degree = [0] * numCourses
        
        # Build the graph and update in-degree counts
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1
        
        # Initialize the queue with courses that have no prerequisites
        queue = deque([course for course in range(numCourses) if in_degree[course] == 0])
        
        # Counter for the number of courses processed
        processed_courses = 0
        
        # Perform BFS-based topological sort
        while queue:
            current_course = queue.popleft()
            processed_courses += 1
            
            # Reduce the in-degree of neighbors and add them to the queue if in-degree becomes 0
            for neighbor in graph[current_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # If all courses are processed, return True; otherwise, return False
        return processed_courses == numCourses

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    numCourses1 = 2
    prerequisites1 = [[1, 0]]
    print(solution.canFinish(numCourses1, prerequisites1))  # Output: True

    # Test case 2
    numCourses2 = 2
    prerequisites2 = [[1, 0], [0, 1]]
    print(solution.canFinish(numCourses2, prerequisites2))  # Output: False