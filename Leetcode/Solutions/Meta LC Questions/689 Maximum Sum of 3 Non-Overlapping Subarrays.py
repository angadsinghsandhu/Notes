# MAXIMUM SUM OF 3 NON-OVERLAPPING SUBARRAYS

# Problem number: 689
# Difficulty: Hard
# Tags: Array, Dynamic Programming, Sliding Window
# Link: https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/

from typing import List

class Solution:
    """
    This problem requires finding three non-overlapping subarrays of size k with maximum sum.
    The solution uses dynamic programming and sliding window technique to calculate the 
    maximum sum at each possible position, and then tracks the optimal indices for the result.

    We will:
    1. Calculate the sum of every possible subarray of length k using sliding window.
    2. Use dynamic programming to track the best subarrays ending before each position and
       starting after each position to ensure non-overlapping.
    3. Iterate through the middle subarray and combine the best from the left and right 
       subarrays to maximize the sum.

    T.C.: O(n) where n is the length of the input array.
    S.C.: O(n) for storing the subarray sums and dynamic programming arrays.
    """

    def maxSumOfThreeSubarrays(self, nums: List[int], k: int) -> List[int]:
        # Step 1: Calculate the sum of every subarray of size k
        n = len(nums)
        sums = [0] * (n - k + 1)
        curr_sum = sum(nums[:k])
        sums[0] = curr_sum
        for i in range(1, len(sums)):
            curr_sum += nums[i + k - 1] - nums[i - 1]
            sums[i] = curr_sum

        # Step 2: Precompute best left and right subarray indices
        left = [0] * len(sums)
        right = [0] * len(sums)
        
        # Find the best left index for each position
        best_left = 0
        for i in range(len(sums)):
            if sums[i] > sums[best_left]:
                best_left = i
            left[i] = best_left

        # Find the best right index for each position
        best_right = len(sums) - 1
        for i in range(len(sums) - 1, -1, -1):
            if sums[i] >= sums[best_right]:  # use >= to prefer lexicographically smaller
                best_right = i
            right[i] = best_right

        # Step 3: Find the best combination of left, middle, and right
        result = [-1, -1, -1]
        max_sum = 0
        for j in range(k, len(sums) - k):
            i, l = left[j - k], right[j + k]
            total = sums[i] + sums[j] + sums[l]
            if total > max_sum:
                max_sum = total
                result = [i, j, l]

        return result

# Best Method: Sliding Window combined with Dynamic Programming provides an efficient solution to the problem.
