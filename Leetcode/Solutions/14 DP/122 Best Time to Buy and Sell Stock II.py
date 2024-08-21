# BEST TIME TO BUY AND SELL STOCK II

# Problem number: 122
# Difficulty: Medium
# Tags: Greedy, Dynamic Programming
# link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/

from typing import List

class Solution:
    """
    This problem is about maximizing the profit by buying and selling stocks on given days.
    There are two approaches to solve this problem: a Greedy approach and a Dynamic Programming approach.

    Greedy Approach:
    The key insight is to add up all the positive differences between consecutive days. 
    This approach works because we can make multiple transactions and buy and sell on the same day.

    Dynamic Programming Approach:
    We maintain a DP array where dp[i][0] represents the maximum profit on the ith day 
    when we do not have a stock, and dp[i][1] represents the maximum profit on the ith day 
    when we have a stock. We transition based on whether we buy, sell, or do nothing on that day.

    T.C. (Greedy): O(n)
    S.C. (Greedy): O(1)

    T.C. (DP): O(n)
    S.C. (DP): O(n)

    Input:
        - prices : List[int] : list of stock prices where prices[i] is the price on the ith day

    Output:
        - int : maximum profit that can be achieved
    """

    def maxProfit(self, prices: List[int]) -> int:
        # Greedy approach to calculate max profit
        max_profit = 0
        
        # iterate over the price list
        for i in range(1, len(prices)):
            # add the difference if the price is higher than the previous day's price
            if prices[i] > prices[i - 1]:
                max_profit += prices[i] - prices[i - 1]
        
        # return the accumulated profit
        return max_profit
    
    def maxProfitDP(self, prices: List[int]) -> int:
        # Dynamic Programming approach to calculate max profit
        if not prices:
            return 0
        
        n = len(prices)
        dp = [[0] * 2 for _ in range(n)]
        
        # Base cases
        dp[0][0] = 0            # No stock on day 0
        dp[0][1] = -prices[0]   # Bought stock on day 0
        
        # Fill the dp array
        for i in range(1, n):
            dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])  # Max of doing nothing or selling stock today
            dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])  # Max of doing nothing or buying stock today
        
        # Maximum profit at the end of the last day without any stock
        return dp[-1][0]

# Sample Inputs
prices = [7, 1, 5, 3, 6, 4]

# Expected Output : 7 (Greedy approach)
print(Solution().maxProfit(prices))

# Expected Output : 7 (DP approach)
print(Solution().maxProfitDP(prices))