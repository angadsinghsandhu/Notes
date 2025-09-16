# TODO

### **File:** `Leetcode/Solutions/122_Best_Time_to_Buy_and_Sell_Stock_II.py`

"""
Problem Number: 122
Problem Name: Best Time to Buy and Sell Stock II
Difficulty: Medium
Tags: Array, Greedy, Dynamic Programming
Company (Frequency): Amazon (98)
Leetcode Link: <https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/>

DESCRIPTION

You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.

On each day, you may decide to buy and/or sell the stock. You can only hold at most **one share** of the stock at any time. However, you can buy it then immediately sell it on the same day.

Find and return the **maximum profit** you can achieve.

---

#### Example 1:
**Input:**
```plaintext
prices = [7,1,5,3,6,4]
```
**Output:**
```plaintext
7
```
**Explanation:**  
- Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = `5 - 1 = 4`
- Buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = `6 - 3 = 3`
- Total profit = `4 + 3 = 7`

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
- Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = `5 - 1 = 4`
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
- There is no way to make a positive profit, so we never buy the stock.
- Maximum profit = `0`

#### Constraints:
- `1 <= prices.length <= 3 * 10^4`
- `0 <= prices[i] <= 10^4`
"""

class Solution:
    """
    Thought Process:
    - We can take advantage of every increasing sequence in prices.
    - Instead of finding peaks and valleys separately, we can accumulate profit by summing up all positive price differences.
    - This approach is greedy and guarantees maximum profit.

    Input:
        prices: List[int] - List of stock prices per day.

    Output:
        int - The maximum profit possible.
    """

    def maxProfit(self, prices: list[int]) -> int:
        """
        Approach:
        - Traverse the array and accumulate profit for every increase in price.
        - If prices[i] > prices[i-1], add the difference to total profit.
        
        T.C.: O(n) - Single pass through the array.
        S.C.: O(1) - Constant extra space.
        """
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
        return profit


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.maxProfit([7,1,5,3,6,4]))  # Output: 7
    print(solution.maxProfit([1,2,3,4,5]))    # Output: 4
    print(solution.maxProfit([7,6,4,3,1]))    # Output: 0