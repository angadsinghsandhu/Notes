# File: Leetcode/Solutions/Amazon/189_Rotate_Array.py

"""
Problem Number: 189
Problem Name: Rotate Array
Difficulty: Medium
Tags: Array, Math, Two Pointers
Company (Frequency): Amazon (95)
Leetcode Link: <https://leetcode.com/problems/rotate-array/description/>

DESCRIPTION

Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.

---

#### Example 1:

Input:
nums = [1,2,3,4,5,6,7], k = 3

Output:
[5,6,7,1,2,3,4]

Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]

---

#### Example 2:

Input:
nums = [-1,-100,3,99], k = 2

Output:
[3,99,-1,-100]

Explanation:
rotate 1 steps to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]

---

#### Constraints:

- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- 0 <= k <= 10^5

#### Follow up:

- Try to come up with as many solutions as you can. There are at least three different ways to solve this problem.
- Could you do it in-place with O(1) extra space?
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires rotating an array to the right by `k` steps.
    - A key observation is that `k` can be larger than the length of the array. The effective rotation is `k % len(s)`.
    - There are several ways to approach this, including using an extra array for a straightforward solution, or in-place algorithms like the reversal method or cyclic replacements to meet the O(1) space complexity challenge.

    Input:
        nums: List[int] - The array of integers.
        k: int - The number of steps to rotate.

    Output:
        None - The function modifies the input array in-place.
    """

    def extra_array_solution(self, nums: List[int], k: int) -> None:
        """
        Approach:
        - Use an auxiliary array to store the rotated elements.
        - An element at index `i` moves to index `(i + k) % n`.
        - Copy the elements from the auxiliary array back to the original array.

        T.C.: O(n)
        S.C.: O(n)
        """
        n = len(nums)
        k %= n  # Handle cases where k > n
        if k == 0:
            return

        # Create a new array with the same size
        rotated_nums = [0] * n
        for i in range(n):
            rotated_nums[(i + k) % n] = nums[i]

        # Copy the rotated array back to the original one
        nums[:] = rotated_nums

    def reversal_solution(self, nums: List[int], k: int) -> None:
        """
        Approach:
        - This is an in-place solution with O(1) extra space.
        - First, handle `k` by taking `k % n`.
        - The algorithm consists of three steps:
        1. Reverse the entire array.
        2. Reverse the first `k` elements.
        3. Reverse the remaining `n - k` elements.

        T.C.: O(n)
        S.C.: O(1)
        """
        n = len(nums)
        k %= n
        if k == 0:
            return

        # Helper function to reverse a sub-array
        def reverse(start: int, end: int):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        # Step 1: Reverse the entire array
        reverse(0, n - 1)
        # Step 2: Reverse the first k elements
        reverse(0, k - 1)
        # Step 3: Reverse the remaining n - k elements
        reverse(k, n - 1)

    def cyclic_replacement_solution(self, nums: List[int], k: int) -> None:
        """
        Approach:
        - This is another in-place solution with O(1) extra space.
        - Move elements one by one to their final rotated positions.
        - Start with an element and place it in its correct spot. The element that was there is then moved to its correct spot, and so on.
        - This continues until we return to the starting element, completing a cycle.
        - We must count the number of elements moved to ensure every element is processed, as some `k` and `n` values result in multiple cycles.

        T.C.: O(n)
        S.C.: O(1)
        """
        n = len(nums)
        k %= n
        if k == 0:
            return

        count = 0  # Number of elements placed
        start_index = 0
        while count < n:
            current_index = start_index
            prev_val = nums[start_index]

            while True:
                next_index = (current_index + k) % n
                # Swap the value
                temp = nums[next_index]
                nums[next_index] = prev_val
                prev_val = temp

                current_index = next_index
                count += 1

                if current_index == start_index:
                    break  # Cycle complete
            
            start_index += 1

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

# Test Case 1
nums1 = [1, 2, 3, 4, 5, 6, 7]
k1 = 3

# Using extra array solution
nums1_test = list(nums1)
solution.extra_array_solution(nums1_test, k1)
print(f"Extra Array Solution for {nums1} with k={k1}: {nums1_test}")  # Output: [5, 6, 7, 1, 2, 3, 4]

# Using reversal solution
nums1_test = list(nums1)
solution.reversal_solution(nums1_test, k1)
print(f"Reversal Solution for {nums1} with k={k1}: {nums1_test}")    # Output: [5, 6, 7, 1, 2, 3, 4]

# Using cyclic replacement solution
nums1_test = list(nums1)
solution.cyclic_replacement_solution(nums1_test, k1)
print(f"Cyclic Solution for {nums1} with k={k1}: {nums1_test}")      # Output: [5, 6, 7, 1, 2, 3, 4]
print("-" * 20)

# Test Case 2
nums2 = [-1, -100, 3, 99]
k2 = 2

# Using reversal solution as the primary in-place method
nums2_test = list(nums2)
solution.reversal_solution(nums2_test, k2)
print(f"Reversal Solution for {nums2} with k={k2}: {nums2_test}")    # Output: [3, 99, -1, -100]