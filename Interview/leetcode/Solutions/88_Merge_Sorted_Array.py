# File: Leetcode/Solutions/Amazon/88_Merge_Sorted_Array.py

"""
Problem Number: 88
Problem Name: Merge Sorted Array
Difficulty: Easy
Tags: Array, Two Pointers, Sorting
Company (Frequency): Not explicitly stated, but common in top tech companies like Amazon (implied by file path)
Leetcode Link: <https://leetcode.com/problems/merge-sorted-array/description/>

DESCRIPTION

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers `m` and `n`, representing the number of elements in `nums1` and `nums2` respectively.
Merge `nums1` and `nums2` into a single array sorted in non-decreasing order.
The final sorted array should not be returned by the function, but instead be stored inside the array `nums1`. To accommodate this, `nums1` has a length of `m + n`, where the first `m` elements denote the elements that should be merged, and the last `n` elements are set to `0` and should be ignored. `nums2` has a length of `n`.

---

#### Example 1:

Input:
nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3

Output:
[1,2,2,3,5,6]

Explanation:
The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.

---

#### Example 2:

Input:
nums1 = [1], m = 1, nums2 = [], n = 0

Output:
[1]

Explanation:
The arrays we are merging are [1] and [].
The result of the merge is [1].

---

#### Example 3:

Input:
nums1 = [0], m = 0, nums2 = [1], n = 1

Output:
[1]

Explanation:
The arrays we are merging are [] and [1].
The result of the merge is [1].
Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.

---

#### Constraints:

- nums1.length == m + n
- nums2.length == n
- 0 <= m, n <= 200
- 1 <= m + n <= 200
- -10^9 <= nums1[i], nums2[j] <= 10^9

#### Follow up:

- Can you come up with an algorithm that runs in O(m + n) time?
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires merging two sorted arrays, `nums1` (with `m` effective elements) and `nums2` (with `n` elements), into `nums1` in-place.
    - The key constraint is that `nums1` has `n` trailing zeros, providing space for `nums2`'s elements.
    - A naive approach might be to copy `nums2` into the zeros part of `nums1` and then sort the entire `nums1`. This would be O((m+n) log (m+n)) due to sorting.
    - To achieve O(m+n) time complexity (as hinted by the follow-up), we need a linear scan approach.
    - Since we are merging into `nums1` and `nums1` has space at the end, it's efficient to start placing elements from the end of `nums1` to avoid overwriting elements that haven't been processed yet.

    Input:
        nums1: List[int] - The first array, with space for merged elements.
        m: int - The number of valid elements in nums1.
        nums2: List[int] - The second array.
        n: int - The number of valid elements in nums2.

    Output:
        None - The function modifies `nums1` in-place.
    """

    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Approach: Two Pointers (Merge from End)
        - This is the optimal solution meeting the O(m + n) time and O(1) extra space complexity (excluding the input arrays themselves).
        - We use three pointers:
            - `p1`: points to the last valid element in `nums1` (`m - 1`).
            - `p2`: points to the last element in `nums2` (`n - 1`).
            - `p`: points to the last position in the merged array `nums1` (`m + n - 1`).
        - We compare elements pointed to by `p1` and `p2`. The larger element is placed at `nums1[p]`, and its respective pointer is decremented.
        - The pointer `p` is always decremented after placing an element.
        - This process continues until `p1` or `p2` goes out of bounds.
        - If there are remaining elements in `nums2` (meaning `p2 >= 0`), they are smaller than any remaining elements in `nums1` (which would have been placed already), so we just copy them directly into the beginning of `nums1`.

        T.C.: O(m + n)
        S.C.: O(1)
        """
        # Initialize pointers
        p1 = m - 1          # Pointer for nums1's valid elements (starts from the end)
        p2 = n - 1          # Pointer for nums2 (starts from the end)
        p = m + n - 1       # Pointer for the merged array in nums1 (starts from the very end)

        # Iterate while there are elements to compare in both arrays
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        # If there are remaining elements in nums2, copy them to nums1
        # This handles cases where nums1's initial elements were all larger
        # than nums2's elements, or m = 0.
        while p2 >= 0:
            nums1[p] = nums2[p2]
            p2 -= 1
            p -= 1

    def simple_copy_and_sort(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Approach: Copy and Sort
        - A simpler but less optimal approach.
        - Copy all elements from `nums2` into the empty slots of `nums1`.
        - Then, sort the entire `nums1` array.

        T.C.: O((m + n) log (m + n)) (due to sorting)
        S.C.: O(1) (if in-place sort, depends on language/implementation)
        """
        # Copy elements from nums2 to the end of nums1
        for i in range(n):
            nums1[m + i] = nums2[i]

        # Sort the entire nums1 array
        nums1.sort()


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1_a = [1,2,3,0,0,0]
    m1 = 3
    nums2_a = [2,5,6]
    n1 = 3
    expected1 = [1,2,2,3,5,6]

    nums1_b = list(nums1_a) # Create a copy for the second method
    nums1_c = list(nums1_a) # Create another copy for visual separation if needed

    # Using Two Pointers (Merge from End)
    solution.merge(nums1_a, m1, nums2_a, n1)
    print(f"Two Pointers (Merge from End) for nums1={nums1_c[:m1]}, nums2={nums2_a}: {nums1_a} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 2
    nums1_a = [1]
    m1 = 1
    nums2_a = []
    n1 = 0
    expected1 = [1]

    nums1_c = list(nums1_a)

    solution.merge(nums1_a, m1, nums2_a, n1)
    print(f"Two Pointers (Merge from End) for nums1={nums1_c[:m1]}, nums2={nums2_a}: {nums1_a} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 3
    nums1_a = [0]
    m1 = 0
    nums2_a = [1]
    n1 = 1
    expected1 = [1]

    nums1_c = list(nums1_a)

    solution.merge(nums1_a, m1, nums2_a, n1)
    print(f"Two Pointers (Merge from End) for nums1={nums1_c[:m1]}, nums2={nums2_a}: {nums1_a} (Expected: {expected1})")
    print("-" * 20)

    # Additional Test Case: nums2 has smaller elements that need to go to the front
    nums1_a = [4,5,6,0,0,0]
    m1 = 3
    nums2_a = [1,2,3]
    n1 = 3
    expected1 = [1,2,3,4,5,6]

    nums1_c = list(nums1_a)

    solution.merge(nums1_a, m1, nums2_a, n1)
    print(f"Two Pointers (Merge from End) for nums1={nums1_c[:m1]}, nums2={nums2_a}: {nums1_a} (Expected: {expected1})")
    print("-" * 20)

    # Additional Test Case: m = 0 (only nums2 elements)
    nums1_a = [0,0,0,0]
    m1 = 0
    nums2_a = [1,2,3,4]
    n1 = 4
    expected1 = [1,2,3,4]

    nums1_c = list(nums1_a)

    solution.merge(nums1_a, m1, nums2_a, n1)
    print(f"Two Pointers (Merge from End) for nums1={nums1_c[:m1]}, nums2={nums2_a}: {nums1_a} (Expected: {expected1})")
    print("-" * 20)