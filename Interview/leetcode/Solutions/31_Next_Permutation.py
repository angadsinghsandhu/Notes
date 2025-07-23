# TODO: Revit
# File: Leetcode/Solutions/Array/31_Next_Permutation.py

"""
Problem Number: 31
Problem Name: Next Permutation
Difficulty: Medium
Tags: Array, Two Pointers
Company (Frequency): Not explicitly stated, but common in top tech companies.
Leetcode Link: <https://leetcode.com/problems/next-permutation/description/>

DESCRIPTION

A permutation of an array of integers is an arrangement of its members into a sequence or linear order.
For example, for `arr = [1,2,3]`, the following are all the permutations of `arr`: `[1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1]`.
The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).
For example, the next permutation of `arr = [1,2,3]` is `[1,3,2]`.
Similarly, the next permutation of `arr = [2,3,1]` is `[3,1,2]`.
While the next permutation of `arr = [3,2,1]` is `[1,2,3]` because `[3,2,1]` does not have a lexicographical larger rearrangement.
Given an array of integers `nums`, find the next permutation of `nums`.
The replacement must be in place and use only constant extra memory.

---

#### Example 1:

Input:
nums = [1,2,3]

Output:
[1,3,2]

---

#### Example 2:

Input:
nums = [3,2,1]

Output:
[1,2,3]

---

#### Example 3:

Input:
nums = [1,1,5]

Output:
[1,5,1]

---

#### Constraints:

- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
"""

from typing import List

class Solution:
    """
    Thought Process:
    To find the next lexicographically greater permutation, we need to make the smallest possible change to the array to increase its value. This typically involves modifying the rightmost part of the array.

    The algorithm follows these steps:

    1.  **Find the first decreasing element from the right:**
        Iterate from the second-to-last element (`n-2`) down to the first element (`0`).
        Find the first index `i` such that `nums[i] < nums[i+1]`.
        This `nums[i]` is the "pivot" element that we need to increase.
        If no such `i` is found (meaning the array is sorted in descending order, e.g., `[3,2,1]`), then this is the last permutation. In this case, we simply reverse the entire array to get the lowest possible order (ascending order).

    2.  **Find the smallest element to swap with the pivot:**
        If a pivot `i` is found, iterate from the last element (`n-1`) down to `i+1`.
        Find the first index `j` such that `nums[j] > nums[i]`.
        This `nums[j]` is the smallest element on the right of `i` that is greater than `nums[i]`. We want to swap `nums[i]` with the smallest possible element from its right that is still larger than `nums[i]` to make the smallest increase.

    3.  **Swap the pivot and the found element:**
        Swap `nums[i]` and `nums[j]`.

    4.  **Reverse the suffix:**
        Reverse the sub-array `nums[i+1:]`. This step is crucial because after swapping `nums[i]`, the elements to its right are still in descending order. To get the *next* permutation, we need to make this suffix as small as possible, which is achieved by sorting it in ascending order (which can be done by reversing since it was in descending order).

    Example: `[1, 5, 8, 4, 7, 6, 5, 3, 1]`
    1. Find `i`: Iterate from right. `1 < 3` (false), `3 < 5` (false), `5 < 6` (false), `6 < 7` (false), `7 < 4` (false).
       `4 < 8` (false). Ah, `nums[3]=4`. `nums[4]=7`. So, `i=3` (pivot is 4).
    2. Find `j`: Iterate from right (`n-1`) down to `i+1`.
       Find smallest element greater than `nums[3]` (which is 4) in `[7,6,5,3,1]`.
       `nums[8]=1` (no), `nums[7]=3` (no), `nums[6]=5` (yes, 5 > 4). So, `j=6`.
    3. Swap `nums[3]` and `nums[6]`: `[1, 5, 8, 5, 7, 6, 4, 3, 1]`
    4. Reverse suffix `nums[i+1:]` (i.e., `nums[4:]`): `[7, 6, 4, 3, 1]` becomes `[1, 3, 4, 6, 7]`
       Final array: `[1, 5, 8, 5, 1, 3, 4, 6, 7]`

    This algorithm works because finding the first decreasing element from the right guarantees that the prefix `nums[0...i]` is the longest possible prefix that remains unchanged, or undergoes the smallest possible change at `nums[i]`. The subsequent swap and reverse ensure the smallest possible increase in the overall number.

    Input:
        nums: List[int] - The array of integers to be modified in-place.

    Output:
        None - The function modifies the input array directly.
    """

    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)

        # Step 1: Find the first decreasing element from the right
        i = n - 2
        while i >= 0 and nums[i] >= nums[i+1]:
            i -= 1

        # If such an element exists (i >= 0), it's not the largest permutation
        if i >= 0:
            # Step 2: Find the smallest element to the right of nums[i] that is greater than nums[i]
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            
            # Step 3: Swap nums[i] and nums[j]
            nums[i], nums[j] = nums[j], nums[i]
        
        # Step 4: Reverse the suffix starting from i + 1
        # This covers two cases:
        # a) If a pivot was found (i >= 0), it sorts the suffix in ascending order to make it lexicographically smallest.
        # b) If no pivot was found (i < 0, meaning array was sorted descending), it reverses the entire array
        #    to get the ascending order, which is the "lowest possible order".
        left = i + 1
        right = n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [1,2,3]
    expected1 = [1,3,2]
    nums1_copy = list(nums1) # Make a copy for printing original input
    solution.nextPermutation(nums1)
    print(f"Input: {nums1_copy} -> Output: {nums1} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 2
    nums2 = [3,2,1]
    expected2 = [1,2,3]
    nums2_copy = list(nums2)
    solution.nextPermutation(nums2)
    print(f"Input: {nums2_copy} -> Output: {nums2} (Expected: {expected2})")
    print("-" * 20)

    # Test Case 3
    nums3 = [1,1,5]
    expected3 = [1,5,1]
    nums3_copy = list(nums3)
    solution.nextPermutation(nums3)
    print(f"Input: {nums3_copy} -> Output: {nums3} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Single element
    nums4 = [1]
    expected4 = [1]
    nums4_copy = list(nums4)
    solution.nextPermutation(nums4)
    print(f"Input: {nums4_copy} -> Output: {nums4} (Expected: {expected4})")
    print("-" * 20)

    # Additional Test Case: Example from thought process
    nums5 = [1,5,8,4,7,6,5,3,1]
    expected5 = [1,5,8,5,1,3,4,6,7]
    nums5_copy = list(nums5)
    solution.nextPermutation(nums5)
    print(f"Input: {nums5_copy} -> Output: {nums5} (Expected: {expected5})")
    print("-" * 20)

    # Additional Test Case: Two elements
    nums6 = [1,3]
    expected6 = [3,1]
    nums6_copy = list(nums6)
    solution.nextPermutation(nums6)
    print(f"Input: {nums6_copy} -> Output: {nums6} (Expected: {expected6})")
    print("-" * 20)

    nums7 = [1,5,1]
    expected7 = [5,1,1]
    nums7_copy = list(nums7)
    solution.nextPermutation(nums7)
    print(f"Input: {nums7_copy} -> Output: {nums7} (Expected: {expected7})")
    print("-" * 20)