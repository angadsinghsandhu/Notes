# File: Leetcode/Solutions/322_Coin_Change.py

"""
Problem Number: 322
Problem Name: Coin Change
Difficulty: Medium
Tags: Array, Dynamic Programming, Breadth-First Search, Neetcode 150
Company (Frequency): Amazon, Google, Microsoft, Facebook, Apple
Leetcode Link: https://leetcode.com/problems/coin-change/description/

DESCRIPTION

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

---

#### Example 1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

---

#### Example 2:
Input: coins = [2], amount = 3
Output: -1

---

#### Example 3:
Input: coins = [1], amount = 0
Output: 0

---

#### Constraints:
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is a classic optimization problem (Unbounded Knapsack variant).
    - We want to find the minimum number of coins to reach a target `amount`.
    - For any amount `a`, the minimum coins needed is 1 + min(dp[a - coin]) for all coins in the set.
    - We use a large value (amount + 1) to represent infinity since the maximum number of coins possible is `amount` (using all 1-cent coins).

    Approach Hierarchy:
    1. Brute Force (Recursion): O(S^n) where S is amount, n is coin count.
    2. Memoization (Top-Down): O(S * n) time, O(S) space.
    3. Tabulation (Bottom-Up): O(S * n) time, O(S) space.
    4. BFS: O(S * n) time, treats the problem as a shortest path in a graph.
    """

    def coin_change_recursive(self, coins: List[int], amount: int) -> int:
        """
        Approach: Pure Recursion
        T.C.: O(S^n)
        S.C.: O(S)
        """
        def solve(rem):
            if rem == 0: return 0
            if rem < 0: return float('inf')
            
            min_coins = float('inf')
            for coin in coins:
                res = solve(rem - coin)
                if res != float('inf'):
                    min_coins = min(min_coins, 1 + res)
            return min_coins

        result = solve(amount)
        return result if result != float('inf') else -1

    def coin_change_memoization(self, coins: List[int], amount: int) -> int:
        """
        Approach: Top-Down DP with Memoization
        T.C.: O(S * n)
        S.C.: O(S)
        """
        memo = {}

        def solve(rem):
            if rem == 0: return 0
            if rem < 0: return float('inf')
            if rem in memo: return memo[rem]
            
            min_coins = float('inf')
            for coin in coins:
                res = solve(rem - coin)
                if res != float('inf'):
                    min_coins = min(min_coins, 1 + res)
            
            memo[rem] = min_coins
            return min_coins

        result = solve(amount)
        return result if result != float('inf') else -1

    def coin_change_tabulation(self, coins: List[int], amount: int) -> int:
        """
        Approach: Bottom-Up DP (Tabulation)
        T.C.: O(S * n)
        S.C.: O(S)
        """
        # Initialize DP table with amount + 1 (representing infinity)
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0 # Base case: 0 coins needed for 0 amount

        

        for a in range(1, amount + 1):
            for coin in coins:
                if a - coin >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - coin])
        
        return dp[amount] if dp[amount] != (amount + 1) else -1

    def coin_change_bfs(self, coins: List[int], amount: int) -> int:
        """
        Approach: Breadth-First Search (BFS)
        - Treat each amount as a node and each coin as an edge.
        - BFS finds the shortest path (minimum coins) to amount 0.
        
        T.C.: O(S * n)
        S.C.: O(S)
        """
        if amount == 0: return 0
        queue = [(0, 0)] # (current_sum, num_coins)
        visited = {0}
        
        for curr_sum, num_coins in queue:
            for coin in coins:
                next_sum = curr_sum + coin
                if next_sum == amount:
                    return num_coins + 1
                if next_sum < amount and next_sum not in visited:
                    visited.add(next_sum)
                    queue.append((next_sum, num_coins + 1))
        return -1

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([1, 2, 5], 11),
        ([2], 3),
        ([1], 0),
        ([186, 419, 83, 408], 6249)
    ]

    for c, a in test_cases:
        print(f"Coins: {c}, Amount: {a}")
        # Recursive is too slow for the last case
        if a < 20:
            print(f"Recursive:   {solution.coin_change_recursive(c, a)}")
        print(f"Memoization: {solution.coin_change_memoization(c, a)}")
        print(f"Tabulation:  {solution.coin_change_tabulation(c, a)}")
        print(f"BFS:         {solution.coin_change_bfs(c, a)}")
        print("-" * 35)

    print(f"result: {solution.coin_change_tabulation(test_cases[0][0], test_cases[0][1])}")