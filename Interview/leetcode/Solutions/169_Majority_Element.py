# File: Leetcode/Solutions/Array/169_Majority_Element.py
"""
Problem Number: 169
Problem Name: Majority Element
Difficulty: Easy
Tags: Array, Hash Table, Divide and Conquer, Sorting, Counting
Company (Frequency): Not explicitly stated, but a very common interview question across many companies.
Leetcode Link: <https://leetcode.com/problems/majority-element/description/>

DESCRIPTION

Given an array `nums` of size `n`, return the majority element.
The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

---

#### Example 1:

Input:
nums = [3,2,3]

Output:
3

---

#### Example 2:

Input:
nums = [2,2,1,1,1,2,2]

Output:
2

---

#### Constraints:

- n == nums.length
- 1 <= n <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9

---

#### Follow-up:

Could you solve the problem in linear time and in O(1) space?
"""
from typing import List
import collections

class Solution:
    """
    Thought Process for Majority Element:

    The problem asks us to find the "majority element" in an array `nums` of size `n`.
    A majority element is defined as an element that appears more than `⌊n / 2⌋` times.
    We are guaranteed that such an element always exists in the array.

    Given the guarantee that a majority element *always* exists, this simplifies things significantly
    as we don't need to handle cases where no majority element is present (e.g., tie situations).

    Several approaches can be used:

    1.  **Brute Force (Inefficient):**
        - Iterate through each element `x` in `nums`.
        - For each `x`, iterate through the entire array again to count its occurrences.
        - If `count(x) > n / 2`, return `x`.
        - T.C.: O(N^2)
        - S.C.: O(1)
        - This approach is too slow for the given constraints (N up to 5 * 10^4).

    2.  **Hash Map / Dictionary:**
        - Store the frequency of each element in a hash map (dictionary in Python).
        - After counting all elements, iterate through the hash map and find the element whose count
          is greater than `n / 2`.
        - T.C.: O(N) to populate the hash map, O(k) (where k is number of unique elements, k <= N)
          to find the majority element. Overall O(N).
        - S.C.: O(N) in the worst case (if all elements are unique). This satisfies the linear time,
          but not the O(1) space follow-up.

    3.  **Sorting:**
        - If the array is sorted, the majority element, by definition, must occupy the middle position
          (`nums[n // 2]`). This is because it appears more than `n/2` times, so even if other
          elements are arranged around it, it will always "fill up" the center.
        - T.C.: O(N log N) due to sorting.
        - S.C.: O(1) if sorting in-place (e.g., Python's `list.sort()` generally uses Timsort, which
          is O(N) worst-case space but often considered O(1) auxiliary space for in-place sorts).

    4.  **Boyer-Moore Voting Algorithm (Optimal for Follow-up):**
        - This is a clever algorithm that achieves O(N) time and O(1) space.
        - The core idea is to find a candidate for the majority element by canceling out non-majority
          elements.
        - Initialize `candidate = None` and `count = 0`.
        - Iterate through the array:
            - If `count` is 0, it means the previous `candidate` (if any) has been "cancelled out"
              by other elements, so we pick the current element as a new `candidate`.
            - If the current element `num` is equal to `candidate`, increment `count`.
            - If `num` is different from `candidate`, decrement `count`.
        - Because a majority element is guaranteed to exist, the final `candidate` after iterating
          through the entire array will always be the majority element. This works because the
          majority element's occurrences outnumber all other elements' occurrences combined.
        - T.C.: O(N)
        - S.C.: O(1)

    5.  **Divide and Conquer:**
        - Recursively find the majority element in the left half and the right half.
        - If the majority elements from both halves are the same, that's the majority for the whole.
        - If they are different, count their occurrences in the full array to determine which one (if any)
          is the majority for the combined range.
        - T.C.: O(N log N)
        - S.C.: O(log N) for recursion stack depth.
    """

    def majorityElement_hash_map(self, nums: List[int]) -> int:
        """
        Approach 1: Using a Hash Map (Dictionary)
        This approach counts the frequency of each number and then finds the one
        that exceeds the n/2 threshold.

        T.C.: O(N) - One pass to populate the hash map. Dictionary operations are O(1) on average.
        S.C.: O(N) - In the worst case, all elements are unique, requiring O(N) space to store counts.
        """
        counts = collections.Counter(nums)
        n_half = len(nums) // 2
        for num, count in counts.items():
            if count > n_half:
                return num
        # This line should technically not be reached given the problem constraints
        # that a majority element always exists.
        return -1 

    def majorityElement_sorting(self, nums: List[int]) -> int:
        """
        Approach 2: Sorting
        If the array is sorted, the majority element will always be at the middle index
        (n // 2) because it appears more than n/2 times.

        T.C.: O(N log N) - Dominated by the sorting step.
        S.C.: O(1) - If sorting is done in-place (Python's list.sort() is in-place and typically O(N) aux space in worst case for Timsort, but often considered O(1) for competitive programming context as it modifies the input list directly).
        """
        nums.sort()
        return nums[len(nums) // 2]

    def majorityElement_boyer_moore(self, nums: List[int]) -> int:
        """
        Approach 3: Boyer-Moore Voting Algorithm
        This is an optimal solution for the follow-up, achieving O(N) time and O(1) space.
        The algorithm works on the principle that if an element is a majority element,
        its count will remain positive even after canceling out with all other elements.

        Steps:
        1. Initialize `candidate` to None and `count` to 0.
        2. Iterate through each `num` in `nums`:
           a. If `count` is 0, set `candidate = num` (start tracking a new potential majority).
           b. If `num` is equal to `candidate`, increment `count`.
           c. If `num` is different from `candidate`, decrement `count`.
        3. After the loop, `candidate` will hold the majority element (guaranteed by problem).

        T.C.: O(N) - Single pass through the array.
        S.C.: O(1) - Only two variables (`candidate` and `count`) are used.
        """
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num
            if num == candidate:
                count += 1
            else:
                count -= 1
        
        return candidate

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([3,2,3], 3),
        ([2,2,1,1,1,2,2], 2),
        ([6,5,5], 5),
        ([1], 1),
        ([7,7,7,7,7,7,1,2,3,4,5], 7), # Majority element with non-majority elements
        ([0,0,0,0,0,1,1,1], 0)
    ]

    print("--- Testing majorityElement_hash_map ---")
    for nums, expected in test_cases:
        result = solution.majorityElement_hash_map(list(nums)) # Use list(nums) to pass a copy
        print(f"Input: {nums}, Output: {result}, Expected: {expected} -> {'Pass' if result == expected else 'Fail'}")
    print("-" * 40)

    print("\n--- Testing majorityElement_sorting ---")
    for nums, expected in test_cases:
        result = solution.majorityElement_sorting(list(nums)) # Use list(nums) to pass a copy
        print(f"Input: {nums}, Output: {result}, Expected: {expected} -> {'Pass' if result == expected else 'Fail'}")
    print("-" * 40)

    print("\n--- Testing majorityElement_boyer_moore ---")
    for nums, expected in test_cases:
        result = solution.majorityElement_boyer_moore(list(nums)) # Use list(nums) to pass a copy
        print(f"Input: {nums}, Output: {result}, Expected: {expected} -> {'Pass' if result == expected else 'Fail'}")
    print("-" * 40)