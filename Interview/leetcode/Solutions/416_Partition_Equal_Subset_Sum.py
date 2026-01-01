# File: Leetcode/Solutions/416_Partition_Equal_Subset_Sum.py

"""
Problem Number: 416
Problem Name: Partition Equal Subset Sum
Difficulty: Medium
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Facebook, Amazon, Microsoft, Google
Leetcode Link: https://leetcode.com/problems/partition-equal-subset-sum/description/

DESCRIPTION

Given an integer array `nums`, return `true` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `false` otherwise.

---

#### Example 1:
Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].

---

#### Example 2:
Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.

---

#### Constraints:
- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100
"""

from typing import List, Set

class Solution:
    """
    Thought Process:
    - This is a variation of the 0/1 Knapsack problem.
    - If we can find a subset that sums to exactly half of the total sum, the remaining elements will naturally sum to the other half.
    - Step 1: Calculate total sum. If total sum is odd, return False (cannot split evenly).
    - Step 2: Target sum = total sum / 2.
    - Step 3: Find if any combination of numbers adds up to the Target.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n) - Explore every subset.
    2. Memoization (Top-Down): O(n * target) time and space.
    3. Tabulation (Bottom-Up): O(n * target) time, O(target) space.
    4. Set-based DP: Using a set to track all possible sums.
    """

    def can_partition_recursive(self, nums: List[int]) -> bool:
        """
        Approach: Pure Recursion
        T.C.: O(2^n)
        S.C.: O(n)
        """
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2

        def solve(i, current_sum):
            if current_sum == target:
                return True
            if i >= len(nums) or current_sum > target:
                return False
            
            # Choice 1: Include nums[i], Choice 2: Exclude nums[i]
            return solve(i + 1, current_sum + nums[i]) or solve(i + 1, current_sum)

        return solve(0, 0)

    def can_partition_memoization(self, nums: List[int]) -> bool:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * target)
        S.C.: O(n * target)
        """
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2
        memo = {}

        def solve(i, current_sum):
            state = (i, current_sum)
            if current_sum == target:
                return True
            if i >= len(nums) or current_sum > target:
                return False
            if state in memo:
                return memo[state]
            
            memo[state] = solve(i + 1, current_sum + nums[i]) or solve(i + 1, current_sum)
            return memo[state]

        return solve(0, 0)

    def can_partition_tabulation(self, nums: List[int]) -> bool:
        """
        Approach: Bottom-Up DP (Space Optimized)
        - We use a boolean array `dp` where `dp[i]` is True if sum `i` is achievable.
        - We iterate through each number and update the possible sums.
        - Important: We iterate backwards through the DP array to avoid using the same element twice.

        

        T.C.: O(n * target)
        S.C.: O(target)
        """
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2

        dp = [False] * (target + 1)
        dp[0] = True # Base case: sum of 0 is always possible

        for num in nums:
            # Iterate backwards to ensure we only use 'num' once per subset
            for i in range(target, num - 1, -1):
                if dp[i - num]:
                    dp[i] = True
            if dp[target]: return True
            
        return dp[target]

    def can_partition_set(self, nums: List[int]) -> bool:
        """
        Approach: Set-based DP
        - Maintain a set of all possible sums seen so far.
        - For each new number, add it to all existing sums in the set.
        
        T.C.: O(n * target)
        S.C.: O(target)
        """
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2
        
        possible_sums = {0}
        
        for num in nums:
            next_sums = set()
            for s in possible_sums:
                if s + num == target:
                    return True
                if s + num < target:
                    next_sums.add(s + num)
            possible_sums.update(next_sums)
            
        return target in possible_sums

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        [1, 5, 11, 5],
        [1, 2, 3, 5],
        [1, 2, 5]
    ]

    for nums in test_cases:
        print(f"Input: {nums}")
        print(f"Memoization: {solution.can_partition_memoization(nums)}")
        print(f"Tabulation:  {solution.can_partition_tabulation(nums)}")
        print(f"Set DP:      {solution.can_partition_set(nums)}")
        print("-" * 35)

    print(f"result: {solution.can_partition_tabulation(test_cases[0])}")
