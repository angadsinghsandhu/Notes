# File: Leetcode/Solutions/Amazon/42_Trapping_Rain_Water.py

"""
Problem Number: 42
Problem Name: Trapping Rain Water
Difficulty: Hard
Tags: Array, Two Pointers, Dynamic Programming, Stack
Company (Frequency): Amazon (76)
Leetcode Link: <https://leetcode.com/problems/trapping-rain-water/description/>

DESCRIPTION

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

---

#### Example 1:
**Input:**
```plaintext
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
```

**Output:**
```plaintext
6
```

**Explanation:**  
The above elevation map (black section) is represented by array `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]`. In this case, 6 units of rain water (blue section) are being trapped.

#### Example 2:
**Input:**
```plaintext
height = [4, 2, 0, 3, 2, 5]
```

**Output:**
```plaintext
9
```

#### Constraints:
- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves calculating the amount of water trapped between bars in an elevation map.
    - A brute force solution would involve calculating the water trapped at each bar by finding the maximum heights on its left and right.
    - Optimized solutions include using dynamic programming (precomputing left and right max heights) and the two-pointer approach.

    Input:
        height: List[int] - The input array representing the elevation map.

    Output:
        int - The total amount of water trapped.
    """

    def brute_force_solution(self, height: List[int]) -> int:
        """
        Approach:
        - For each bar, find the maximum height to its left and right.
        - The water trapped at each bar is the minimum of the left and right maximum heights minus the current bar's height.
        - Sum the water trapped at all bars.

        T.C.: O(n^2)
        S.C.: O(1)
        """
        n = len(height)
        total_water = 0

        for i in range(n):
            left_max = max(height[:i + 1]) if i > 0 else height[i]
            right_max = max(height[i:]) if i < n - 1 else height[i]
            water = min(left_max, right_max) - height[i]
            total_water += water

        return total_water

    def dynamic_programming_solution(self, height: List[int]) -> int:
        """
        Approach:
        - Precompute the maximum height to the left and right of each bar using dynamic programming.
        - Use the precomputed values to calculate the water trapped at each bar.

        T.C.: O(n)
        S.C.: O(n)
        """
        n = len(height)
        if n == 0:
            return 0

        left_max = [0] * n
        right_max = [0] * n

        # Precompute left_max for each bar
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # Precompute right_max for each bar
        right_max[-1] = height[-1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Calculate the total water trapped
        total_water = 0
        for i in range(n):
            water = min(left_max[i], right_max[i]) - height[i]
            total_water += water

        return total_water

    def two_pointer_solution(self, height: List[int]) -> int:
        """
        Approach:
        - Use two pointers to traverse the array from both ends.
        - Track the maximum height encountered so far from the left and right.
        - Calculate the water trapped at each step based on the smaller of the two maximum heights.

        T.C.: O(n)
        S.C.: O(1)
        """
        n = len(height)
        if n == 0:
            return 0

        left, right = 0, n - 1
        left_max, right_max = height[left], height[right]
        total_water = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                total_water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                total_water += right_max - height[right]

        return total_water

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.brute_force_solution([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # Output: 6
    print(solution.dynamic_programming_solution([4, 2, 0, 3, 2, 5]))  # Output: 9
    print(solution.two_pointer_solution([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # Output: 6