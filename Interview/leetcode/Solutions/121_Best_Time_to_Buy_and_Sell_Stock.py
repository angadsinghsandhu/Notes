# File: Leetcode/Solutions/121_Best_Time_to_Buy_and_Sell_Stock.py

"""
Problem Number: 121
Problem Name: Best Time to Buy and Sell Stock
Difficulty: Easy
Tags: Array, Dynamic Programming
Company (Frequency): Amazon (45), Microsoft (30), Google (25)
Leetcode Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/

DESCRIPTION

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.

---

#### Example 1:
Input:
prices = [7, 1, 5, 3, 6, 4]

Output:
5

Explanation:
Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5.

#### Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding the maximum profit by buying and selling a stock on different days.
    - A brute-force approach involves checking every pair of buy and sell days, but this is inefficient.
    - An optimized approach uses a single pass to track the minimum price and calculate the maximum profit.

    Input:
        prices: List[int] - A list of stock prices where `prices[i]` is the price on the `i-th` day.

    Output:
        int - The maximum profit achievable.
    """

    def brute_force_solution(self, prices: List[int]) -> int:
        """
        Approach:
        - Iterate through every possible pair of buy and sell days.
        - Calculate the profit for each pair and track the maximum profit.

        T.C.: O(n^2) - Checking every pair of days.
        S.C.: O(1) - No additional space used.
        """
        max_profit = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                profit = prices[j] - prices[i]
                if profit > max_profit:
                    max_profit = profit
        return max_profit

    def optimized_solution(self, prices: List[int]) -> int:
        """
        Approach:
        - Use a single pass to track the minimum price encountered so far.
        - Calculate the profit for each day by subtracting the minimum price from the current price.
        - Track the maximum profit.

        T.C.: O(n) - Single pass through the prices list.
        S.C.: O(1) - Constant space used.
        """
        if not prices:
            return 0

        min_price = float('inf')
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price

        return max_profit

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    prices1 = [7, 1, 5, 3, 6, 4]
    print(solution.brute_force_solution(prices1))  # Output: 5
    print(solution.optimized_solution(prices1))    # Output: 5

    # Test case 2
    prices2 = [7, 6, 4, 3, 1]
    print(solution.brute_force_solution(prices2))  # Output: 0
    print(solution.optimized_solution(prices2))    # Output: 0