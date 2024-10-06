# NEXT PERMUTATION

# Problem number: 31
# Difficulty: Medium
# Tags: Array, Two Pointers, Greedy
# Link: https://leetcode.com/problems/next-permutation/

from typing import List

class Solution:
    """
    The goal is to rearrange the numbers in the list to get the next lexicographically larger permutation. 
    If no such permutation exists, rearrange the list to the lowest possible order (i.e., sorted in ascending order).
    
    We use a greedy approach where we:
    1. Identify the first decreasing element from the end.
    2. Swap it with the next larger element.
    3. Reverse the elements after the swap position to get the smallest lexicographical order.

    This solution modifies the list in-place and only uses constant extra memory.
    """

    def nextPermutation(self, nums: List[int]) -> None:
        """
        Rearranges the list nums in-place to the next lexicographical permutation.
        
        T.C. : O(n), where n is the length of the list.
        S.C. : O(1), in-place solution with constant extra memory.
        """
        # Step 1: Find the first decreasing element from the end
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        # Step 2: If we find such an element, find the next larger element to swap
        if i >= 0:
            j = len(nums) - 1
            while nums[j] <= nums[i]:
                j -= 1
            # Swap the elements
            nums[i], nums[j] = nums[j], nums[i]

        # Step 3: Reverse the elements after the swapped element
        left, right = i + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

# Best Method: The above solution uses a single traversal to find the first decreasing element and another to swap it with the next larger element. Finally, reversing the elements guarantees the next permutation.

# Sample Inputs for Testing
nums1 = [1, 2, 3]
Solution().nextPermutation(nums1)
print(nums1)  # Expected output: [1, 3, 2]

nums2 = [3, 2, 1]
Solution().nextPermutation(nums2)
print(nums2)  # Expected output: [1, 2, 3]

nums3 = [1, 1, 5]
Solution().nextPermutation(nums3)
print(nums3)  # Expected output: [1, 5, 1]
