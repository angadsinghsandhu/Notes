# CLIMBING STAIRS

# Problem number: 70
# Difficulty: Easy
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/climbing-stairs/

class Solution:
    """
    This problem is about finding the number of distinct ways to climb to the top of a staircase
    where each time you can either climb 1 or 2 steps. This can be solved using dynamic programming.
    The key observation is that the number of ways to reach the nth step is the sum of the number of
    ways to reach the (n-1)th step and the (n-2)th step. This is analogous to the Fibonacci sequence.

    T.C. : O(n)
    S.C. : O(1)

    Input:
        - n : int : number of steps to reach the top

    Output:
        - int : number of distinct ways to reach the top
    """
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        # Initialize variables for the first two steps
        prev2, prev1 = 1, 2
        
        # Iterate from the 3rd step up to the nth step
        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2 = prev1
            prev1 = current
        
        # Return the final value which represents the number of ways to reach the nth step
        return prev1

# Sample Inputs
n = 3

# Expected Output : 3
print(Solution().climbStairs(n))