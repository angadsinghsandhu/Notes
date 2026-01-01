# File: Leetcode/Solutions/494_Target_Sum.py

"""
Problem Number: 494
Problem Name: Target Sum
Difficulty: Medium
Tags: Array, Dynamic Programming, Backtracking, NeetCode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft
Leetcode Link: https://leetcode.com/problems/target-sum/description/

DESCRIPTION

You are given an integer array `nums` and an integer `target`.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build the expression "+2-1".
Return the number of different expressions that you can build, which evaluates to target.

---

#### Example 1:
Input: nums = [1,1,1,1,1], target = 3
Output: 5
Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
-1+1+1+1+1 = 3
+1-1+1+1+1 = 3
+1+1-1+1+1 = 3
+1+1+1-1+1 = 3
+1+1+1+1-1 = 3

---

#### Example 2:
Input: nums = [1], target = 1
Output: 1

---

#### Constraints:
- 1 <= nums.length <= 20
- 0 <= nums[i] <= 1000
- 0 <= sum(nums[i]) <= 1000
- -1000 <= target <= 1000
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This problem can be modeled as a decision tree where at each index we choose either '+' or '-'.
    - Math Reduction: 
        Let P be the subset of numbers with a '+' sign and N be the subset with a '-' sign.
        1. sum(P) - sum(N) = target
        2. sum(P) + sum(N) = sum(nums)
        Adding (1) and (2): 2 * sum(P) = target + sum(nums)
        So, sum(P) = (target + sum(nums)) / 2
    - The problem transforms into: "Find the number of subsets that sum up to (target + total) / 2".
    - This is exactly the "Subset Sum" or "Partition Equal Subset Sum" logic.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n)
    2. Memoization (Top-Down): O(n * total_sum)
    3. Tabulation (Bottom-Up): O(n * target_subset_sum)
    4. Space Optimized: O(target_subset_sum)
    """

    def find_target_sum_ways_memo(self, nums: List[int], target: int) -> int:
        """
        Approach: Top-Down DP (Memoization)
        - State: (index, current_sum)
        T.C.: O(n * sum(nums))
        S.C.: O(n * sum(nums))
        """
        memo = {}

        def backtrack(i, cur_sum):
            if i == len(nums):
                return 1 if cur_sum == target else 0
            if (i, cur_sum) in memo:
                return memo[(i, cur_sum)]

            memo[(i, cur_sum)] = (backtrack(i + 1, cur_sum + nums[i]) + 
                                  backtrack(i + 1, cur_sum - nums[i]))
            return memo[(i, cur_sum)]

        return backtrack(0, 0)

    def find_target_sum_ways_tabulation(self, nums: List[int], target: int) -> int:
        """
        Approach: Bottom-Up DP (Reduced to Subset Sum)
        - Formula: target_subset = (target + total_sum) / 2
        
        

        T.C.: O(n * target_subset)
        S.C.: O(target_subset)
        """
        total_sum = sum(nums)
        
        # Check if target is reachable or if the reduced formula produces an integer
        if abs(target) > total_sum or (target + total_sum) % 2 != 0:
            return 0
        
        target_subset = (target + total_sum) // 2
        
        # Standard 0/1 Knapsack "Number of Ways" DP
        dp = [0] * (target_subset + 1)
        dp[0] = 1 # Base case: 1 way to get sum 0 (empty subset)
        
        for num in nums:
            # Iterate backwards to avoid using the same element twice
            for i in range(target_subset, num - 1, -1):
                dp[i] += dp[i - num]
        
        return dp[target_subset]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([1, 1, 1, 1, 1], 3),
        ([1], 1),
        ([1, 2, 1], 0)
    ]

    for n, t in test_cases:
        print(f"Nums: {n}, Target: {t}")
        print(f"Memoization: {solution.find_target_sum_ways_memo(n, t)}")
        print(f"Tabulation (Subset Sum): {solution.find_target_sum_ways_tabulation(n, t)}")
        print("-" * 35)

    print(f"result: {solution.find_target_sum_ways_tabulation(test_cases[0][0], test_cases[0][1])}")
