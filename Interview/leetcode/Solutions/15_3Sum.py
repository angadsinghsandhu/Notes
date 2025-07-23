# File: Leetcode/Solutions/Array/15_3Sum.py
"""
Problem Number: 15
Problem Name: 3Sum
Difficulty: Medium
Tags: Array, Two Pointers, Sorting
Company (Frequency): Extremely common and fundamental interview problem, appears very frequently at top tech companies.
Leetcode Link: <https://leetcode.com/problems/3sum/description/>

DESCRIPTION

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.
Notice that the solution set must not contain duplicate triplets.

---

#### Example 1:

Input:
nums = [-1,0,1,2,-1,-4]

Output:
[[-1,-1,2],[-1,0,1]]

Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

---

#### Example 2:

Input:
nums = [0,1,1]

Output:
[]

Explanation:
The only possible triplet does not sum up to 0.

---

#### Example 3:

Input:
nums = [0,0,0]

Output:
[[0,0,0]]

Explanation:
The only possible triplet sums up to 0.

---

#### Constraints:

- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5
- The product of any subarray of `nums` is guaranteed to fit in a 32-bit integer.
"""
from typing import List

class Solution:
    """
    Thought Process for 3Sum:

    The problem asks us to find all unique triplets `[nums[i], nums[j], nums[k]]` in an array `nums`
    such that `nums[i] + nums[j] + nums[k] == 0`. We must avoid duplicate triplets in the output.

    Challenges:
    1.  Finding three numbers that sum to zero.
    2.  Handling duplicates: If the input array has duplicate numbers, we need to ensure that the same triplet (e.g., `[-1, 0, 1]`) is not added multiple times to the result set.

    Common Approaches and their analysis:

    1.  **Brute Force:**
        -   Iterate through all possible combinations of three distinct indices `i, j, k`.
        -   Check their sum. If it's zero, add the sorted triplet to a set (to handle duplicates) then convert to a list.
        -   **T.C.:** O(N^3) (three nested loops). For N=3000, this is `3000^3 = 2.7 * 10^10` operations, far too slow.
        -   **S.C.:** O(N) or O(N^3) for the set of triplets depending on unique triplets formed.

    2.  **Using Hash Set for the Third Element (N^2 with Hash Set):**
        -   Fix `nums[i]` and `nums[j]`, then calculate the `target = -(nums[i] + nums[j])`.
        -   Check if `target` exists in the remaining part of the array using a hash set.
        -   To correctly handle duplicates and ensure `i != j != k`, it's still best to sort the array first.
        -   **Algorithm:**
            1. Sort `nums`.
            2. Initialize `result = set()` (use set of tuples for uniqueness).
            3. Outer loop `i` from 0 to `n-3`:
               a. Skip duplicates for `nums[i]`: `if i > 0 and nums[i] == nums[i-1]: continue`.
               b. Create a `seen_numbers` hash set for numbers encountered in the inner loop (from index `i+1` onwards for the current `i`).
               c. Inner loop `j` from `i+1` to `n-1`:
                  i. `complement = -(nums[i] + nums[j])`.
                  ii. If `complement` is in `seen_numbers`:
                      - Add `tuple(sorted((nums[i], nums[j], complement)))` to `result`.
                  iii. Add `nums[j]` to `seen_numbers`.
            4. Convert `result` set to a list of lists.
        -   **T.C.:** O(N^2)
            - Sorting: O(N log N).
            - Outer loop: N iterations. Inner loop: N iterations. Hash set operations: O(1) average.
            - Total: O(N log N + N*N) = O(N^2).
        -   **S.C.:** O(N) for the hash set, plus O(N) for the result set (worst case all triplets are unique).

    3.  **Sorting + Two Pointers (Optimal and Canonical Solution):**
        -   This is the most widely accepted and efficient approach. It cleverly combines sorting with the two-pointer technique to achieve O(N^2) time complexity while efficiently handling duplicates.
        -   **Core Idea:**
            1. Sort the array `nums`. This allows us to move pointers systematically and easily skip duplicate elements.
            2. Iterate through each element `nums[i]` from `0` to `n-3` (as the first element of the triplet).
            3. For each `nums[i]`, the problem reduces to a 2Sum problem on the subarray `nums[i+1:]`. We need to find `nums[left]` and `nums[right]` such that `nums[left] + nums[right] = -nums[i]`.
            4. Use two pointers, `left` (starting at `i+1`) and `right` (starting at `n-1`), to search for the remaining two numbers.
        -   **Algorithm:**
            1.  Sort `nums`.
            2.  Initialize `result = []`.
            3.  Get array length `n = len(nums)`.
            4.  Iterate `i` from 0 to `n - 3`:
                a.  **Optimization/Duplicate Handling for `nums[i]`:** If `nums[i]` is the same as `nums[i-1]` (and `i > 0`), it means we've already considered `nums[i-1]` as the first element of a triplet, and any triplet starting with the current `nums[i]` would be a duplicate. So, `continue` to the next `i`.
                b.  Initialize `left = i + 1` and `right = n - 1`.
                c.  Calculate `target = -nums[i]` (because `nums[i] + nums[left] + nums[right] == 0` means `nums[left] + nums[right] == -nums[i]`).
                d.  While `left < right`:
                    i.  Calculate `current_sum = nums[left] + nums[right]`.
                    ii. If `current_sum == target`:
                        -   Add `[nums[i], nums[left], nums[right]]` to `result`.
                        -   **Duplicate Handling for `left` and `right`:**
                            -   Increment `left` while `left < right` and `nums[left]` is equal to `nums[left+1]`.
                            -   Decrement `right` while `left < right` and `nums[right]` is equal to `nums[right-1]`.
                        -   Move pointers inwards: `left += 1`, `right -= 1`.
                    iii. Else if `current_sum < target`:
                        -   Increment `left` (need a larger sum).
                    iv. Else (`current_sum > target`):
                        -   Decrement `right` (need a smaller sum).
            5.  Return `result`.

        -   **T.C.:** O(N^2)
            -   Sorting: O(N log N).
            -   Outer loop runs N times.
            -   Inner two-pointer loop runs at most N times (as `left` and `right` pointers traverse the remaining part of the array, `left` only moves forward, `right` only moves backward).
            -   Total: O(N log N + N * N) = O(N^2).
        -   **S.C.:** O(log N) to O(N) for sorting (depending on implementation), plus O(N) for storing the result triplets. Considered O(1) auxiliary space if sorting is in-place and output space is not counted.
    """

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Approach: Sorting + Two Pointers.
        This is the most efficient and standard solution for the 3Sum problem.

        T.C.: O(N^2)
        S.C.: O(log N) to O(N) (for sorting, depending on Python's sort implementation, typically Timsort which is O(N) worst-case).
              If considering auxiliary space for pointers and not the output list, it's O(1).
        """
        result = []
        nums.sort()  # Sort the array to efficiently handle duplicates and use two pointers.
        n = len(nums)

        # Iterate through the array for the first element of the triplet
        # We go up to n-2 because we need at least two more elements (left and right)
        for i in range(n - 2):
            # Skip duplicate values for nums[i]
            # This ensures that we don't process the same triplet multiple times
            # (e.g., if nums = [-1, -1, 2], we process the first -1, then skip the second -1).
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Set up two pointers for the remaining part of the array
            left = i + 1
            right = n - 1
            target = -nums[i] # We are looking for nums[left] + nums[right] = -nums[i]

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    # Found a triplet
                    result.append([nums[i], nums[left], nums[right]])

                    # Skip duplicate values for nums[left] and nums[right]
                    # Move left pointer past any duplicates
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Move right pointer past any duplicates
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    # Move both pointers to continue searching for other triplets
                    left += 1
                    right -= 1
                elif current_sum < target:
                    # Sum is too small, need a larger value. Move left pointer right.
                    left += 1
                else: # current_sum > target
                    # Sum is too large, need a smaller value. Move right pointer left.
                    right -= 1
        
        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([-1,0,1,2,-1,-4], [[-1,-1,2],[-1,0,1]]),
        ([0,1,1], []),
        ([0,0,0], [[0,0,0]]),
        ([0,0,0,0], [[0,0,0]]), # Test with more zeros
        ([-2,0,1,1,2], [[-2,0,2],[-2,1,1]]), # Test with multiple valid triplets and duplicates
        ([-5,-4,-3,-2,-1,0,1,2,3,4,5], [
            [-5,0,5], [-5,1,4], [-5,2,3],
            [-4,-1,5], [-4,0,4], [-4,1,3],
            [-3,-2,5], [-3,-1,4], [-3,0,3], [-3,1,2],
            [-2,-1,3], [-2,0,2],
            [-1,0,1]
        ]),
        ([-1,0,1,2,-1,-4,-2,-3,3,0,4], [[-4,0,4],[-4,1,3],[-3,-1,4],[-3,0,3],[-2,-1,3],[-2,0,2],[-1,-1,2],[-1,0,1]])
    ]

    # Helper function to sort and normalize output for comparison
    def normalize_output(output: List[List[int]]) -> List[List[int]]:
        return sorted([sorted(triplet) for triplet in output])

    for nums, expected_output in test_cases:
        # Pass a copy of the list because sort modifies in-place
        result = solution.threeSum(list(nums))
        
        normalized_result = normalize_output(result)
        normalized_expected = normalize_output(expected_output)

        print(f"Input: {nums}")
        print(f"Output: {normalized_result}")
        print(f"Expected: {normalized_expected}")
        print(f"Status: {'Pass' if normalized_result == normalized_expected else 'Fail'}")
        print("-" * 30)