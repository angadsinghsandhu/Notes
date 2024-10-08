# PRODUCT OF ARRAY EXCEPT SELF

# Problem number: 238
# Difficulty: Medium
# Tags: Array, Prefix Product, Suffix Product
# Link: https://leetcode.com/problems/product-of-array-except-self/

from typing import List

class Solution:
    """
    This problem requires constructing an array such that each element in the output
    is the product of all the elements in the input array except the one at the same index.
    
    The constraints specify that the solution should be in O(n) time and without division.
    
    We'll use two passes over the array:
    1. In the first pass, we'll calculate the prefix product for each element.
    2. In the second pass, we'll calculate the suffix product and update the output array.
    
    This ensures that we meet the O(n) time complexity.
    """

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Approach:
        1. Calculate prefix products for each element.
        2. Calculate suffix products while updating the result in the same array.
        
        T.C. : O(n), where n is the number of elements in nums
        S.C. : O(1), no extra space used apart from the output array
        """
        n = len(nums)
        result = [1] * n  # Initialize the result array with 1's

        # Step 1: Calculate the prefix product for each element
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]

        # Step 2: Calculate the suffix product and update the result array
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]

        return result

# Best Method: This method optimizes space complexity by using the result array for both prefix and suffix products.

# Sample Inputs for Testing
print(Solution().productExceptSelf([1, 2, 3, 4]))  # Output should be [24, 12, 8, 6]
print(Solution().productExceptSelf([-1, 1, 0, -3, 3]))  # Output should be [0, 0, 9, 0, 0]
