# TODO: revisit

# File: Leetcode/Solutions/309_Best_Time_to_Buy_and_Sell_Stock_with_Cooldown.py

"""
Problem Number: 309
Problem Name: Best Time to Buy and Sell Stock with Cooldown
Difficulty: Medium
Tags: Array, Dynamic Programming
Company (Frequency): Google (15), Amazon (10), Facebook (8)
Leetcode Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/

DESCRIPTION

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.

Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:

- After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).
- You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

---

#### Example 1:
**Input:**
```plaintext
prices = [1,2,3,0,2]
```
**Output:**
```plaintext
3
```
**Explanation:**
Transactions = [buy, sell, cooldown, buy, sell]

#### Constraints:
- `1 <= prices.length <= 5000`
- `0 <= prices[i] <= 1000`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This problem introduces a cooldown period after selling a stock.
    - A brute-force approach checking all possible transactions is inefficient.
    - An optimized approach uses **dynamic programming (DP)** to track different states of transactions.
    
    Input:
        prices: List[int] - A list of stock prices where `prices[i]` is the price on the `i-th` day.

    Output:
        int - The maximum profit achievable.
    """
    
    def brute_force_solution(self, prices: List[int]) -> int:
        """
        Approach:
        - Use recursion to explore all possible buy/sell combinations with cooldown.
        - This approach is inefficient for large inputs.
        
        T.C.: O(2^n) - Exponential growth due to recursion.
        S.C.: O(n) - Stack space for recursion.
        """
        def dfs(i, holding):
            if i >= len(prices):
                return 0
            if holding:
                return max(dfs(i + 1, True), dfs(i + 2, False) + prices[i])
            return max(dfs(i + 1, False), dfs(i + 1, True) - prices[i])
        
        return dfs(0, False)

    def optimized_solution(self, prices: List[int]) -> int:
        """
        Approach:
        - Use **Dynamic Programming (DP)** to track three states:
            1. **Hold (holding a stock)**: Max profit if a stock is currently held.
            2. **Sell (just sold a stock)**: Max profit if a stock was sold today.
            3. **Cooldown (not holding and not selling today)**: Max profit from rest.
        - Transition between these states to maximize profit.
        
        T.C.: O(n) - Single pass through the prices list.
        S.C.: O(1) - Constant space used (only a few variables).
        """
        if not prices:
            return 0
        
        hold, sell, cooldown = -prices[0], 0, 0
        
        for price in prices[1:]:
            prev_sell, prev_cooldown = sell, cooldown
            sell = hold + price
            hold = max(hold, cooldown - price)
            cooldown = max(prev_cooldown, prev_sell)
        
        return max(sell, cooldown)
    
    def optimized_tab_solution(self, prices: List[int]) -> int:
        """
        Approach:
        - Use a DP table with three states:
            0. Hold: Currently holding a stock.
            1. Sold: Just sold a stock (in cooldown).
            2. Rest: Not holding a stock and not in cooldown.
        - Initialize the DP table for day 0 and update it for each subsequent day.
        - The answer is the maximum profit on the last day from either the sold or rest state.
        
        T.C.: O(n) where n is the number of days.
        S.C.: O(n) for the DP table.
        """
        if not prices:
            return 0
        
        n = len(prices)
        # dp[i][0]: hold, dp[i][1]: sold, dp[i][2]: rest
        dp = [[0] * 3 for _ in range(n)]
        
        # Base case for day 0:
        dp[0][0] = -prices[0]  # Bought stock on day 0.
        dp[0][1] = 0           # Cannot sell on day 0.
        dp[0][2] = 0           # Resting on day 0.
        
        for i in range(1, n):
            # If holding stock today, either keep holding from yesterday
            # or buy today (only allowed if yesterday was a rest day)
            dp[i][0] = max(dp[i-1][0], dp[i-1][2] - prices[i])
            
            # If sold today, you must have held the stock yesterday
            dp[i][1] = dp[i-1][0] + prices[i]
            
            # If resting today, take the max profit from being in cooldown or already at rest yesterday
            dp[i][2] = max(dp[i-1][1], dp[i-1][2])
        
        # Maximum profit on the last day (can't be in the "hold" state because profit is not realized until you sell)
        return max(dp[n-1][1], dp[n-1][2])

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    prices1 = [1,2,3,0,2]
    print(solution.brute_force_solution(prices1))   # Output: 3
    print(solution.optimized_solution(prices1))     # Output: 3
    print(solution.optimized_tab_solution(prices1)) # Output: 3

    # Test case 2
    prices2 = [1]
    print(solution.brute_force_solution(prices2))   # Output: 0
    print(solution.optimized_solution(prices2))     # Output: 0
    print(solution.optimized_tab_solution(prices2)) # Output: 0
