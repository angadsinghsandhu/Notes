# COIN CHANGE

# Problem number: 322
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/coin-change/

from typing import List

class Solution:
    """
    This problem requires finding the minimum number of coins needed to make up a given amount.
    We can solve this using a dynamic programming approach with a 1D DP array. The idea is to keep 
    track of the minimum number of coins required for every amount from 0 up to the given amount.
    For each coin, we iterate over the possible amounts and update the DP array to reflect the minimum 
    coins needed.

    T.C. : O(n * amount)
    S.C. : O(amount)

    Input:
        - coins : List[int] : list of coin denominations
        - amount : int : total amount to be made

    Output:
        - int : minimum number of coins needed, or -1 if the amount cannot be made
    """
    def coinChange(self, coins: List[int], amount: int) -> int:
        # initialize DP array with a large number (infinity)
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        # iterate over each coin
        for coin in coins:
            # update DP array for each amount from coin to the target amount
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
        
        # return the result for the target amount, or -1 if it is still infinity
        return dp[amount] if dp[amount] != float('inf') else -1

# Sample Inputs
coins = [1, 2, 5]
amount = 11

# Expected Output : 3
print(Solution().coinChange(coins, amount))