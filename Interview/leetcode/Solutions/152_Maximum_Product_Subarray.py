# File: Leetcode/Solutions/Array/152_Maximum_Product_Subarray.py
"""
Problem Number: 152
Problem Name: Maximum Product Subarray
Difficulty: Medium
Tags: Array, Dynamic Programming
Company (Frequency): Classic DP problem, frequently seen in interviews at top tech companies.
Leetcode Link: <https://leetcode.com/problems/maximum-product-subarray/description/>

DESCRIPTION

Given an integer array `nums`, find a subarray that has the largest product, and return the product.
The test cases are generated so that the answer will fit in a 32-bit integer.

---

#### Example 1:

Input:
nums = [2,3,-2,4]

Output:
6

Explanation:
[2,3] has the largest product 6.

---

#### Example 2:

Input:
nums = [-2,0,-1]

Output:
0

Explanation:
The result cannot be 2, because [-2,-1] is not a subarray.
The largest product is 0, which comes from the subarray [0] or [-2,0] or [0,-1].

---

#### Constraints:

- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any subarray of `nums` is guaranteed to fit in a 32-bit integer.
"""
from typing import List

class Solution:
    """
    Thought Process for Maximum Product Subarray:

    The problem asks for the maximum product of a contiguous subarray. This is similar to Kadane's algorithm
    for Maximum Sum Subarray, but with a crucial difference: negative numbers.
    In sum problems, a negative number always reduces the sum. In product problems, a negative number
    can turn a very small (large negative) product into a large positive product when multiplied by another negative number.
    This implies that we cannot simply track the maximum product ending at the current position; we also need
    to track the minimum product ending at the current position, because a minimum (most negative) product
    multiplied by a negative number might become the new maximum product.

    Consider the state for dynamic programming:
    Let `max_so_far[i]` be the maximum product of a subarray ending at index `i`.
    Let `min_so_far[i]` be the minimum product of a subarray ending at index `i`.

    For `nums[i]`:
    The maximum product ending at `i` could be:
    1.  `nums[i]` itself (starting a new subarray).
    2.  `max_so_far[i-1] * nums[i]` (extending the previous maximum positive product).
    3.  `min_so_far[i-1] * nums[i]` (extending the previous minimum negative product, which becomes positive if `nums[i]` is negative).

    Similarly, the minimum product ending at `i` could be:
    1.  `nums[i]` itself.
    2.  `max_so_far[i-1] * nums[i]`.
    3.  `min_so_far[i-1] * nums[i]`.

    We need to take the `max` of these three for `max_so_far[i]` and the `min` for `min_so_far[i]`.
    The overall maximum product will be the maximum value encountered in `max_so_far` array.

    Optimization: Since `max_so_far[i]` and `min_so_far[i]` only depend on the values at `i-1`,
    we can optimize space from O(N) to O(1) by just keeping track of the current maximum and minimum
    products instead of full arrays.

    Algorithm:

    1.  Initialize `max_prod_ending_here = nums[0]`. This will track the maximum product of a subarray ending at the current index.
    2.  Initialize `min_prod_ending_here = nums[0]`. This will track the minimum product of a subarray ending at the current index.
    3.  Initialize `overall_max_product = nums[0]`. This will store the global maximum product found across all subarrays.

    4.  Iterate through the array `nums` starting from the second element (index 1):
        For each `current_num = nums[i]`:
            a.  **Crucial Step for Negatives:** If `current_num` is negative, it will flip the signs of `max_prod_ending_here` and `min_prod_ending_here`. So, the current maximum product might become the new minimum, and vice versa. To correctly calculate the next `max_prod_ending_here` and `min_prod_ending_here`, we can swap their values *conceptually* before multiplication or simply calculate all three possibilities.
            Let's use a temporary variable for the previous `max_prod_ending_here` to make the update logic clear:
            `temp_max_prod = max_prod_ending_here`

            b.  Calculate the new `max_prod_ending_here`:
                This can be `current_num` itself (starting a new sequence), or `current_num` multiplied by the previous `max_prod_ending_here`, or `current_num` multiplied by the previous `min_prod_ending_here`.
                `max_prod_ending_here = max(current_num, temp_max_prod * current_num, min_prod_ending_here * current_num)`

            c.  Calculate the new `min_prod_ending_here`:
                Similarly, this can be `current_num` itself, or `current_num` multiplied by the previous `max_prod_ending_here`, or `current_num` multiplied by the previous `min_prod_ending_here`.
                `min_prod_ending_here = min(current_num, temp_max_prod * current_num, min_prod_ending_here * current_num)`

            d.  Update `overall_max_product`:
                `overall_max_product = max(overall_max_product, max_prod_ending_here)`

    5.  Return `overall_max_product`.

    Edge Cases:
    -   Single element array: Handled by initialization.
    -   Array with zeros: A zero will reset `max_prod_ending_here` and `min_prod_ending_here` to zero if they become part of a product involving zero, and subsequent positive/negative numbers will then start new sequences from themselves. If the max product is 0, then the result might be 0 (e.g., `[-2,0,-1]` -> 0).

    Complexity:
    -   **Time Complexity (T.C.):** O(N) - We iterate through the array once.
    -   **Space Complexity (S.C.):** O(1) - We only use a few constant extra variables.
    """

    def maxProduct(self, nums: List[int]) -> int:
        if not nums:
            return 0 # Or raise an error based on constraints (1 <= nums.length)

        # Initialize max_so_far and min_so_far to the first element
        # max_so_far: stores the maximum product of a subarray ending at the current position.
        # min_so_far: stores the minimum product of a subarray ending at the current position (important for negatives).
        max_so_far = nums[0]
        min_so_far = nums[0]
        
        # overall_max_product: stores the global maximum product found across all subarrays.
        overall_max_product = nums[0]

        # Iterate from the second element
        for i in range(1, len(nums)):
            curr = nums[i]
            
            # We need to calculate the next max_so_far and min_so_far.
            # The next max/min product can be:
            # 1. The current number itself (starting a new subarray).
            # 2. current_num * max_so_far (extending the previous max product).
            # 3. current_num * min_so_far (extending the previous min product - crucial for negative numbers).
            
            # Store the old max_so_far because it's needed for calculating min_so_far
            # after max_so_far itself has been updated.
            temp_max_so_far = max_so_far 

            max_so_far = max(curr, temp_max_so_far * curr, min_so_far * curr)
            min_so_far = min(curr, temp_max_so_far * curr, min_so_far * curr)
            
            # Update the overall maximum product
            overall_max_product = max(overall_max_product, max_so_far)
            
        return overall_max_product

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([2,3,-2,4], 6),
        ([-2,0,-1], 0),
        ([-2], -2),
        ([0], 0),
        ([3,-1,4], 4),
        ([-2,-3,-4], 24), # (-2*-3 = 6, 6*-4 = -24). Overall max is 6 (from [-2,-3])
        ([2,-5,-2,-4,3], 240), # (2*-5*-2 = 20, 20*-4 = -80, -80*3 = -240). (2*-5*-2*-4 = 80, 80*3 = 240)
        ([0,2,3,-2,4,0], 6), # Contains zeros
        ([-1,-2,-9,-6], 108), # (108)
        ([7,-2,-4], 56) # (7 * -2 * -4 = 56)
    ]

    for nums, expected_output in test_cases:
        result = solution.maxProduct(list(nums)) # Pass a copy of the list
        print(f"Input: {nums}")
        print(f"Output: {result}")
        print(f"Expected: {expected_output}")
        print(f"Status: {'Pass' if result == expected_output else 'Fail'}")
        print("-" * 30)