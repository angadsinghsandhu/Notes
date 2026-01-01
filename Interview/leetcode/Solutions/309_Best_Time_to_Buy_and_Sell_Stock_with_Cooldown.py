# File: Leetcode/Solutions/309_Best_Time_to_Buy_and_Sell_Stock_with_Cooldown.py

"""
Problem Number: 309
Problem Name: Best Time to Buy and Sell Stock with Cooldown
Difficulty: Medium
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft
Leetcode Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/

DESCRIPTION

You are given an array `prices` where `prices[i]` is the price of a given stock on the `ith` day.

Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:
- After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

---

#### Example 1:
Input: prices = [1,2,3,0,2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]

---

#### Example 2:
Input: prices = [1]
Output: 0

---

#### Constraints:
- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000
"""

from typing import List

class Solution:
    """
    Thought Process:
    - We are in one of two states at any day: Buying or Selling.
    - If we are in a 'Buying' state:
        1. Buy: move to selling state, index + 1.
        2. Skip: stay in buying state, index + 1.
    - If we are in a 'Selling' state:
        1. Sell: move to buying state, but index must be + 2 (because of 1-day cooldown).
        2. Skip: stay in selling state, index + 1.
    
    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n)
    2. Memoization (Top-Down): O(n) time and space.
    3. Tabulation (Bottom-Up): O(n) time and space.
    4. State Machine (Space Optimized): O(n) time, O(1) space.
    """

    def max_profit_memoization(self, prices: List[int]) -> int:
        """
        Approach: Top-Down DP (Memoization)
        - State: (index, buying_boolean)

        T.C.: O(n)
        S.C.: O(n)
        """
        memo = {}

        def dfs(i, buying):
            if i >= len(prices):
                return 0
            if (i, buying) in memo:
                return memo[(i, buying)]

            if buying:
                # Choice 1: Buy (subtract price)
                buy = dfs(i + 1, False) - prices[i]
                # Choice 2: Cooldown/Skip
                cooldown = dfs(i + 1, True)
                memo[(i, buying)] = max(buy, cooldown)
            else:
                # Choice 1: Sell (add price, skip next day due to cooldown)
                sell = dfs(i + 2, True) + prices[i]
                # Choice 2: Cooldown/Skip
                cooldown = dfs(i + 1, False)
                memo[(i, buying)] = max(sell, cooldown)
            
            return memo[(i, buying)]

        return dfs(0, True)

    def max_profit_optimized(self, prices: List[int]) -> int:
        """
        Approach: State Machine (Optimized DP)
        - We track three states: 
            1. hold: Max profit if we currently hold a stock.
            2. sold: Max profit if we just sold a stock today.
            3. rest: Max profit if we are currently resting/cooldown.
            
        T.C.: O(n)
        S.C.: O(1)
        """
        if not prices:
            return 0
            
        # Initial states
        hold = -float('inf')
        sold = 0
        rest = 0
        
        for p in prices:
            prev_sold = sold
            # We can sell only if we were holding
            sold = hold + p
            # We can hold if we were already holding, or if we buy after a rest
            hold = max(hold, rest - p)
            # Rest is the max of previous rest or the profit from a just-sold state
            rest = max(rest, prev_sold)
            
        return max(sold, rest)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        [1, 2, 3, 0, 2],
        [1],
        [1, 2, 4]
    ]

    for prices in test_cases:
        print(f"Prices: {prices}")
        print(f"Memoization: {solution.max_profit_memoization(prices)}")
        print(f"Optimized:   {solution.max_profit_optimized(prices)}")
        print("-" * 35)

    print(f"result: {solution.max_profit_optimized(test_cases[0])}")