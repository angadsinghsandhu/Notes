# FIBONACCI NUMBER

# Problem number: 509
# Difficulty: Easy
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/fibonacci-number/

class Solution:
    """
    The Fibonacci sequence is defined such that each number is the sum of the two preceding ones, starting 
    from 0 and 1. This problem asks us to compute the nth Fibonacci number. We can solve this problem 
    using dynamic programming to avoid redundant calculations. We will store the Fibonacci numbers 
    in a 1D DP array, building up from the base cases.

    T.C. : O(n)
    S.C. : O(n)

    Input:
        - n : int : index in the Fibonacci sequence

    Output:
        - int : nth Fibonacci number
    """
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        # initialize DP array
        dp = [0] * (n + 1)
        dp[0] = 0
        dp[1] = 1
        
        # fill the DP array for Fibonacci sequence
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        # return the nth Fibonacci number
        return dp[n]

# Sample Inputs
n = 4

# Expected Output : 3
print(Solution().fib(n))