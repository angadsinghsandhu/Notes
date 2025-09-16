# TODO: revisit

# File: Leetcode/Solutions/287_Find_the_Duplicate_Number.py

"""
Problem Number: 287
Problem Name: Find the Duplicate Number
Difficulty: Medium
Tags: Array, Two Pointers, Binary Search, Neetcode 150
Company (Frequency): Amazon, Apple, Facebook, Google, Microsoft
Leetcode Link: <https://leetcode.com/problems/find-the-duplicate-number/description/>

DESCRIPTION

Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive.
There is only one repeated number in `nums`, return this repeated number.
You must solve the problem without modifying the array `nums` and using only constant extra space.

---

#### Example 1:

Input:
nums = [1,3,4,2,2]

Output:
2

---

#### Example 2:

Input:
nums = [3,1,3,4,2]

Output:
3

---

#### Example 3:

Input:
nums = [3,3,3,3,3]

Output:
3

---

#### Constraints:

- 1 <= n <= 10^5
- nums.length == n + 1
- 1 <= nums[i] <= n
- All the integers in `nums` appear only once except for precisely one integer which appears two or more times.

#### Follow up:

- How can we prove that at least one duplicate number must exist in `nums`? (Hint: Pigeonhole Principle)
- Can you solve the problem in linear runtime complexity?
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem asks us to find a single duplicate number in an array without modifying the array and using constant extra space.
    - The numbers are in the range [1, n], and there are n+1 numbers in the array. This setup is a classic hint for cycle detection in a linked list, or problems that can be mapped to it.
    - If there were no duplicates, and we considered `nums[i]` as the "next" node for `i`, it would form a permutation of [1, n] plus an extra element. With a duplicate, it forms a cycle.

    Input:
        nums: List[int] - The array of integers.

    Output:
        int - The repeated number.
    """

    def floyd_cycle_detection_solution(self, nums: List[int]) -> int:
        """
        Approach: Floyd's Tortoise and Hare (Cycle Detection)
        - This is the most optimal solution meeting all constraints (O(n) time, O(1) space, no modification).
        - We can think of the array elements as pointers. If we start at index `0` and go to `nums[0]`, then `nums[nums[0]]`, and so on, this forms a sequence.
        - Since there are `n+1` numbers in the range `[1, n]`, and only one duplicate, this structure can be viewed as a linked list with a cycle. The duplicate number is the entry point of the cycle.
        - Use two pointers, `slow` and `fast`.
        - `slow` moves one step at a time: `slow = nums[slow]`
        - `fast` moves two steps at a time: `fast = nums[nums[fast]]`
        - They are guaranteed to meet inside the cycle.
        - Once they meet, reset `slow` to the beginning (index `0` or `nums[0]` effectively, but here we can reset it to point to the first element's value, or restart from a known non-cycle point). A common way is to reset `slow` to `nums[0]` and move both `slow` and `fast` one step at a time until they meet again. This second meeting point is the start of the cycle, which is our duplicate number.

        T.C.: O(n)
        S.C.: O(1)
        """
        # Initialize slow and fast pointers.
        # It's important to start them such that the 'next' step will be into the array's "linked list".
        # A common way is to think of index 0 as a dummy node, and the sequence starts from nums[0].
        # Or, just consider `slow = nums[0]` and `fast = nums[nums[0]]` as the very first step.
        slow = nums[0]
        fast = nums[nums[0]]

        # Phase 1: Find the meeting point inside the cycle
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]

        # Phase 2: Find the start of the cycle (the duplicate number)
        # Reset one pointer to the beginning (effectively index 0, or value 0)
        # The crucial insight is that the distance from the start of the "list"
        # to the cycle entry point is the same as the distance from the meeting point
        # to the cycle entry point.
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow # Or fast, they are at the same point

    def binary_search_solution(self, nums: List[int]) -> int:
        """
        Approach: Binary Search
        - This approach leverages the fact that the numbers are in the range [1, n].
        - We can perform a binary search on the possible values of the duplicate number (from 1 to n).
        - For a given `mid` value, we count how many numbers in `nums` are less than or equal to `mid`.
        - If this count is greater than `mid`, it means that the duplicate number must be in the range `[1, mid]`. We try to find a smaller duplicate by setting `high = mid - 1` and `ans = mid`.
        - Otherwise, the duplicate must be in the range `[mid + 1, n]`. We set `low = mid + 1`.

        T.C.: O(n log n) (log n for binary search, n for counting in each step)
        S.C.: O(1)
        """
        n = len(nums) - 1 # The range of numbers is [1, n]
        low = 1
        high = n
        ans = -1

        while low <= high:
            mid = low + (high - low) // 2
            count = 0
            for num in nums:
                if num <= mid:
                    count += 1

            if count > mid:
                # The duplicate is in the lower half (including mid)
                ans = mid
                high = mid - 1
            else:
                # The duplicate is in the upper half
                low = mid + 1
        return ans

    # Other common solutions (not implemented to keep this concise, but worth mentioning):
    # - Using a Hash Set: O(n) T.C., O(n) S.C. (violates constant space constraint)
    # - Sorting: O(n log n) T.C., O(1) or O(n) S.C. depending on sort (violates "without modifying array" constraint)


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [1,3,4,2,2]
    expected1 = 2

    # Using Floyd's Cycle Detection
    result1_floyd = solution.floyd_cycle_detection_solution(list(nums1)) # Using list(nums1) to ensure original not modified
    print(f"Floyd's Cycle Detection for {nums1}: {result1_floyd} (Expected: {expected1})")

    # Using Binary Search
    result1_bs = solution.binary_search_solution(list(nums1))
    print(f"Binary Search Solution for {nums1}: {result1_bs} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 2
    nums2 = [3,1,3,4,2]
    expected2 = 3

    # Using Floyd's Cycle Detection
    result2_floyd = solution.floyd_cycle_detection_solution(list(nums2))
    print(f"Floyd's Cycle Detection for {nums2}: {result2_floyd} (Expected: {expected2})")

    # Using Binary Search
    result2_bs = solution.binary_search_solution(list(nums2))
    print(f"Binary Search Solution for {nums2}: {result2_bs} (Expected: {expected2})")
    print("-" * 20)

    # Test Case 3
    nums3 = [3,3,3,3,3]
    expected3 = 3

    # Using Floyd's Cycle Detection
    result3_floyd = solution.floyd_cycle_detection_solution(list(nums3))
    print(f"Floyd's Cycle Detection for {nums3}: {result3_floyd} (Expected: {expected3})")

    # Using Binary Search
    result3_bs = solution.binary_search_solution(list(nums3))
    print(f"Binary Search Solution for {nums3}: {result3_bs} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Larger array
    nums4 = [2,5,9,6,9,3,8,9,7,1]
    expected4 = 9

    # Using Floyd's Cycle Detection
    result4_floyd = solution.floyd_cycle_detection_solution(list(nums4))
    print(f"Floyd's Cycle Detection for {nums4}: {result4_floyd} (Expected: {expected4})")

    # Using Binary Search
    result4_bs = solution.binary_search_solution(list(nums4))
    print(f"Binary Search Solution for {nums4}: {result4_bs} (Expected: {expected4})")
    print("-" * 20)