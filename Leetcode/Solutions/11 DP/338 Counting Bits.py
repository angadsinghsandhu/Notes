# COUNTING BITS

# Problem number: 338
# Difficulty: Easy
# Tags: Dynamic Programming, Bit Manipulation
# link: https://leetcode.com/problems/counting-bits/

from typing import List

class Solution:
    """
    This problem requires counting the number of 1's in the binary representation of numbers 
    from 0 to n. We can solve this efficiently using a dynamic programming approach by leveraging 
    the relationship between the numbers. Specifically, the number of 1's in the binary 
    representation of a number i can be derived from i // 2 (right shift) plus the least significant bit of i.

    T.C. : O(n)
    S.C. : O(n)

    Input:
        - n : int : the maximum number for which to count the bits

    Output:
        - List[int] : array where each element represents the number of 1's in the binary representation of i
    """
    def countBits(self, n: int) -> List[int]:
        # initialize the DP array with zeros
        dp = [0] * (n + 1)
        
        # fill the DP array based on the relationship
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        
        # return the filled DP array
        return dp

# Sample Inputs
n = 5

# Expected Output : [0,1,1,2,1,2]
print(Solution().countBits(n))