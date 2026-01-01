# File: Leetcode/Solutions/213_House_Robber_II.py

"""
Problem Number: 213
Problem Name: House Robber II
Difficulty: Medium
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Microsoft, Google, Amazon, Apple, Cisco
Leetcode Link: https://leetcode.com/problems/house-robber-ii/description/

DESCRIPTION

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

---

#### Example 1:

Input:
nums = [2,3,2]

Output:
3

Explanation:
You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.

---

#### Example 2:

Input:
nums = [1,2,3,1]

Output:
4

Explanation:
Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

---

#### Example 3:

Input:
nums = [1,2,3]

Output:
3

---

#### Constraints:

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is a variation of the "House Robber" problem where houses are in a circle.
    - The circular constraint means that the first house and the last house are adjacent.
    - Therefore, we cannot rob both the first house and the last house.
    - This allows us to break the problem into two linear subproblems:
        1. Rob houses from index 0 to n-2 (ignore the last house).
        2. Rob houses from index 1 to n-1 (ignore the first house).
    - The final answer is the maximum of these two cases.
    - Special Case: If there is only one house, we simply return its value.

    Input:
        nums: List[int] - The amount of money in each house.

    Output:
        int - The maximum money that can be robbed.
    """

    def _rob_linear_helper(self, houses: List[int]) -> int:
        """
        Standard linear house robber logic using space optimization.
        T.C.: O(k) where k is the length of the list.
        S.C.: O(1)
        """
        prev_max = 0
        curr_max = 0
        for money in houses:
            temp = curr_max
            curr_max = max(prev_max + money, curr_max)
            prev_max = temp
        return curr_max

    def rob_recursive(self, nums: List[int]) -> int:
        """
        Approach: Recursive with Case Splitting
        - Splits the problem into two linear arrays and recursively solves them.
        
        T.C.: O(2^n)
        S.C.: O(n)
        """
        if len(nums) == 1:
            return nums[0]

        def solve(arr, i):
            if i < 0:
                return 0
            return max(solve(arr, i - 1), solve(arr, i - 2) + arr[i])

        # Scenario 1: Exclude last element, Scenario 2: Exclude first element
        res1 = solve(nums[:-1], len(nums) - 2)
        res2 = solve(nums[1:], len(nums) - 2)
        return max(res1, res2)

    def rob_memoization(self, nums: List[int]) -> int:
        """
        Approach: Top-Down DP (Memoization)
        - Uses a helper with a dictionary to cache results for the two sub-ranges.

        T.C.: O(n)
        S.C.: O(n)
        """
        if len(nums) == 1:
            return nums[0]

        def solve_memo(arr):
            memo = {}
            def helper(i):
                if i < 0: return 0
                if i in memo: return memo[i]
                memo[i] = max(helper(i - 1), helper(i - 2) + arr[i])
                return memo[i]
            return helper(len(arr) - 1)

        return max(solve_memo(nums[:-1]), solve_memo(nums[1:]))

    def rob_optimized(self, nums: List[int]) -> int:
        """
        Approach: Space Optimized Bottom-Up DP
        - We apply the O(1) space logic of House Robber I to two different slices of the input.
        
        T.C.: O(n)
        S.C.: O(1)
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        # Max of (rob houses 0 to n-2) or (rob houses 1 to n-1)
        return max(self._rob_linear_helper(nums[:-1]), 
                   self._rob_linear_helper(nums[1:]))

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [2, 3, 2]
    print(f"Test Case 1: nums = {nums1}")
    print(f"Recursive Result:  {solution.rob_recursive(nums1)}")
    print(f"Memoization Result: {solution.rob_memoization(nums1)}")
    print(f"Optimized Result:   {solution.rob_optimized(nums1)}")
    print("-" * 35)

    # Test Case 2
    nums2 = [1, 2, 3, 1]
    print(f"Test Case 2: nums = {nums2}")
    print(f"Optimized Result:   {solution.rob_optimized(nums2)}")
    print("-" * 35)

    # Test Case 3
    nums3 = [1, 2, 3]
    print(f"Test Case 3: nums = {nums3}")
    print(f"Optimized Result:   {solution.rob_optimized(nums3)}")
