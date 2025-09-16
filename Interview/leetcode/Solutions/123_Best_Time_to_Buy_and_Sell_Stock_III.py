# File: Leetcode/Solutions/123_Best_Time_to_Buy_and_Sell_Stock_III.py

"""
Problem Number: 123
Problem Name: Best Time to Buy and Sell Stock III
Difficulty: Hard
Tags: Array, Dynamic Programming
Company (Frequency): Amazon (95)
Leetcode Link: <https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/>

DESCRIPTION

You are given an array `prices` where `prices[i]` represents the stock price on the `i-th` day.

You are allowed to complete at most **two transactions** (a transaction consists of buying and selling one stock).

**Note:**
- You **cannot** engage in multiple transactions at the same time (i.e., you must sell the stock before buying again).
- The goal is to determine the maximum profit that can be made through **at most** two transactions.

---

#### Example 1:
**Input:**
```plaintext
prices = [3,3,5,0,0,3,1,4]
```
**Output:**
```plaintext
6
```
**Explanation:**  
- Buy on day 4 (price = 0), sell on day 6 (price = 3), profit = `3 - 0 = 3`
- Buy on day 7 (price = 1), sell on day 8 (price = 4), profit = `4 - 1 = 3`
- Total profit = `3 + 3 = 6`

#### Example 2:
**Input:**
```plaintext
prices = [1,2,3,4,5]
```
**Output:**
```plaintext
4
```
**Explanation:**  
- Buy on day 1 (price = 1), sell on day 5 (price = 5), profit = `5 - 1 = 4`
- No second transaction needed.
- Total profit = `4`

#### Example 3:
**Input:**
```plaintext
prices = [7,6,4,3,1]
```
**Output:**
```plaintext
0
```
**Explanation:**  
- No transactions can be made since prices are decreasing.

#### Constraints:
- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^5`
"""

class Solution:
    """
    Thought Process:
    - We need to find the maximum profit from **at most** two transactions.
    - The **Dynamic Programming** approach efficiently tracks profit across **four states**:
      1. **First Buy (`f1`)**: Buying at the lowest price.
      2. **First Sell (`f2`)**: Selling to maximize first profit.
      3. **Second Buy (`f3`)**: Buying again while considering the first profit.
      4. **Second Sell (`f4`)**: Selling again to maximize total profit.
    - We iterate through the `prices` array and update these four states at each step.

    Input:
        prices: List[int] - List of stock prices per day.

    Output:
        int - The maximum profit that can be achieved with at most two transactions.
    """

    def maxProfit_dp(self, prices: list[int]) -> int:
        """
        Approach:
        - **Dynamic Programming** approach using four key states:
          - `f1`: Maximum profit after **first buy**.
          - `f2`: Maximum profit after **first sell**.
          - `f3`: Maximum profit after **second buy**.
          - `f4`: Maximum profit after **second sell**.
        - We iterate through prices, updating `f1`, `f2`, `f3`, and `f4`.

        T.C.: O(n) - Single pass through the array.
        S.C.: O(1) - Constant space used.
        """
        if not prices:
            return 0

        # Initialize the four states
        f1, f2 = float('-inf'), 0
        f3, f4 = float('-inf'), 0

        for price in prices:
            # Update states in the correct order
            f1 = max(f1, 0 - price)      # Buying first stock at minimum cost
            f2 = max(f2, f1 + price)     # Selling first stock at maximum profit
            f3 = max(f3, f2 - price)     # Buying second stock after first profit
            f4 = max(f4, f3 + price)     # Selling second stock at maximum profit

        return f4  # The maximum profit possible with up to two transactions
    
    def maxProfit_divide_and_conquer(self, prices: list[int]) -> int:
        """
        Approach:
        - **Divide and Conquer** approach to find the maximum profit.
        - We divide the array into two halves and find the maximum profit for each half.
        - We also find the maximum profit by buying on the left and selling on the right.
        - The maximum profit is the maximum of the three values.
        
        T.C.: O(n) - Single pass through the array.
        S.C.: O(1) - Constant space used.
        """

        n = len(prices)
        if n == 0:
            return 0
        
        leftMaxProfit, rightMaxProfit = [0] * n, [0] * n

        # Find the maximum profit from left to right
        minPrice = prices[0]
        for i in range(1, n):
            leftMaxProfit[i] = max(leftMaxProfit[i - 1], prices[i] - minPrice)
            minPrice = min(minPrice, prices[i])

        # Find the maximum profit from right to left
        maxPrice = prices[n - 1]
        for i in range(n - 2, -1, -1):
            rightMaxProfit[i] = max(rightMaxProfit[i + 1], maxPrice - prices[i])
            maxPrice = max(maxPrice, prices[i])

        # Find the maximum profit by buying on the left and selling on the right
        maxProfit = rightMaxProfit[0]
        for i in range(1, n):
            maxProfit = max(maxProfit, leftMaxProfit[i - 1] + rightMaxProfit[i])

        return maxProfit


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.maxProfit([3,3,5,0,0,3,1,4]))  # Output: 6
    print(solution.maxProfit([1,2,3,4,5]))        # Output: 4
    print(solution.maxProfit([7,6,4,3,1]))        # Output: 0