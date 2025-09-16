# TODO: revisit

# File: Leetcode/Solutions/210_Course_Schedule_II.py

"""
Problem Number: 210
Problem Name: Course Schedule II
Difficulty: Medium
Tags: Depth-First Search, Breadth-First Search, Graph, Topological Sort, Neetcode 150
Company (Frequency): Amazon (45), Google, Facebook, Microsoft, Apple
Leetcode Link: https://leetcode.com/problems/course-schedule-ii/description/

DESCRIPTION

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you must take course `bi` first if you want to take course `ai`.

Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.

---

#### Example 1:
**Input:**
```plaintext
numCourses = 2, prerequisites = [[1,0]]
```

**Output:**
```plaintext
[0,1]
```

**Explanation:**  
There are a total of 2 courses to take. To take course 1, you should have finished course 0. So the correct course order is [0,1].

#### Constraints:
- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= numCourses * (numCourses - 1)`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- `ai != bi`
- All the pairs `[ai, bi]` are distinct.
"""

from collections import defaultdict, deque
from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding a valid order to take courses given their prerequisites.
    - This can be modeled as a directed graph where each course is a node, and prerequisites are directed edges.
    - We need to perform a topological sort on this graph to determine a valid order of courses.
    - If the graph contains a cycle, it is impossible to complete all courses, and we should return an empty array.

    Input:
        numCourses: int - The total number of courses.
        prerequisites: List[List[int]] - A list of prerequisite pairs.

    Output:
        List[int] - A list representing the order of courses to take, or an empty list if no valid order exists.
    """

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Approach:
        - Build a graph representation of the courses and their prerequisites.
        - Calculate the in-degree (number of prerequisites) for each course.
        - Use a queue to perform a BFS-based topological sort.
        - Start with courses that have no prerequisites (in-degree = 0).
        - Process each course, reduce the in-degree of its neighbors, and add them to the queue if their in-degree becomes 0.
        - If all courses are processed, return the order; otherwise, return an empty list.

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
        
        # List to store the course order
        course_order = []
        
        # Perform BFS-based topological sort
        while queue:
            current_course = queue.popleft()
            course_order.append(current_course)
            
            # Reduce the in-degree of neighbors and add them to the queue if in-degree becomes 0
            for neighbor in graph[current_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # If all courses are processed, return the order; otherwise, return an empty list
        return course_order if len(course_order) == numCourses else []

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    numCourses1 = 2
    prerequisites1 = [[1, 0]]
    print(solution.findOrder(numCourses1, prerequisites1))  # Output: [0, 1]

    # Test case 2
    numCourses2 = 4
    prerequisites2 = [[1, 0], [2, 0], [3, 1], [3, 2]]
    print(solution.findOrder(numCourses2, prerequisites2))  # Output: [0, 1, 2, 3] or [0, 2, 1, 3]

    # Test case 3
    numCourses3 = 1
    prerequisites3 = []
    print(solution.findOrder(numCourses3, prerequisites3))  # Output: [0]