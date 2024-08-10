# BEST TIME TO BUY AND SELL STOCK III

# Problem number: 123
# Difficulty: Hard
# Tags: Dynamic Programming, Greedy
# link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/

from typing import List

class Solution:
    """
    This problem asks us to find the maximum profit from at most two transactions on a list of stock prices.
    We can solve this problem using two approaches: a Greedy approach and a more explicit Dynamic Programming approach.

    **Greedy Approach:**
    We maintain four states:
    - first_buy: Maximum profit after the first buy.
    - first_sell: Maximum profit after the first sell.
    - second_buy: Maximum profit after the second buy.
    - second_sell: Maximum profit after the second sell.
    
    These states are updated as we iterate through the prices to capture the maximum profit.

    **Dynamic Programming Approach:**
    We can also solve this using a 2D DP array where dp[i][j] represents the maximum profit we can achieve up to day i with at most j transactions.
    We update the dp array by deciding whether to make a transaction on that day or not.

    T.C. : O(n) for both approaches
    S.C. : O(1) for Greedy, O(n*2) for DP

    Input:
        - prices : List[int] : list of stock prices

    Output:
        - int : maximum profit that can be achieved with at most two transactions
    """
    
    def maxProfitGreedy(self, prices: List[int]) -> int:
        first_buy = float('-inf')
        first_sell = 0
        second_buy = float('-inf')
        second_sell = 0
        
        for price in prices:
            first_buy = max(first_buy, -price)
            first_sell = max(first_sell, first_buy + price)
            second_buy = max(second_buy, first_sell - price)
            second_sell = max(second_sell, second_buy + price)
        
        return second_sell

    def maxProfitDP(self, prices: List[int]) -> int:
        if not prices:
            return 0
        
        n = len(prices)
        dp = [[0] * 3 for _ in range(n)]
        
        for j in range(1, 3):
            max_diff = -prices[0]
            for i in range(1, n):
                dp[i][j] = max(dp[i-1][j], prices[i] + max_diff)
                max_diff = max(max_diff, dp[i][j-1] - prices[i])
        
        return dp[-1][-1]

# Sample Inputs
prices = [3, 3, 5, 0, 0, 3, 1, 4]

# Expected Output : 6 using both methods
solution = Solution()
print(solution.maxProfitGreedy(prices))
print(solution.maxProfitDP(prices))