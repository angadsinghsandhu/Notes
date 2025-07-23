# TWO SUM

# Problem number: 1
# Difficulty: Easy
# Tags: Array, Hash Map
# Link: https://leetcode.com/problems/two-sum/

from typing import List

class Solution:
    """
    This problem requires finding two indices such that the numbers at those indices in the array add up to the target.
    
    The optimal solution uses a hash map to store the complement of the current number as we iterate through the list.
    If the complement is found in the hash map, we return the indices.
    
    We will implement two approaches:
    1. Brute Force Approach
    2. Hash Map Approach (Optimal)
    """

    def twoSum_brute_force(self, nums: List[int], target: int) -> List[int]:
        """
        Brute force approach to find two indices.
        
        T.C. : O(n^2) where n is the length of the array
        S.C. : O(1)
        """
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    def twoSum_hash_map(self, nums: List[int], target: int) -> List[int]:
        """
        Optimal approach using a hash map.
        
        T.C. : O(n) where n is the length of the array
        S.C. : O(n) due to the use of a hash map
        """
        hash_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hash_map:
                return [hash_map[complement], i]
            hash_map[num] = i
        return []

# Best Method: The hash map approach is optimal with O(n) time complexity, as it checks each element once.
