# COIN CHANGE II

# Problem number: 518
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/coin-change-ii/

from typing import List

class Solution:
    """
    This problem is about counting the number of combinations to make up a given amount using a set
    of coin denominations. We use a 1D DP array where `dp[i]` represents the number of ways to make 
    the amount `i`. For each coin, we iterate through possible amounts and update the DP array based on 
    the number of ways to form amounts including that coin.

    T.C. : O(n * amount)
    S.C. : O(amount)

    Input:
        - coins : List[int] : list of coin denominations
        - amount : int : total amount to be made

    Output:
        - int : number of combinations to make the amount, or 0 if the amount cannot be made
    """
    def change(self, amount: int, coins: List[int]) -> int:
        # initialize DP array with 0s and set dp[0] to 1
        dp = [0] * (amount + 1)
        dp[0] = 1
        
        # iterate over each coin
        for coin in coins:
            # update DP array for each amount from coin to the target amount
            for x in range(coin, amount + 1):
                dp[x] += dp[x - coin]
        
        # return the result for the target amount
        return dp[amount]

# Sample Inputs
amount = 5
coins = [1, 2, 5]

# Expected Output : 4
print(Solution().change(amount, coins))