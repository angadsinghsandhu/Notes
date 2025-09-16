# File: Leetcode/Solutions/42_Trapping_Rain_Water.py

"""
Problem Number: 42
Problem Name: Trapping Rain Water
Difficulty: Hard
Tags: Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/trapping-rain-water/description/>

DESCRIPTION

Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

---

#### Example 1:

Input:
height = [0,1,0,2,1,0,1,3,2,1,2,1]

Output:
6

Explanation:
The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

---

#### Example 2:

Input:
height = [4,2,0,3,2,5]

Output:
9

---

#### Constraints:

- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem asks us to calculate the total amount of water that can be trapped between bars of an elevation map.
    - Water can only be trapped if there are "walls" on both sides that are higher than the current position.
    - The amount of water trapped at a specific position `i` is determined by the minimum of the maximum height to its left and the maximum height to its right, minus the current bar's height.
    - `water_at_i = min(max_left_height, max_right_height) - height[i]`
    - We need to sum this value for all relevant positions.

    Input:
        height: List[int] - The elevation map.

    Output:
        int - The total units of trapped rain water.
    """

    def two_pointers_solution(self, height: List[int]) -> int:
        """
        Approach:
        - This is an optimized in-place solution using two pointers.
        - Instead of pre-calculating all max_left and max_right for each position, we can compute them on the fly.
        - Initialize `left` pointer at 0, `right` pointer at `n-1`.
        - Initialize `left_max = 0`, `right_max = 0`.
        - Initialize `trapped_water = 0`.
        - Move the pointers inwards:
            - If `height[left] < height[right]`:
                - If `height[left] >= left_max`, update `left_max = height[left]`.
                - Else (`height[left] < left_max`), water can be trapped: `trapped_water += left_max - height[left]`.
                - Increment `left`.
            - Else (`height[right] <= height[left]`):
                - If `height[right] >= right_max`, update `right_max = height[right]`.
                - Else (`height[right] < right_max`), water can be trapped: `trapped_water += right_max - height[right]`.
                - Decrement `right`.
        - Continue until `left >= right`.

        T.C.: O(n)
        S.C.: O(1)
        """
        if not height:
            return 0

        n = len(height)
        left, right = 0, n - 1
        left_max = 0
        right_max = 0
        trapped_water = 0

        while left < right:
            if height[left] < height[right]:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    trapped_water += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    trapped_water += right_max - height[right]
                right -= 1
        return trapped_water

    def dynamic_programming_solution(self, height: List[int]) -> int:
        """
        Approach:
        - This approach involves pre-calculating the maximum height to the left and right of each bar.
        - Create two arrays: `left_max` and `right_max`.
        - `left_max[i]` stores the maximum height encountered from index 0 to `i`.
        - `right_max[i]` stores the maximum height encountered from index `n-1` to `i`.
        - Iterate from left to right to populate `left_max`.
        - Iterate from right to left to populate `right_max`.
        - Finally, iterate through the `height` array. For each bar `i`, the water trapped is `min(left_max[i], right_max[i]) - height[i]`. Sum these values.

        T.C.: O(n)
        S.C.: O(n) (for `left_max` and `right_max` arrays)
        """
        if not height:
            return 0

        n = len(height)
        left_max = [0] * n
        right_max = [0] * n

        # Populate left_max array
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i-1], height[i])

        # Populate right_max array
        right_max[n-1] = height[n-1]
        for i in range(n-2, -1, -1):
            right_max[i] = max(right_max[i+1], height[i])

        trapped_water = 0
        for i in range(n):
            water_at_current_bar = min(left_max[i], right_max[i]) - height[i]
            trapped_water += max(0, water_at_current_bar) # Ensure non-negative water

        return trapped_water


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    height1 = [0,1,0,2,1,0,1,3,2,1,2,1]
    expected1 = 6

    # Using Two Pointers Solution
    result1_two_pointers = solution.two_pointers_solution(list(height1))
    print(f"Two Pointers Solution for {height1}: {result1_two_pointers} (Expected: {expected1})") # Output: 6

    # Using Dynamic Programming Solution
    result1_dp = solution.dynamic_programming_solution(list(height1))
    print(f"DP Solution for {height1}: {result1_dp} (Expected: {expected1})") # Output: 6
    print("-" * 20)

    # Test Case 2
    height2 = [4,2,0,3,2,5]
    expected2 = 9

    # Using Two Pointers Solution
    result2_two_pointers = solution.two_pointers_solution(list(height2))
    print(f"Two Pointers Solution for {height2}: {result2_two_pointers} (Expected: {expected2})") # Output: 9

    # Using Dynamic Programming Solution
    result2_dp = solution.dynamic_programming_solution(list(height2))
    print(f"DP Solution for {height2}: {result2_dp} (Expected: {expected2})") # Output: 9
    print("-" * 20)

    # Additional Test Case: No water trapped
    height3 = [1,2,3,4,5]
    expected3 = 0
    result3_two_pointers = solution.two_pointers_solution(list(height3))
    print(f"Two Pointers Solution for {height3}: {result3_two_pointers} (Expected: {expected3})")
    result3_dp = solution.dynamic_programming_solution(list(height3))
    print(f"DP Solution for {height3}: {result3_dp} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Empty array
    height4 = []
    expected4 = 0
    result4_two_pointers = solution.two_pointers_solution(list(height4))
    print(f"Two Pointers Solution for {height4}: {result4_two_pointers} (Expected: {expected4})")
    result4_dp = solution.dynamic_programming_solution(list(height4))
    print(f"DP Solution for {height4}: {result4_dp} (Expected: {expected4})")
    print("-" * 20)

    # Additional Test Case: Single element array
    height5 = [5]
    expected5 = 0
    result5_two_pointers = solution.two_pointers_solution(list(height5))
    print(f"Two Pointers Solution for {height5}: {result5_two_pointers} (Expected: {expected5})")
    result5_dp = solution.dynamic_programming_solution(list(height5))
    print(f"DP Solution for {height5}: {result5_dp} (Expected: {expected5})")
    print("-" * 20)