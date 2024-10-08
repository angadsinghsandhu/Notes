# CONTINUOUS SUBARRAY SUM

# Problem number: 523
# Difficulty: Medium
# Tags: Array, Hash Table, Prefix Sum, Math
# Link: https://leetcode.com/problems/continuous-subarray-sum/

from typing import List

class Solution:
    """
    This problem requires checking if there exists a continuous subarray of at least size 2 
    such that the sum of its elements is a multiple of a given integer k.
    
    We will solve this using the prefix sum approach and a hash map to efficiently 
    track modulo operations.
    """

    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        """
        Time Complexity: O(n), where n is the length of the array
        Space Complexity: O(min(n, k)), as we are using a hash map to store remainders.
        """

        # HashMap to store (remainder, index)
        remainder_map = {0: -1}  # Initialize with remainder 0 at index -1 (for the case when sum is a multiple of k)
        current_sum = 0

        for i, num in enumerate(nums):
            current_sum += num

            # We only care about the remainder when current_sum is divided by k
            if k != 0:
                current_sum %= k
            
            # If this remainder has been seen before and the subarray length is at least 2
            if current_sum in remainder_map:
                if i - remainder_map[current_sum] > 1:  # Subarray length check
                    return True
            else:
                remainder_map[current_sum] = i
        
        return False

# Best Method: Using prefix sum and modulo with a hash map for efficient look-up of remainders.
