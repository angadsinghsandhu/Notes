# BEST TIME TO BUY AND SELL STOCK

# Problem number: 121
# Difficulty: Easy
# Tags: Array, Dynamic Programming, Sliding Window
# Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

from typing import List

class Solution:
    """
    This problem requires finding the maximum profit from buying and selling stock once. 
    The key is to track the minimum price and calculate the potential profit at each day, 
    updating the maximum profit accordingly.
    
    We will implement two methods:
    1. Single Pass (Optimal)
    2. Brute Force (Less Optimal)
    """

    def maxProfit(self, prices: List[int]) -> int:
        """
        Single Pass approach to calculate maximum profit.
        
        T.C. : O(n) where n is the number of days (prices array length)
        S.C. : O(1) since we only store a few variables (min_price and max_profit)
        """
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price  # Track the minimum price so far
            elif price - min_price > max_profit:
                max_profit = price - min_price  # Calculate the profit

        return max_profit

    def maxProfit_bruteForce(self, prices: List[int]) -> int:
        """
        Brute Force approach to calculate maximum profit.
        
        T.C. : O(n^2) where n is the number of days (prices array length)
        S.C. : O(1) since we only store a single variable (max_profit)
        """
        max_profit = 0

        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                profit = prices[j] - prices[i]
                if profit > max_profit:
                    max_profit = profit

        return max_profit

# Best Method: The single pass approach is optimal due to its O(n) time complexity.

# Sample Inputs for Testing
prices1 = [7,1,5,3,6,4]  # Expected output: 5
prices2 = [7,6,4,3,1]    # Expected output: 0

# Testing Optimal Method
print(Solution().maxProfit(prices1))  # Should output 5
print(Solution().maxProfit(prices2))  # Should output 0

# Testing Brute Force Method
print(Solution().maxProfit_bruteForce(prices1))  # Should output 5
print(Solution().maxProfit_bruteForce(prices2))  # Should output 0
