# File: Leetcode/Solutions/Amazon/167_Two_Sum_II_Input_Array_Is_Sorted.py

"""
Problem Number: 167
Problem Name: Two Sum II - Input Array Is Sorted
Difficulty: Medium
Tags: Array, Two Pointers, Binary Search
Company (Frequency): Not explicitly stated, but common in top tech companies like Amazon (implied by file path)
Leetcode Link: <https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/>

DESCRIPTION

Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array `[index1, index2]` of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.

Your solution must use only constant extra space.

---

#### Example 1:

Input:
numbers = [2,7,11,15], target = 9

Output:
[1,2]

Explanation:
The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

---

#### Example 2:

Input:
numbers = [2,3,4], target = 6

Output:
[1,3]

Explanation:
The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

---

#### Example 3:

Input:
numbers = [-1,0], target = -1

Output:
[1,2]

Explanation:
The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

---

#### Constraints:

- 2 <= numbers.length <= 3 * 10^4
- -1000 <= numbers[i] <= 1000
- `numbers` is sorted in non-decreasing order.
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem asks us to find two numbers in a sorted array that sum up to a target.
    - The key constraints are that the array is sorted, we need to return 1-based indices, and we must use only constant extra space.
    - The sorted nature of the array is a strong hint for using a two-pointer approach or binary search.
    - A hash map solution (like in "Two Sum I") would take O(n) space, violating the constant space constraint.

    Input:
        numbers: List[int] - The sorted array of integers.
        target: int - The target sum.

    Output:
        List[int] - A 2-element array [index1, index2] (1-based indices).
    """

    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        Approach: Two Pointers
        - This is the optimal solution meeting all constraints (O(n) time, O(1) space).
        - Initialize two pointers: `left` at the beginning of the array (index 0) and `right` at the end of the array (index `len(numbers) - 1`).
        - While `left` is less than `right`:
            - Calculate the `current_sum = numbers[left] + numbers[right]`.
            - If `current_sum == target`: We found the pair. Return `[left + 1, right + 1]` (for 1-based indexing).
            - If `current_sum < target`: The sum is too small. To increase the sum, we need a larger number. Since the array is sorted, we increment `left` to consider a larger left-side value.
            - If `current_sum > target`: The sum is too large. To decrease the sum, we need a smaller number. We decrement `right` to consider a smaller right-side value.
        - Since it's guaranteed that there is exactly one solution, this loop will always find and return the answer.

        T.C.: O(n) - In the worst case, `left` and `right` pointers cross, traversing the array once.
        S.C.: O(1) - Only a few variables are used.
        """
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                # Return 1-based indices
                return [left + 1, right + 1]
            elif current_sum < target:
                left += 1  # Need a larger sum, move left pointer right
            else:  # current_sum > target
                right -= 1 # Need a smaller sum, move right pointer left

        # This part should theoretically not be reached given the problem constraints
        # that there is exactly one solution.
        return []

    # Although Binary Search is listed as a tag, a single binary search won't work directly for two numbers.
    # A potential approach involving binary search would be:
    # For each element `numbers[i]`, perform a binary search for `target - numbers[i]`
    # in the remaining part of the array (`numbers[i+1:]`).
    # This would be O(n log n) time complexity. The Two Pointers approach is more efficient (O(n)).
    # So, we prioritize the Two Pointers solution as it's optimal and simpler.

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    numbers1 = [2,7,11,15]
    target1 = 9
    expected1 = [1,2]

    result1 = solution.twoSum(list(numbers1), target1) # Use list(numbers1) to pass a copy
    print(f"Input: numbers={numbers1}, target={target1} -> Output: {result1} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 2
    numbers2 = [2,3,4]
    target2 = 6
    expected2 = [1,3]

    result2 = solution.twoSum(list(numbers2), target2)
    print(f"Input: numbers={numbers2}, target={target2} -> Output: {result2} (Expected: {expected2})")
    print("-" * 20)

    # Test Case 3
    numbers3 = [-1,0]
    target3 = -1
    expected3 = [1,2]

    result3 = solution.twoSum(list(numbers3), target3)
    print(f"Input: numbers={numbers3}, target={target3} -> Output: {result3} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Larger array
    numbers4 = [1,2,3,4,5,6,7,8,9,10]
    target4 = 15
    expected4 = [5,10] # 5 + 10 = 15

    result4 = solution.twoSum(list(numbers4), target4)
    print(f"Input: numbers={numbers4}, target={target4} -> Output: {result4} (Expected: {expected4})")
    print("-" * 20)

    # Additional Test Case: Negative numbers and positive target
    numbers5 = [-5,-3,0,1,6,8]
    target5 = 3
    expected5 = [2,5] # -3 + 6 = 3

    result5 = solution.twoSum(list(numbers5), target5)
    print(f"Input: numbers={numbers5}, target={target5} -> Output: {result5} (Expected: {expected5})")
    print("-" * 20)