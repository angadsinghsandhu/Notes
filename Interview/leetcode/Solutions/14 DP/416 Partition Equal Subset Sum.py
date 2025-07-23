# PARTITION EQUAL SUBSET SUM

# Problem number: 416
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/partition-equal-subset-sum/

from typing import List

class Solution:
    """
    This problem involves determining if an array can be partitioned into two subsets with equal sums. 
    We can solve this problem using a 1D DP array where `dp[j]` represents whether a subset with sum `j` 
    can be achieved. We will iterate over the elements of the array and update the DP array to reflect 
    possible subset sums.

    T.C. : O(n * sum/2)
    S.C. : O(sum/2)

    Input:
        - nums : List[int] : list of integers

    Output:
        - bool : True if the array can be partitioned into two subsets with equal sum, otherwise False
    """
    def canPartition(self, nums: List[int]) -> bool:
        total_sum = sum(nums)
        
        # If the total sum is odd, it cannot be partitioned into two equal subsets
        if total_sum % 2 != 0:
            return False
        
        target = total_sum // 2
        
        # initialize DP array with False and set dp[0] to True
        dp = [False] * (target + 1)
        dp[0] = True
        
        # iterate over each number
        for num in nums:
            # update DP array for each possible sum from target down to the number
            for j in range(target, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]
        
        # return the result for the target sum
        return dp[target]

# Sample Inputs
nums = [1, 5, 11, 5]

# Expected Output : True
print(Solution().canPartition(nums))