# File: Leetcode/Solutions/198_House_Robber.py

"""
Problem Number: 198
Problem Name: House Robber
Difficulty: Medium
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, Apple, Cisco
Leetcode Link: https://leetcode.com/problems/house-robber/description/

DESCRIPTION

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

---

#### Example 1:

Input:
nums = [1,2,3,1]

Output:
4

Explanation:
Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

---

#### Example 2:

Input:
nums = [2,7,9,3,1]

Output:
12

Explanation:
Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.

---

#### Constraints:

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is a optimization problem where we need to make a sequence of decisions (rob or skip).
    - For each house i, we have two choices:
        1. Rob the house: We gain nums[i] but must skip house i-1.
        2. Skip the house: We gain 0 from this house and carry over the max profit from house i-1.
    - The recurrence relation is: f(i) = max(f(i-2) + nums[i], f(i-1)).
    - Base cases: 
        - If no houses: 0.
        - If 1 house: nums[0].
        - If 2 houses: max(nums[0], nums[1]).

    Input:
        nums: List[int] - Amount of money in each house.

    Output:
        int - Maximum money that can be robbed.
    """

    def rob_recursive(self, nums: List[int]) -> int:
        """
        Approach: Pure Recursion (Brute Force)
        - Start from the last house and recursively decide to rob or skip.
        
        T.C.: O(2^n) - Each house has two branches.
        S.C.: O(n) - Recursion stack depth.
        """
        def solve(i):
            if i < 0:
                return 0
            if i == 0:
                return nums[0]
            # Choice: Rob current house and jump back 2, or skip current house and jump back 1
            return max(solve(i - 2) + nums[i], solve(i - 1))

        return solve(len(nums) - 1)

    def rob_memoization(self, nums: List[int]) -> int:
        """
        Approach: Top-Down DP (Memoization)
        - Use a cache to store results for house indices already processed.

        T.C.: O(n)
        S.C.: O(n) - Memoization table and recursion stack.
        """
        memo = {}

        def solve(i):
            if i < 0:
                return 0
            if i == 0:
                return nums[0]
            if i in memo:
                return memo[i]
            
            memo[i] = max(solve(i - 2) + nums[i], solve(i - 1))
            return memo[i]

        return solve(len(nums) - 1)

    def rob_tabulation(self, nums: List[int]) -> int:
        """
        Approach: Bottom-Up DP (Tabulation Array)
        - Build an array where dp[i] is the max money robbed up to house i.

        T.C.: O(n)
        S.C.: O(n)
        """
        if not nums:
            return 0
        n = len(nums)
        if n == 1:
            return nums[0]
        
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        
        for i in range(2, n):
            dp[i] = max(dp[i-1], dp[i-2] + nums[i])
            
        return dp[n-1]

    def rob_optimized(self, nums: List[int]) -> int:
        """
        Approach: Space Optimized DP
        - Since we only need dp[i-1] and dp[i-2], we use two variables to track them.

        T.C.: O(n)
        S.C.: O(1)
        """
        if not nums:
            return 0
        
        prev_max = 0 # Represents dp[i-2]
        curr_max = 0 # Represents dp[i-1]
        
        # 
        for x in nums:
            temp = curr_max
            curr_max = max(prev_max + x, curr_max)
            prev_max = temp
            
        return curr_max

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [1, 2, 3, 1]
    print(f"Test Case 1: nums = {nums1}")
    print(f"Recursive Result:  {solution.rob_recursive(nums1)}")
    print(f"Memoization Result: {solution.rob_memoization(nums1)}")
    print(f"Tabulation Result:  {solution.rob_tabulation(nums1)}")
    print(f"Optimized Result:   {solution.rob_optimized(nums1)}")
    print("-" * 35)

    # Test Case 2
    nums2 = [2, 7, 9, 3, 1]
    print(f"Test Case 2: nums = {nums2}")
    print(f"Memoization Result: {solution.rob_memoization(nums2)}")
    print(f"Tabulation Result:  {solution.rob_tabulation(nums2)}")
    print(f"Optimized Result:   {solution.rob_optimized(nums2)}")
    print("-" * 35)

    # Test Case 3: Alternating large values
    nums3 = [100, 1, 1, 100]
    print(f"Test Case 3: nums = {nums3}")
    print(f"Optimized Result:   {solution.rob_optimized(nums3)}") # Expected: 200
