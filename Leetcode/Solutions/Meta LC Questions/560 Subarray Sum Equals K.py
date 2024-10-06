# SUBARRAY SUM EQUALS K

# Problem number: 560
# Difficulty: Medium
# Tags: Array, Hash Map, Prefix Sum
# Link: https://leetcode.com/problems/subarray-sum-equals-k/

from typing import List

class Solution:
    """
    This problem requires finding the total number of continuous subarrays 
    whose sum equals to a given value k. 

    We will use the Prefix Sum approach along with a Hash Map to optimize the solution.
    The basic idea is to compute the cumulative sum (prefix sum) and check 
    if (current_sum - k) has been seen before. If so, the difference between them forms a valid subarray.

    Time Complexity: O(n), as we iterate through the array once.
    Space Complexity: O(n), due to the hash map storing prefix sums.
    """

    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Optimized approach using a hash map to store prefix sums.
        
        T.C. : O(n), where n is the number of elements in the array
        S.C. : O(n), due to the hash map storing prefix sums
        """
        count = 0
        prefix_sum = 0
        prefix_sums = {0: 1}  # Dictionary to store (prefix_sum, frequency)

        for num in nums:
            prefix_sum += num
            
            # Check if (prefix_sum - k) exists in the map
            if (prefix_sum - k) in prefix_sums:
                count += prefix_sums[prefix_sum - k]

            # Update the prefix_sums map
            prefix_sums[prefix_sum] = prefix_sums.get(prefix_sum, 0) + 1

        return count

# Best Method: The Hash Map approach is the most optimal solution for this problem.

# Example Test Cases
nums1 = [1, 1, 1]
k1 = 2
print(Solution().subarraySum(nums1, k1))  # Expected Output: 2

nums2 = [1, 2, 3]
k2 = 3
print(Solution().subarraySum(nums2, k2))  # Expected Output: 2
