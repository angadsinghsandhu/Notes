# File: Leetcode/Solutions/735_Asteroid_Collision.py

"""
Problem Number: 735
Problem Name: Asteroid Collision
Difficulty: Medium
Tags: Stack, Array, Simulation
Company (Frequency): Google (15), Facebook (10), Amazon (10)
Leetcode Link: https://leetcode.com/problems/asteroid-collision/description/

DESCRIPTION

We are given an array `asteroids` of integers representing asteroids in a row.

For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.

Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

---

#### Example 1:
**Input:**
```plaintext
asteroids = [5,10,-5]
```

**Output:**
```plaintext
[5,10]
```

**Explanation:**  
The 10 and -5 collide, resulting in 10. The 5 and 10 never collide.

#### Constraints:
- `2 <= asteroids.length <= 10^4`
- `-1000 <= asteroids[i] <= 1000`
- `asteroids[i] != 0`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves simulating collisions between moving asteroids.
    - Using a stack can efficiently track and resolve collisions in O(n) time.
    - Asteroids moving right (positive) are stored in the stack until they collide with a left-moving (negative) asteroid.
    - Resolve collisions iteratively by comparing asteroid sizes.
    
    Input:
        asteroids: List[int] - A list representing asteroids moving in space.

    Output:
        List[int] - The final state of asteroids after all collisions.
    """
    
    def brute_force_solution(self, asteroids: List[int]) -> List[int]:
        """
        Approach:
        - Compare each asteroid pair to check for collisions.
        - Remove asteroids based on collision rules.
        
        T.C.: O(n^2) - Nested iteration over asteroid pairs.
        S.C.: O(n) - Additional space for the result list.
        """
        i = 0
        while i < len(asteroids) - 1:
            if asteroids[i] > 0 and asteroids[i+1] < 0:
                if abs(asteroids[i]) > abs(asteroids[i+1]):
                    asteroids.pop(i+1)
                elif abs(asteroids[i]) < abs(asteroids[i+1]):
                    asteroids.pop(i)
                else:
                    asteroids.pop(i)
                    asteroids.pop(i)
                i = max(0, i-1)
            else:
                i += 1
        return asteroids
    
    def optimized_solution(self, asteroids: List[int]) -> List[int]:
        """
        Approach:
        - Use a stack to store asteroids moving right.
        - When a left-moving asteroid is encountered, compare with top of stack.
        - Resolve collisions iteratively, ensuring only remaining asteroids are stored.
        
        T.C.: O(n) - Each asteroid is pushed and popped at most once.
        S.C.: O(n) - Stack can store all asteroids if no collisions occur.
        """
        stack = []
        
        for asteroid in asteroids:
            while stack and asteroid < 0 and stack[-1] > 0:
                if abs(asteroid) > stack[-1]:
                    stack.pop()
                    continue
                elif abs(asteroid) == stack[-1]:
                    stack.pop()
                break
            else:
                stack.append(asteroid)
        
        return stack

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    asteroids1 = [5, 10, -5]
    print(solution.brute_force_solution(asteroids1.copy()))  # Output: [5,10]
    print(solution.optimized_solution(asteroids1.copy()))    # Output: [5,10]

    # Test case 2
    asteroids2 = [8, -8]
    print(solution.brute_force_solution(asteroids2.copy()))  # Output: []
    print(solution.optimized_solution(asteroids2.copy()))    # Output: []

    # Test case 3
    asteroids3 = [10, 2, -5]
    print(solution.brute_force_solution(asteroids3.copy()))  # Output: [10]
    print(solution.optimized_solution(asteroids3.copy()))    # Output: [10]
