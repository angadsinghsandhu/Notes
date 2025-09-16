### File: Leetcode/Solutions/188_Best_Time_to_Buy_and_Sell_Stock_IV.py

"""
Problem Number: 188
Problem Name: Best Time to Buy and Sell Stock IV
Difficulty: Hard
Tags: Array, Dynamic Programming
Company (Frequency): Amazon (85)
Leetcode Link: <https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/>

DESCRIPTION

You are given an integer `k` and an array `prices`, where `prices[i]` represents the price of a stock on day `i`.

You can complete at most **k transactions** (a transaction consists of buying and selling one stock).

**Rules:**
- You **cannot** engage in multiple transactions at the same time (i.e., you must sell the stock before buying again).
- The goal is to determine the **maximum profit** that can be made using at most `k` transactions.

---

#### Example 1:
**Input:**
```plaintext
k = 2, prices = [2,4,1]
```
**Output:**
```plaintext
2
```
**Explanation:**  
- Buy on day 1 (price = 2), sell on day 2 (price = 4), profit = `4 - 2 = 2`
- Total profit = `2`

#### Example 2:
**Input:**
```plaintext
k = 2, prices = [3,2,6,5,0,3]
```
**Output:**
```plaintext
7
```
**Explanation:**  
- Buy on day 2 (price = 2), sell on day 3 (price = 6), profit = `6 - 2 = 4`
- Buy on day 5 (price = 0), sell on day 6 (price = 3), profit = `3 - 0 = 3`
- Total profit = `4 + 3 = 7`

#### Constraints:
- `1 <= k <= 100`
- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^5`
"""

class Solution:
    """
    Thought Process:
    - Since we are limited to **k transactions**, we use **Dynamic Programming** to track profits.
    - The approach follows a **state transition** strategy:
      1. **Define a state `dp[t][d]`** where:
         - `t` represents the number of transactions completed.
         - `d` represents the day.
         - `dp[t][d]` stores the **maximum profit possible** with `t` transactions up to day `d`.
      2. **State Transition Formula**:
         - The maximum profit on day `d` using `t` transactions is:
         ```plaintext
         dp[t][d] = max(dp[t][d-1], prices[d] + max(prices[j] - dp[t-1][j] for j in range(d)))
         ```
         - Here, `prices[d] - dp[t-1][j]` represents the profit from buying on day `j` and selling on day `d`.
      3. **Optimization**:
         - Instead of computing `max(prices[j] - dp[t-1][j])` in `O(n)`, we track it dynamically.

    Input:
        k: int - The maximum number of transactions allowed.
        prices: List[int] - List of stock prices per day.

    Output:
        int - The maximum profit that can be achieved with at most `k` transactions.
    """

    def maxProfit(self, k: int, prices: list[int]) -> int:
        """
        Approach:
        - Use **Dynamic Programming**:
          - If `k >= len(prices) // 2`, we can apply a **greedy approach** (unlimited transactions).
          - Otherwise, use "optimized DP" to track profits with at most `k` transactions.
        - Initialize a DP table `dp` to track profits.
        - Iterate through the `prices` array and update the DP table dynamically.
        - Return the maximum profit from the DP table.

        T.C.: O(n * k) - Iterating over `prices` for `k` transactions.
        S.C.: O(k) - Optimized DP table.
        """
        if not prices or k == 0:
            return 0

        n = len(prices)
        
        # If k is very large, use greedy approach (equivalent to unlimited transactions)
        if k >= n // 2:
            return sum(max(prices[i] - prices[i - 1], 0) for i in range(1, n))

        # Initialize DP table
        dp = [0] * n

        for t in range(k):
            max_buy_profit = -prices[0]  # Track the maximum buy profit dynamically
            profit = 0
            for i in range(1, n):
                # Update max_buy_profit for future transactions (buying at minimum price)
                max_buy_profit = max(max_buy_profit, dp[i] - prices[i])
                # Max profit from either not selling or selling on day `i`
                profit = max(profit, prices[i] + max_buy_profit)
                dp[i] = max(dp[i - 1], profit)

        return dp[-1]


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.maxProfit(2, [2,4,1]))        # Output: 2
    print(solution.maxProfit(2, [3,2,6,5,0,3]))  # Output: 7
    print(solution.maxProfit(3, [1,2,4,2,5,7,2,4,9,0]))  # Output: 13

    # test
    print(solution.maxProfit(2, [3,3,5,0,0,3,1,4]))  # Output: 6
    print(solution.maxProfit(2, [1,2,3,4,5]))        # Output: 4
    print(solution.maxProfit(2, [7,6,4,3,1]))        # Output: 0