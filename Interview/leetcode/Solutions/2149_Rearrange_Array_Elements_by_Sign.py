# File: Leetcode/Solutions/2149_Rearrange_Array_Elements_by_Sign.py

"""
Problem Number: 2149
Problem Name: Rearrange Array Elements by Sign
Difficulty: Medium
Tags: Array, Two Pointers, Simulation
Company (Frequency): Not explicitly stated, but common in top tech companies like Amazon (implied by file path)
Leetcode Link: <https://leetcode.com/problems/rearrange-array-elements-by-sign/description/>

DESCRIPTION

You are given a 0-indexed integer array `nums` of even length consisting of an equal number of positive and negative integers.
You should return the array of nums such that the array follows the given conditions:
1. Every consecutive pair of integers have opposite signs.
2. For all integers with the same sign, the order in which they were present in `nums` is preserved.
3. The rearranged array begins with a positive integer.

Return the modified array after rearranging the elements to satisfy the aforementioned conditions.

---

#### Example 1:

Input:
nums = [3,1,-2,-5,2,-4]

Output:
[3,-2,1,-5,2,-4]

Explanation:
The positive integers in nums are [3,1,2]. The negative integers are [-2,-5,-4].
The only possible way to rearrange them such that they satisfy all conditions is [3,-2,1,-5,2,-4].
Other ways such as [1,-2,2,-5,3,-4], [3,1,2,-2,-5,-4], [-2,3,-5,1,-4,2] are incorrect because they do not satisfy one or more conditions.

---

#### Example 2:

Input:
nums = [-1,1]

Output:
[1,-1]

Explanation:
1 is the only positive integer and -1 the only negative integer in nums.
So nums is rearranged to [1,-1].

---

#### Constraints:

- 2 <= nums.length <= 2 * 10^5
- nums.length is even
- 1 <= |nums[i]| <= 10^5
- nums consists of equal number of positive and negative integers.

It is not required to do the modifications in-place.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires rearranging an array `nums` with an even length and an equal number of positive and negative integers.
    - Key conditions:
        1. Alternate signs (positive, then negative, then positive, etc.).
        2. Preserve the relative order of positive integers among themselves.
        3. Preserve the relative order of negative integers among themselves.
        4. The rearranged array must start with a positive integer.
    - Since it's guaranteed to have an equal number of positive and negative integers and an even length, and starts with positive, the alternating pattern will naturally fill the entire output array.
    - We can achieve this by separating the positive and negative numbers into two lists, preserving their order, and then merging them into a new result array by picking one from each list alternately.

    Input:
        nums: List[int] - The input array of integers.

    Output:
        List[int] - The rearranged array.
    """

    def rearrangeArray(self, nums: List[int]) -> List[int]:
        """
        Approach: Two Pointers / Separate Lists
        - Create two new lists, one for positive numbers (`pos_nums`) and one for negative numbers (`neg_nums`).
        - Iterate through the original `nums` array and append elements to the respective lists, preserving their relative order.
        - Create a `result` array of the same length as `nums`.
        - Use two pointers, `pos_ptr` for `pos_nums` and `neg_ptr` for `neg_nums`, both starting at 0.
        - Iterate through the `result` array's indices:
            - If the current index `i` is even, place the next positive number (`pos_nums[pos_ptr]`) into `result[i]`, and increment `pos_ptr`.
            - If the current index `i` is odd, place the next negative number (`neg_nums[neg_ptr]`) into `result[i]`, and increment `neg_ptr`.
        - Return the `result` array.

        T.C.: O(n) - One pass to separate, one pass to merge.
        S.C.: O(n) - For storing `pos_nums`, `neg_nums`, and `result` array.
        """
        n = len(nums)
        pos_nums = []
        neg_nums = []

        # Separate positive and negative numbers while preserving order
        for num in nums:
            if num > 0:
                pos_nums.append(num)
            else:
                neg_nums.append(num)

        result = [0] * n  # Initialize result array

        pos_idx = 0
        neg_idx = 0

        # Fill the result array according to the conditions
        for i in range(n):
            if i % 2 == 0:  # Even indices get positive numbers
                result[i] = pos_nums[pos_idx]
                pos_idx += 1
            else:           # Odd indices get negative numbers
                result[i] = neg_nums[neg_idx]
                neg_idx += 1
        return result

    def rearrangeArray_optimized_pointers(self, nums: List[int]) -> List[int]:
        """
        Approach: Optimized Two Pointers (Direct Fill)
        - This approach avoids creating intermediate `pos_nums` and `neg_nums` lists explicitly,
          though it still implicitly extracts elements for placement. It directly places elements
          into the `result` array.
        - Initialize `result = [0] * n`.
        - Maintain two pointers for the `result` array: `pos_res_idx` (0, 2, 4...) for positive numbers,
          and `neg_res_idx` (1, 3, 5...) for negative numbers.
        - Iterate through the original `nums` array.
            - If `nums[i]` is positive, place it at `result[pos_res_idx]` and increment `pos_res_idx` by 2.
            - If `nums[i]` is negative, place it at `result[neg_res_idx]` and increment `neg_res_idx` by 2.
        - This preserves order and naturally alternates.

        T.C.: O(n) - Single pass through the input array.
        S.C.: O(n) - For the `result` array. (Since in-place modification is not required, this is acceptable).
        """
        n = len(nums)
        result = [0] * n
        pos_res_idx = 0  # Pointer for placing positive numbers (0, 2, 4, ...)
        neg_res_idx = 1  # Pointer for placing negative numbers (1, 3, 5, ...)

        for num in nums:
            if num > 0:
                result[pos_res_idx] = num
                pos_res_idx += 2
            else:
                result[neg_res_idx] = num
                neg_res_idx += 2
        return result


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [3,1,-2,-5,2,-4]
    expected1 = [3,-2,1,-5,2,-4]

    # Using Separate Lists Approach
    result1_sep_lists = solution.rearrangeArray(list(nums1))
    print(f"Separate Lists Approach for {nums1}: {result1_sep_lists} (Expected: {expected1})")

    # Using Optimized Pointers Approach
    result1_opt_pointers = solution.rearrangeArray_optimized_pointers(list(nums1))
    print(f"Optimized Pointers Approach for {nums1}: {result1_opt_pointers} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 2
    nums2 = [-1,1]
    expected2 = [1,-1]

    # Using Separate Lists Approach
    result2_sep_lists = solution.rearrangeArray(list(nums2))
    print(f"Separate Lists Approach for {nums2}: {result2_sep_lists} (Expected: {expected2})")

    # Using Optimized Pointers Approach
    result2_opt_pointers = solution.rearrangeArray_optimized_pointers(list(nums2))
    print(f"Optimized Pointers Approach for {nums2}: {result2_opt_pointers} (Expected: {expected2})")
    print("-" * 20)

    # Additional Test Case: More elements
    nums3 = [10,-20,30,-40,50,-60,70,-80]
    expected3 = [10,-20,30,-40,50,-60,70,-80]

    result3_sep_lists = solution.rearrangeArray(list(nums3))
    print(f"Separate Lists Approach for {nums3}: {result3_sep_lists} (Expected: {expected3})")

    result3_opt_pointers = solution.rearrangeArray_optimized_pointers(list(nums3))
    print(f"Optimized Pointers Approach for {nums3}: {result3_opt_pointers} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Different order
    nums4 = [7,-3,1,-8,2,-5]
    expected4 = [7,-3,1,-8,2,-5]

    result4_sep_lists = solution.rearrangeArray(list(nums4))
    print(f"Separate Lists Approach for {nums4}: {result4_sep_lists} (Expected: {expected4})")

    result4_opt_pointers = solution.rearrangeArray_optimized_pointers(list(nums4))
    print(f"Optimized Pointers Approach for {nums4}: {result4_opt_pointers} (Expected: {expected4})")
    print("-" * 20)