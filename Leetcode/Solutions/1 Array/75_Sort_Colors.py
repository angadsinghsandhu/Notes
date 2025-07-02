# File: Leetcode/Solutions/LeetCode/75_Sort_Colors.py

"""
Problem Number: 75
Problem Name: Sort Colors
Difficulty: Medium
Tags: Array, Two Pointers, Sorting
Company (Frequency): (premium)
Leetcode Link: https://leetcode.com/problems/sort-colors/

DESCRIPTION

Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent,  
with the colors in the order red, white, and blue.

We use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.  
You must solve this problem without using the library's sort function.

---

#### Example 1:
Input:
nums = [2,0,2,1,1,0]

Output:
[0,0,1,1,2,2]

#### Example 2:

Input:
nums = [2,0,1]

Output:
[0,1,2]

#### Constraints:

* `n == nums.length`
* `1 <= n <= 300`
* `nums[i]` is either `0`, `1`, or `2`.

#### Follow up:

Could you come up with a one-pass algorithm using only constant extra space?
"""

from typing import List

class Solution:
    """
    Thought Process:
    - Brute Force: Count the occurrences of each color (0,1,2) then overwrite the array in two passes.
    - Optimized: Use the Dutch National Flag algorithm (three pointers) to sort in one pass with O(1) extra space.
    """

    def brute_force(self, nums: List[int]) -> None:
        """
        Approach:
        - First pass: count how many 0s, 1s, and 2s.
        - Second pass: overwrite the array with the counted number of 0s, then 1s, then 2s.

        T.C.: O(n)
        S.C.: O(1) extra
        """
        count0 = count1 = count2 = 0
        for num in nums:
            if num == 0:
                count0 += 1
            elif num == 1:
                count1 += 1
            else:
                count2 += 1

        idx = 0
        for _ in range(count0):
            nums[idx] = 0
            idx += 1
        for _ in range(count1):
            nums[idx] = 1
            idx += 1
        for _ in range(count2):
            nums[idx] = 2
            idx += 1

    def optimized(self, nums: List[int]) -> None:
        """
        Approach:
        - Maintain three pointers: low for next 0, mid for current element, high for next 2.
        - Traverse with mid:
        - If nums[mid] == 0: swap with nums[low], low++, mid++.
        - If nums[mid] == 1: mid++.
        - If nums[mid] == 2: swap with nums[high], high-- (don't mid++, since swapped element needs examination).

        T.C.: O(n)
        S.C.: O(1) extra
        """
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1

if __name__ == "__main__":
    solution = Solution()


# Example 1
arr1 = [2,0,2,1,1,0]
solution.brute_force(arr1)
print(arr1)  # [0,0,1,1,2,2]

arr2 = [2,0,2,1,1,0]
solution.optimized(arr2)
print(arr2)  # [0,0,1,1,2,2]

# Example 2
arr3 = [2,0,1]
solution.brute_force(arr3)
print(arr3)  # [0,1,2]

arr4 = [2,0,1]
solution.optimized(arr4)
print(arr4)  # [0,1,2]