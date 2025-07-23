# File: Leetcode/Solutions/Array/128_Longest_Consecutive_Sequence.py
"""
Problem Number: 128
Problem Name: Longest Consecutive Sequence
Difficulty: Medium
Tags: Array, Hash Table, Union Find
Company (Frequency): Very common interview question at top tech companies.
Leetcode Link: <https://leetcode.com/problems/longest-consecutive-sequence/description/>

DESCRIPTION

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.
You must write an algorithm that runs in O(n) time.

---

#### Example 1:

Input:
nums = [100,4,200,1,3,2]

Output:
4

Explanation:
The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

---

#### Example 2:

Input:
nums = [0,3,7,2,5,8,4,6,0,1]

Output:
9

---

#### Example 3:

Input:
nums = [1,0,1,2]

Output:
3

---

#### Constraints:

- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

"""
from typing import List

class Solution:
    """
    Thought Process for Longest Consecutive Sequence:

    The problem asks for the length of the longest sequence of consecutive integers in an unsorted array `nums`.
    A key constraint is that the algorithm must run in O(N) time.

    Let's consider different approaches and their complexities:

    1.  **Brute Force (Inefficient):**
        -   For each number `x` in the array, check if `x+1`, `x+2`, `x+3`, ..., exist in the array.
        -   To quickly check existence, convert `nums` to a `set`.
        -   **Algorithm:**
            1. Convert `nums` to a hash set `num_set`.
            2. Initialize `longest_streak = 0`.
            3. For each `num` in `nums`:
               a. Start `current_num = num` and `current_streak = 1`.
               b. While `current_num + 1` is in `num_set`:
                  i. `current_num += 1`
                  ii. `current_streak += 1`
               c. `longest_streak = max(longest_streak, current_streak)`.
            4. Return `longest_streak`.
        -   **Problem:** While lookups in a set are O(1) on average, if the array contains many long sequences, the inner `while` loop might run multiple times for elements within the same sequence, leading to an overall O(N^2) worst-case time complexity (e.g., for `[1,2,3,...,N]`, each number would initiate a check up to its end).
        -   **T.C.:** O(N^2) in worst case.
        -   **S.C.:** O(N) for the hash set.

    2.  **Sorting:**
        -   **Idea:** If the array is sorted, consecutive elements will be adjacent, making it easy to find sequences by iterating through the sorted array.
        -   **Algorithm:**
            1. Sort `nums`.
            2. Handle empty or single-element arrays.
            3. Initialize `longest_streak = 0`, `current_streak = 0`.
            4. Iterate through the sorted array:
               a. Skip duplicate elements.
               b. If `nums[i]` is `nums[i-1] + 1`, increment `current_streak`.
               c. Else (not consecutive), reset `current_streak = 1`.
               d. Update `longest_streak = max(longest_streak, current_streak)`.
            5. Return `longest_streak`.
        -   **Problem:** Sorting takes O(N log N) time, which violates the O(N) requirement.
        -   **T.C.:** O(N log N)
        -   **S.C.:** O(1) (for in-place sort) or O(N) (if a new sorted list is created).

    3.  **Hash Set (Optimized O(N) Solution):**
        -   **Key Insight:** The O(N^2) issue in the brute-force approach comes from repeatedly starting a sequence check from an element `x` when `x-1` is already present. If `x-1` is present, it means `x` is *not* the start of the overall consecutive sequence. We only need to start counting a sequence from an element `x` if `x-1` does *not* exist in the input set. This ensures each sequence is only "traversed" once from its true starting point.
        -   **Algorithm:**
            1.  Convert `nums` to a hash set `num_set` for O(1) average time lookups. This also handles duplicates automatically if `nums` contains any.
            2.  Initialize `longest_streak = 0`.
            3.  Iterate through each `num` in the original `nums` array (or iterate through the `num_set`):
                a.  **Crucial Check:** `if (num - 1) not in num_set:`
                    -   This `num` is a potential start of a new consecutive sequence.
                    -   Initialize `current_num = num` and `current_streak = 1`.
                    -   While `(current_num + 1)` is in `num_set`:
                        -   `current_num += 1`
                        -   `current_streak += 1`
                    -   `longest_streak = max(longest_streak, current_streak)`
            4.  Return `longest_streak`.
        -   **T.C.:** O(N) on average.
            -   Converting to set: O(N).
            -   The outer loop iterates N times. The inner `while` loop, however, collectively processes each number in a sequence only once *across all outer loop iterations*. For example, if `[1,2,3,4]` is present, when `num=1`, the `while` loop progresses. When `num=2, 3, or 4`, the `(num - 1) not in num_set` condition will be false, and these numbers will be quickly skipped. Thus, each number is visited (checked in the `while` loop) at most a constant number of times over the entire execution.
        -   **S.C.:** O(N) to store elements in the hash set. This meets the O(N) time constraint.

    4.  **Union-Find (Alternative O(N) on average):**
        -   This approach models the problem as finding connected components where numbers `x` and `x+1` are connected if both exist. The largest component's size is the answer.
        -   **Complexity:** O(N * alpha(N)) effectively O(N) on average, and O(N) space.
        -   **Consideration:** While valid, it's generally more complex to implement than the hash set approach for this specific problem and might have larger constant factors. The hash set approach is typically preferred for its simplicity and directness in achieving O(N).
    """

    def longestConsecutive(self, nums: List[int]) -> int:
        """
        Approach: Hash Set (Optimized O(N) Solution)

        T.C.: O(N) on average
        S.C.: O(N)
        """
        if not nums:
            return 0

        # Convert to a set for O(1) average time lookups.
        # This also automatically handles duplicate numbers.
        num_set = set(nums)
        
        longest_streak = 0

        # Iterate through each number in the original list (or the set)
        for num in nums:
            # Check if the current number 'num' is the start of a consecutive sequence.
            # A number 'num' is the start if 'num - 1' is NOT present in the set.
            if (num - 1) not in num_set:
                current_num = num
                current_streak = 1

                # Extend the sequence upwards
                while (current_num + 1) in num_set:
                    current_num += 1
                    current_streak += 1
                
                # Update the maximum streak found so far
                longest_streak = max(longest_streak, current_streak)
        
        return longest_streak

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([100,4,200,1,3,2], 4),
        ([0,3,7,2,5,8,4,6,0,1], 9),
        ([1,0,1,2], 3),
        ([], 0), # Empty array
        ([1], 1), # Single element
        ([5,4,3,2,1], 5), # Descending sequence
        ([1,2,0,1], 3), # Duplicates and non-sequential
        ([9,1,4,7,3,-1,0,5,8,-1,6], 10), # Complex sequence with negatives and duplicates
        ([0, -1], 2), # Negative numbers
        ([1,3,5,7,9], 1), # No consecutive numbers
    ]

    for nums, expected_output in test_cases:
        result = solution.longestConsecutive(list(nums)) # Pass a copy of the list
        print(f"Input: {nums}")
        print(f"Output: {result}")
        print(f"Expected: {expected_output}")
        print(f"Status: {'Pass' if result == expected_output else 'Fail'}")
        print("-" * 30)