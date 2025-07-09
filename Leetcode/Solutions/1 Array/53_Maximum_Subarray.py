"""
Problem Number: 53
Problem Name: Maximum Subarray
Difficulty: Medium
Tags: Array, Divide and Conquer, Dynamic Programming
Leetcode Link: <https://leetcode.com/problems/maximum-subarray/description/>

DESCRIPTION

Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

---

#### Example 1:

Input:
nums = [-2,1,-3,4,-1,2,1,-5,4]

Output:
6

Explanation:
The subarray [4,-1,2,1] has the largest sum 6.

---

#### Example 2:

Input:
nums = [1]

Output:
1

Explanation:
The subarray [1] has the largest sum 1.

---

#### Example 3:

Input:
nums = [5,4,-1,7,8]

Output:
23

Explanation:
The subarray [5,4,-1,7,8] has the largest sum 23.

---

#### Constraints:

- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

#### Follow up:

- If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
"""

from typing import List
import math

class Solution:
    """
    Thought Process:
    - The problem asks for the largest sum of a contiguous subarray.
    - The most efficient approach is Kadane's Algorithm, which is a dynamic programming technique. It iterates through the array, keeping track of the maximum sum ending at the current position and the overall maximum sum found so far.
    - A second approach, as suggested by the follow-up, is Divide and Conquer. This involves recursively splitting the array, solving for the left and right halves, and also calculating the maximum sum that crosses the midpoint. The overall maximum is the largest of these three values.

    Input:
        nums: List[int] - The array of integers.

    Output:
        int - The largest subarray sum.
    """

    def kadanes_algorithm(self, nums: List[int]) -> int:
        """
        Approach: Kadane's Algorithm
        - Iterate through the array, maintaining two variables: `current_max` and `global_max`.
        - `current_max` is the maximum sum of a subarray ending at the current position.
        - `global_max` is the maximum sum found anywhere in the array so far.
        - For each number, we decide whether to extend the current subarray or start a new one. This is done by `current_max = max(num, current_max + num)`.
        - We then update `global_max` with the new `current_max` if it's larger.

        T.C.: O(n)
        S.C.: O(1)
        """
        if not nums:
            return 0

        global_max = nums[0]
        current_max = nums[0]

        for i in range(1, len(nums)):
            num = nums[i]
            current_max = max(num, current_max + num)
            if current_max > global_max:
                global_max = current_max

        return global_max

    def divide_and_conquer_solution(self, nums: List[int]) -> int:
        """
        Approach: Divide and Conquer
        - Recursively split the array into two halves.
        - The maximum subarray sum can be in:
          1. The left half.
          2. The right half.
          3. A subarray that crosses the midpoint.
        - The crossing sum is found by taking the max sum from the midpoint to the left and the max sum from the midpoint to the right.
        - The function returns the maximum of these three values.

        T.C.: O(n log n)
        S.C.: O(log n) for recursion stack
        """
        def find_max_subarray(arr, left, right):
            # Base case: only one element
            if left == right:
                return arr[left]

            mid = (left + right) // 2

            # 1. Max subarray sum in the left half
            left_sum = find_max_subarray(arr, left, mid)

            # 2. Max subarray sum in the right half
            right_sum = find_max_subarray(arr, mid + 1, right)

            # 3. Max subarray sum that crosses the midpoint
            cross_sum = self._find_max_crossing_sum(arr, left, mid, right)

            return max(left_sum, right_sum, cross_sum)

        return find_max_subarray(nums, 0, len(nums) - 1)

    def _find_max_crossing_sum(self, arr, left, mid, right):
        # Find max sum starting from mid and extending to the left
        left_sum = -math.inf
        current_sum = 0
        for i in range(mid, left - 1, -1):
            current_sum += arr[i]
            if current_sum > left_sum:
                left_sum = current_sum

        # Find max sum starting from mid+1 and extending to the right
        right_sum = -math.inf
        current_sum = 0
        for i in range(mid + 1, right + 1):
            current_sum += arr[i]
            if current_sum > right_sum:
                right_sum = current_sum

        return left_sum + right_sum

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Kadane's for {nums1}: {solution.kadanes_algorithm(nums1)}") # Output: 6
    print(f"D&C for {nums1}: {solution.divide_and_conquer_solution(nums1)}") # Output: 6
    print("-" * 20)

    # Test Case 2
    nums2 = [1]
    print(f"Kadane's for {nums2}: {solution.kadanes_algorithm(nums2)}") # Output: 1
    print(f"D&C for {nums2}: {solution.divide_and_conquer_solution(nums2)}") # Output: 1
    print("-" * 20)

    # Test Case 3
    nums3 = [5, 4, -1, 7, 8]
    print(f"Kadane's for {nums3}: {solution.kadanes_algorithm(nums3)}") # Output: 23
    print(f"D&C for {nums3}: {solution.divide_and_conquer_solution(nums3)}") # Output: 23
    print("-" * 20)