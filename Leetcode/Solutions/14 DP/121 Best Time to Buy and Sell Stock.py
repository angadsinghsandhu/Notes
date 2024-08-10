# BEST TIME TO BUY AND SELL STOCK

# Problem number: 121
# Difficulty: Easy
# Tags: Array, Dynamic Programming
# link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

from typing import List

class Solution:
    """
    This problem requires finding the maximum profit that can be made by buying and selling a stock on different days.
    We can solve this using two approaches: a single pass through the array (greedy approach) and a dynamic programming approach.

    Greedy Approach:
    We maintain the minimum price encountered so far and calculate the maximum profit that can be achieved by selling on the current day.

    DP Approach:
    We create two arrays: one to track the minimum price up to the current day and another to store the maximum profit achievable by selling on each day.
    The maximum profit is obtained by comparing the profit for each day.

    T.C. : O(n)
    S.C. : O(1) for Greedy, O(n) for DP

    Input:
        - prices : List[int] : list of stock prices on each day

    Output:
        - int : maximum profit achievable, or 0 if no profit can be made
    """

    def maxProfit(self, prices: List[int]) -> int:
        # Greedy approach
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
        
        return max_profit

    def maxProfitDP(self, prices: List[int]) -> int:
        # Dynamic Programming approach
        n = len(prices)
        if n == 0:
            return 0
        
        # Initialize the DP arrays
        min_price_dp = [0] * n
        max_profit_dp = [0] * n
        
        # Fill the min_price_dp array
        min_price_dp[0] = prices[0]
        for i in range(1, n):
            min_price_dp[i] = min(min_price_dp[i-1], prices[i])
        
        # Calculate the maximum profit
        max_profit_dp[0] = 0
        for i in range(1, n):
            max_profit_dp[i] = max(max_profit_dp[i-1], prices[i] - min_price_dp[i])
        
        # The last element of max_profit_dp holds the maximum profit
        return max_profit_dp[-1]

# Sample Inputs
prices = [7, 1, 5, 3, 6, 4]

# Expected Output : 5
print(Solution().maxProfit(prices)) # Using Greedy Approach
print(Solution().maxProfitDP(prices)) # Using Dynamic Programming Approach