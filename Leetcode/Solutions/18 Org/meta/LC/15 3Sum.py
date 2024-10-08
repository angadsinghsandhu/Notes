# 3Sum

# Problem number: 15
# Difficulty: Medium
# Tags: Array, Two Pointers, Sorting
# Link: https://leetcode.com/problems/3sum/

from typing import List

class Solution:
    """
    This problem requires finding all unique triplets in the array that sum to zero. 
    The array can contain both positive and negative numbers. We must ensure that 
    triplets are unique, and indices cannot repeat.
    
    We will implement two methods:
    1. Sorting + Two Pointers Approach (Optimal)
    2. Brute Force Approach (Less Optimal for comparison)
    """

    def threeSum_optimal(self, nums: List[int]) -> List[List[int]]:
        """
        Optimal approach using sorting and two-pointer technique.
        
        T.C. : O(n^2) where n is the length of the input array
        S.C. : O(1) ignoring the output space (in-place sorting)
        """
        nums.sort()  # First, sort the array to allow for two-pointer approach
        result = []
        n = len(nums)

        for i in range(n):
            # Skip duplicates for the first element
            if i > 0 and nums[i] == nums[i-1]:
                continue

            # Now apply two-pointer approach
            left, right = i + 1, n - 1
            while left < right:
                total_sum = nums[i] + nums[left] + nums[right]

                if total_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    # Skip duplicates for left and right
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total_sum < 0:
                    left += 1
                else:
                    right -= 1

        return result

    def threeSum_bruteforce(self, nums: List[int]) -> List[List[int]]:
        """
        Brute-force approach using three nested loops.
        
        T.C. : O(n^3) where n is the length of the input array
        S.C. : O(n) for storing the result
        
        This approach is provided for comparison but is not optimal for large inputs.
        """
        nums.sort()  # Sorting helps reduce duplicate triplets
        result = []
        n = len(nums)

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplet = sorted([nums[i], nums[j], nums[k]])
                        if triplet not in result:
                            result.append(triplet)

        return result

# Best Method: The two-pointer approach is the most optimal with O(n^2) complexity.

# Sample Inputs for Testing
nums1 = [-1, 0, 1, 2, -1, -4]
nums2 = [0, 1, 1]
nums3 = [0, 0, 0]

# Testing Optimal Method
print(Solution().threeSum_optimal(nums1))  # Output: [[-1, -1, 2], [-1, 0, 1]]
print(Solution().threeSum_optimal(nums2))  # Output: []
print(Solution().threeSum_optimal(nums3))  # Output: [[0, 0, 0]]

# Testing Brute Force Method
print(Solution().threeSum_bruteforce(nums1))  # Output: [[-1, -1, 2], [-1, 0, 1]]
