# File: Leetcode/Solutions/312_Burst_Balloons.py

"""
Problem Number: 312
Problem Name: Burst Balloons
Difficulty: Hard
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, Facebook
Leetcode Link: https://leetcode.com/problems/burst-balloons/description/

DESCRIPTION

You are given `n` balloons, indexed from `0` to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`. You are asked to burst all the balloons.

If you burst the `ith` balloon, you will get `nums[i - 1] * nums[i] * nums[i + 1]` coins. After the burst, the `i - 1` and `i + 1` balloons become adjacent.

Find the maximum coins you can collect by bursting the balloons wisely.

Note: You may imagine `nums[-1] = nums[n] = 1`. They are not real therefore you cannot burst them.

---

#### Example 1:
Input: nums = [3,1,5,8]
Output: 167
Explanation:
nums = [3,1,5,8] --> [3,5,8] --> [3,8] --> [8] --> []
coins =  3*1*5    +   3*5*8   +   1*3*8   +   1*8*1   = 167

---

#### Example 2:
Input: nums = [1,5]
Output: 10

---

#### Constraints:
- n == nums.length
- 1 <= n <= 300
- 0 <= nums[i] <= 100
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is a classic "Interval DP" problem.
    - If we try to simulate bursting the first balloon, the subproblems become dependent because the remaining balloons shift and become neighbors.
    - REVERSE THINKING: Instead of picking which balloon to burst first, pick which balloon to burst LAST in a given range [left, right].
    - If `nums[i]` is the LAST balloon to burst in the range [left, right], then:
        1. All balloons between `left` and `i` have already been burst.
        2. All balloons between `i` and `right` have already been burst.
        3. The neighbors of `i` at the moment it bursts will be `nums[left-1]` and `nums[right+1]`.
    - Total coins = coins(left, i-1) + coins(i+1, right) + (nums[left-1] * nums[i] * nums[right+1])

    Approach Hierarchy:
    1. Brute Force (Recursion): O(n!) - Try every permutation.
    2. Memoization (Top-Down): O(n^3) time, O(n^2) space.
    3. Tabulation (Bottom-Up): O(n^3) time, O(n^2) space.
    """

    def max_coins_memo(self, nums: List[int]) -> int:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n^3)
        S.C.: O(n^2)
        """
        # Add the implicit 1s at the boundaries
        balloons = [1] + nums + [1]
        memo = {}

        

        def dfs(l, r):
            if l > r:
                return 0
            if (l, r) in memo:
                return memo[(l, r)]

            memo[(l, r)] = 0
            for i in range(l, r + 1):
                # Calculate coins if balloon i is the LAST to burst in this range
                coins = balloons[l - 1] * balloons[i] * balloons[r + 1]
                coins += dfs(l, i - 1) + dfs(i + 1, r)
                memo[(l, r)] = max(memo[(l, r)], coins)
            
            return memo[(l, r)]

        return dfs(1, len(nums))

    def max_coins_tabulation(self, nums: List[int]) -> int:
        """
        Approach: Bottom-Up DP (Tabulation)
        - We iterate through all possible interval lengths.
        
        

        T.C.: O(n^3)
        S.C.: O(n^2)
        """
        balloons = [1] + nums + [1]
        n = len(balloons)
        dp = [[0] * n for _ in range(n)]

        # length is the size of the interval [left, right]
        for length in range(1, n - 1):
            for left in range(1, n - length):
                right = left + length - 1
                for i in range(left, right + 1):
                    # i is the last balloon to burst in range [left, right]
                    coins = balloons[left - 1] * balloons[i] * balloons[right + 1]
                    coins += dp[left][i - 1] + dp[i + 1][right]
                    dp[left][right] = max(dp[left][right], coins)
                    
        return dp[1][n - 2]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        [3, 1, 5, 8],
        [1, 5],
        [7, 9, 8, 0, 7]
    ]

    for n in test_cases:
        print(f"Balloons: {n}")
        print(f"Memoization: {solution.max_coins_memo(n)}")
        print(f"Tabulation:  {solution.max_coins_tabulation(n)}")
        print("-" * 35)

    print(f"result: {solution.max_coins_tabulation(test_cases[0])}")