# MAXIMUM SUBARRAY

# Problem number: 53
# Difficulty: Medium
# Tags: Dynamic Programming, Greedy
# link: https://leetcode.com/problems/maximum-subarray/

from typing import List

class Solution:
    """
    This problem is about finding the subarray with the largest sum in a given integer array.
    The optimal solution can be achieved using a dynamic programming approach known as Kadane's Algorithm.
    The idea is to iterate through the array, keeping track of the maximum subarray sum ending at each position.
    If the sum becomes negative, we reset it to the current element, as a subarray starting from this element would have a higher sum.
    The maximum sum found during the iteration is the answer.

    T.C. : O(n)
    S.C. : O(1)

    Input:
        - nums : List[int] : list of integers

    Output:
        - int : the largest sum of a subarray
    """
    def maxSubArray(self, nums: List[int]) -> int:
        # Initialize the current sum and maximum sum with the first element
        current_sum = max_sum = nums[0]
        
        # Iterate over the array starting from the second element
        for num in nums[1:]:
            # Update the current sum by including the current element or starting fresh from the current element
            current_sum = max(num, current_sum + num)
            # Update the maximum sum if the current sum is larger
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
# Sample Inputs
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

# Expected Output : 6
print(Solution().maxSubArray(nums))