# File: Leetcode/Solutions/300_Longest_Increasing_Subsequence.py

"""
Problem Number: 300
Problem Name: Longest Increasing Subsequence
Difficulty: Medium
Tags: Array, Binary Search, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Google, Microsoft, Facebook, Apple
Leetcode Link: https://leetcode.com/problems/longest-increasing-subsequence/description/

DESCRIPTION

Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements. For example, [3,6,2,7] is a subsequence of the array [0,3,1,6,2,2,7].

---

#### Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

---

#### Example 2:
Input: nums = [0,1,0,3,2,3]
Output: 4

---

#### Example 3:
Input: nums = [7,7,7,7,7,7,7]
Output: 1

---

#### Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
"""

from typing import List
import bisect

class Solution:
    """
    Thought Process:
    - We need the length of a subsequence where each element is strictly greater than the previous.
    - At each element `i`, we can either include it in a previous subsequence (if it's larger) or start a new one.
    - Standard DP approach involves checking all previous elements `j < i`.
    - An optimized approach uses "Patience Sorting" logic with binary search to maintain a list of smallest possible tail elements for all increasing subsequences.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n)
    2. Memoization (Top-Down): O(n^2) time, O(n^2) space.
    3. Tabulation (Bottom-Up): O(n^2) time, O(n) space.
    4. Binary Search (Patience Sorting): O(n log n) time, O(n) space.
    """

    def length_of_lis_recursive(self, nums: List[int]) -> int:
        """
        Approach: Pure Recursion
        T.C.: O(2^n)
        S.C.: O(n)
        """
        def solve(index, prev_idx):
            if index == len(nums):
                return 0
            
            # Choice 1: Skip current element
            res = solve(index + 1, prev_idx)
            
            # Choice 2: Include current element if it's strictly increasing
            if prev_idx == -1 or nums[index] > nums[prev_idx]:
                res = max(res, 1 + solve(index + 1, index))
            
            return res

        return solve(0, -1)

    def length_of_lis_tabulation(self, nums: List[int]) -> int:
        """
        Approach: Bottom-Up Dynamic Programming
        - dp[i] represents the length of the LIS ending at index i.
        - To find dp[i], we check all dp[j] where j < i and nums[j] < nums[i].
        
        

        T.C.: O(n^2)
        S.C.: O(n)
        """
        if not nums:
            return 0
        
        n = len(nums)
        dp = [1] * n # Base case: every single element is a subsequence of length 1
        
        for i in range(1, n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], 1 + dp[j])
                    
        return max(dp)

    def length_of_lis_binary_search(self, nums: List[int]) -> int:
        """
        Approach: Patience Sorting (Binary Search)
        - We maintain a list `sub` that stores the smallest tail of all increasing subsequences.
        - For each `x` in `nums`:
            - If `x` is larger than all tails, append it (increases LIS length).
            - Otherwise, find the first element in `sub` >= `x` and replace it with `x`.
        
        

        T.C.: O(n log n)
        S.C.: O(n)
        """
        sub = []
        for x in nums:
            if not sub or x > sub[-1]:
                sub.append(x)
            else:
                # Find the index of the first element >= x using binary search
                idx = bisect.bisect_left(sub, x)
                sub[idx] = x
        
        return len(sub)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7, 7, 7, 7]
    ]

    for nums in test_cases:
        print(f"Input: {nums}")
        # Recursive is too slow for large constraints but okay for these
        print(f"Recursive:     {solution.length_of_lis_recursive(nums)}")
        print(f"Tabulation:    {solution.length_of_lis_tabulation(nums)}")
        print(f"Binary Search: {solution.length_of_lis_binary_search(nums)}")
        print("-" * 35)

    print(f"result: {solution.length_of_lis_binary_search(test_cases[0])}")
