# File: Leetcode/Solutions/Array/78_Subsets.py
"""
Problem Number: 78
Problem Name: Subsets
Difficulty: Medium
Tags: Backtracking, Bit Manipulation, Recursion, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/subsets/description/>

DESCRIPTION

Given an integer array `nums` of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.

---

#### Example 1:

Input:
nums = [1,2,3]

Output:
[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

---

#### Example 2:

Input:
nums = [0]

Output:
[[],[0]]

---

#### Constraints:

- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of `nums` are unique.
"""
from typing import List

class Solution:
    """
    Thought Process for Subsets:

    The problem asks us to generate all possible subsets (the power set) of a given integer array `nums`
    containing unique elements. The order of subsets or elements within subsets does not matter.

    For an array of `n` unique elements, there are $2^n$ possible subsets. This is because each element
    can either be included or excluded from a given subset, resulting in 2 choices for each of the `n` elements.

    Common approaches to solve this combinatorial problem:

    1.  **Backtracking (Recursive Approach):**
        - This is a very intuitive and common approach for problems involving permutations, combinations, and subsets.
        - The idea is to build subsets incrementally. At each step, for an element `nums[i]`, we have two fundamental choices:
            a.  Include `nums[i]` in the current subset.
            b.  Exclude `nums[i]` from the current subset.
        - We explore both paths recursively.

    2.  **Iterative Approach:**
        - Start with an empty subset `[[]]`.
        - For each number in the input `nums`, iterate through all subsets generated so far.
        - For each existing subset, create a new subset by adding the current number to it.
        - Add all these newly created subsets to the collection of subsets.

    3.  **Bit Manipulation:**
        - This approach leverages the fact that each subset can be uniquely mapped to a binary number from `0` to `2^n - 1`.
        - If the `j`-th bit of a binary number `i` is set (1), it means the `j`-th element of `nums` is included in the subset.
        - If the `j`-th bit is not set (0), it's excluded.
        - We iterate through all numbers from `0` to `2^n - 1`, and for each number, construct the corresponding subset.

    Complexity Analysis (for all approaches):
    Let `n` be the length of `nums`.

    -   **Time Complexity (T.C.):** O($N * 2^N$)
        -   There are $2^N$ total subsets.
        -   For each subset, creating a copy and adding it to the result list typically takes O(N) time (proportional to the maximum length of a subset).
        -   Thus, $2^N$ subsets * N operations per subset = $N * 2^N$.
    -   **Space Complexity (S.C.):** O($N * 2^N$)
        -   This is the space required to store all $2^N$ subsets. In the worst case, the sum of lengths of all subsets is $N * 2^{N-1}$. If we count the output space as part of the complexity, this is the dominant factor.
        -   Auxiliary space (recursion stack for backtracking, or temporary variables for iterative/bit manipulation) is O(N).
    """

    def subsets_backtracking(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 1: Backtracking (Recursive)

        T.C.: O(N * 2^N)
        S.C.: O(N * 2^N) (for storing results) + O(N) (for recursion stack depth)
        """
        result = []
        n = len(nums)

        def backtrack(current_subset: List[int], start_index: int):
            # Base case: Add the current subset to the result.
            # Make a copy of current_subset to avoid issues with modification later.
            result.append(list(current_subset))

            # Recursive step: Iterate through the remaining elements
            for i in range(start_index, n):
                # Include nums[i]
                current_subset.append(nums[i])
                # Recurse with the next element
                backtrack(current_subset, i + 1)
                # Exclude nums[i] (backtrack) - remove the last added element
                current_subset.pop()

        # Start the backtracking process from an empty subset and the first element (index 0)
        backtrack([], 0)
        return result

    def subsets_iterative(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 2: Iterative Construction

        T.C.: O(N * 2^N)
        S.C.: O(N * 2^N)
        """
        result = [[]]  # Start with an empty subset

        for num in nums:
            # For each number, iterate through all existing subsets
            # and create new subsets by adding the current number to them.
            # We iterate through `result` as it was before this iteration started,
            # so we use a copy of the list or iterate through its current length.
            # Using result_len_before_iter ensures we don't process newly added subsets in the same loop.
            result_len_before_iter = len(result)
            for i in range(result_len_before_iter):
                current_subset = list(result[i]) # Make a copy
                current_subset.append(num)
                result.append(current_subset)
        
        return result

    def subsets_bit_manipulation(self, nums: List[int]) -> List[List[int]]:
        """
        Approach 3: Bit Manipulation

        T.C.: O(N * 2^N)
        S.C.: O(N * 2^N)
        """
        n = len(nums)
        num_subsets = 1 << n  # This is 2^n

        result = []
        # Iterate from 0 to 2^n - 1. Each number represents a unique subset.
        for i in range(num_subsets):
            current_subset = []
            # Check each bit from 0 to n-1
            for j in range(n):
                # If the j-th bit of 'i' is set (1), include nums[j]
                if (i >> j) & 1:
                    current_subset.append(nums[j])
            result.append(current_subset)
            
        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([1,2,3], [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]),
        ([0], [[],[0]]),
        ([], [[]]), # Empty input array
        ([1,2], [[],[1],[2],[1,2]]),
        ([5,10], [[],[5],[10],[5,10]]),
    ]

    # Helper to sort list of lists for consistent comparison, as order doesn't matter
    def sort_subsets(subsets: List[List[int]]) -> List[List[int]]:
        return sorted([sorted(s) for s in subsets])

    print("--- Testing subsets_backtracking ---")
    for nums, expected in test_cases:
        result = solution.subsets_backtracking(list(nums))
        print(f"Input: {nums}")
        print(f"Output: {sort_subsets(result)}")
        print(f"Expected: {sort_subsets(expected)}")
        print(f"Status: {'Pass' if sort_subsets(result) == sort_subsets(expected) else 'Fail'}")
        print("-" * 30)

    print("\n--- Testing subsets_iterative ---")
    for nums, expected in test_cases:
        result = solution.subsets_iterative(list(nums))
        print(f"Input: {nums}")
        print(f"Output: {sort_subsets(result)}")
        print(f"Expected: {sort_subsets(expected)}")
        print(f"Status: {'Pass' if sort_subsets(result) == sort_subsets(expected) else 'Fail'}")
        print("-" * 30)

    print("\n--- Testing subsets_bit_manipulation ---")
    for nums, expected in test_cases:
        result = solution.subsets_bit_manipulation(list(nums))
        print(f"Input: {nums}")
        print(f"Output: {sort_subsets(result)}")
        print(f"Expected: {sort_subsets(expected)}")
        print(f"Status: {'Pass' if sort_subsets(result) == sort_subsets(expected) else 'Fail'}")
        print("-" * 30)