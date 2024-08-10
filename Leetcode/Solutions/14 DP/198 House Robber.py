# HOUSE ROBBER

# Problem number: 198
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/house-robber/

from typing import List

class Solution:
    """
    This problem is about maximizing the amount of money you can rob from a series of houses
    without robbing two adjacent houses. The optimal solution can be found using dynamic
    programming. The idea is to keep track of the maximum money that can be robbed up to each house,
    considering whether to rob the current house or not.

    T.C. : O(n)
    S.C. : O(1)

    Input:
        - nums : List[int] : list representing the amount of money in each house

    Output:
        - int : maximum amount of money that can be robbed without alerting the police
    """
    def rob(self, nums: List[int]) -> int:
        # Edge case: if there are no houses, return 0
        if not nums:
            return 0
        
        # Initialize variables to store the maximum money up to the previous two houses
        prev1, prev2 = 0, 0
        
        # Iterate over each house
        for num in nums:
            # Calculate the maximum money if the current house is robbed or skipped
            temp = max(prev1, prev2 + num)
            prev2 = prev1
            prev1 = temp
        
        # The last calculated value is the answer
        return prev1

# Sample Inputs
nums = [1, 2, 3, 1]

# Expected Output : 4
print(Solution().rob(nums))