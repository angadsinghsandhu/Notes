# File: Leetcode/Solutions/518_Coin_Change_II.py

"""
Problem Number: 518
Problem Name: Coin Change II
Difficulty: Medium
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Google, Microsoft, Bloomberg
Leetcode Link: https://leetcode.com/problems/coin-change-ii/description/

DESCRIPTION

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.

---

#### Example 1:
Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: There are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

---

#### Example 2:
Input: amount = 3, coins = [2]
Output: 0
Explanation: The amount of 3 cannot be made up just with coins of 2.

---

#### Example 3:
Input: amount = 10, coins = [10]
Output: 1

---

#### Constraints:
- 1 <= coins.length <= 300
- 1 <= coins[i] <= 5000
- All the values of coins are unique.
- 0 <= amount <= 5000
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is the "Number of Ways" variation of the Unbounded Knapsack problem.
    - Unlike Coin Change I (min coins), here we count distinct combinations.
    - To avoid counting permutations (e.g., [1,2] and [2,1]) as different ways, we must iterate through the coins one by one.
    - For each coin, we update the number of ways to reach every amount from `coin` to `amount`.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n)
    2. Memoization (Top-Down): O(n * amount) time and space.
    3. Tabulation (Bottom-Up): O(n * amount) time, O(amount) space.
    """

    def change_recursive(self, amount: int, coins: List[int]) -> int:
        """
        Approach: Pure Recursion
        - We track the current coin index to ensure we don't pick a 'previous' coin again,
          which prevents duplicate permutations.
        """
        def solve(i, rem):
            if rem == 0: return 1
            if rem < 0 or i == len(coins): return 0
            
            # Choice 1: Use the current coin (stay at index i)
            # Choice 2: Skip the current coin (move to index i + 1)
            return solve(i, rem - coins[i]) + solve(i + 1, rem)

        return solve(0, amount)

    def change_memoization(self, amount: int, coins: List[int]) -> int:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * amount)
        S.C.: O(n * amount)
        """
        memo = {}

        def solve(i, rem):
            if rem == 0: return 1
            if rem < 0 or i == len(coins): return 0
            if (i, rem) in memo: return memo[(i, rem)]
            
            memo[(i, rem)] = solve(i, rem - coins[i]) + solve(i + 1, rem)
            return memo[(i, rem)]

        return solve(0, amount)

    def change_tabulation_2d(self, amount: int, coins: List[int]) -> int:
        """
        Approach: Bottom-Up DP (2D Table)
        - dp[i][j] = number of ways to make amount j using first i coins.
        """
        n = len(coins)
        dp = [[0] * (amount + 1) for _ in range(n + 1)]
        
        # Base case: 1 way to make amount 0 (using no coins)
        for i in range(n + 1):
            dp[i][0] = 1
            
        for i in range(1, n + 1):
            for j in range(1, amount + 1):
                # Ways without current coin
                dp[i][j] = dp[i-1][j]
                # Ways with current coin (if it fits)
                if j - coins[i-1] >= 0:
                    dp[i][j] += dp[i][j - coins[i-1]]
        
        return dp[n][amount]

    def change_tabulation_optimized(self, amount: int, coins: List[int]) -> int:
        """
        Approach: Space-Optimized Bottom-Up DP (1D Table)
        - We only need the previous row's values, which we can update in-place.
        - Important: The inner loop must go from `coin` to `amount` (forward) 
          to allow for multiple uses of the same coin.

        

        T.C.: O(n * amount)
        S.C.: O(amount)
        """
        dp = [0] * (amount + 1)
        dp[0] = 1 # Base case: 1 way to make amount 0
        
        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] += dp[x - coin]
                
        return dp[amount]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        (5, [1, 2, 5]),
        (3, [2]),
        (10, [10])
    ]

    for a, c in test_cases:
        print(f"Amount: {a}, Coins: {c}")
        print(f"Memoization: {solution.change_memoization(a, c)}")
        print(f"Tabulation:  {solution.change_tabulation_optimized(a, c)}")
        print("-" * 35)

    print(f"result: {solution.change_tabulation_optimized(test_cases[0][0], test_cases[0][1])}")