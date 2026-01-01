# File: Leetcode/Solutions/152_Maximum_Product_Subarray.py

"""
Problem Number: 152
Problem Name: Maximum Product Subarray
Difficulty: Medium
Tags: Array, Dynamic Programming, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, Facebook
Leetcode Link: https://leetcode.com/problems/maximum-product-subarray/description/

DESCRIPTION

Given an integer array `nums`, find a subarray that has the largest product, and return the product.
The test cases are generated so that the answer will fit in a 32-bit integer.

---

#### Example 1:
Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.

---

#### Example 2:
Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

---

#### Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is similar to Kadane's Algorithm (Maximum Sum Subarray), but with a twist: products.
    - Because of negative numbers, a very small negative product can become the maximum product if multiplied by another negative number.
    - Therefore, at each step, we must keep track of both the maximum product AND the minimum product up to that point.
    - If we encounter a 0, it resets the product chain.

    Approach Hierarchy:
    1. Brute Force: O(n^2) - Calculate every possible subarray product.
    2. Dynamic Programming: O(n) time, O(1) space - Keep track of current min/max.
    3. Prefix/Suffix Product: O(n) - The max product must be a prefix or suffix product (ignoring zeros).
    """

    def max_product_brute_force(self, nums: List[int]) -> int:
        """
        Approach: Brute Force
        T.C.: O(n^2)
        S.C.: O(1)
        """
        res = nums[0]
        for i in range(len(nums)):
            cur = 1
            for j in range(i, len(nums)):
                cur *= nums[j]
                res = max(res, cur)
        return res

    def max_product_dp(self, nums: List[int]) -> int:
        """
        Approach: Optimized Dynamic Programming (Kadane's Variation)
        - We maintain curMax and curMin.
        - When we hit a negative number, curMax and curMin essentially swap their roles after multiplication.
        
        T.C.: O(n)
        S.C.: O(1)
        """
        res = max(nums)
        curMin, curMax = 1, 1

        

        for n in nums:
            if n == 0:
                curMin, curMax = 1, 1
                continue
            
            # Temporary storage for curMax because it's used to calculate curMin
            tmp = curMax * n
            curMax = max(n * curMax, n * curMin, n)
            curMin = min(tmp, n * curMin, n)
            res = max(res, curMax)
            
        return res

    def max_product_prefix_suffix(self, nums: List[int]) -> int:
        """
        Approach: Two-Pass (Prefix and Suffix)
        - The maximum product subarray must be either a prefix or a suffix of a sub-segment 
          divided by zeros.
        
        T.C.: O(n)
        S.C.: O(1)
        """
        res = nums[0]
        prefix = 0
        suffix = 0
        n = len(nums)
        
        for i in range(n):
            # If product becomes 0, reset to 1 (conceptually starting a new subarray)
            prefix = (prefix or 1) * nums[i]
            suffix = (suffix or 1) * nums[n - 1 - i]
            res = max(res, prefix, suffix)
            
        return res

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        [2, 3, -2, 4],
        [-2, 0, -1],
        [-2, 3, -4],
        [0, 2]
    ]

    for nums in test_cases:
        print(f"Input: {nums}")
        print(f"DP Result:            {solution.max_product_dp(nums)}")
        print(f"Prefix/Suffix Result: {solution.max_product_prefix_suffix(nums)}")
        print("-" * 35)

    print(f"result: {solution.max_product_dp(test_cases[0])}")