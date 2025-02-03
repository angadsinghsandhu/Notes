# File: Leetcode/Solutions/238_Product_of_Array_Except_Self.py

"""
Problem Number: 238
Problem Name: Product of Array Except Self
Difficulty: Medium
Tags: Array, Prefix Sum
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/product-of-array-except-self/description/

DESCRIPTION

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

---

#### Example 1:
**Input:**
```plaintext
nums = [1, 2, 3, 4]
```

**Output:**
```plaintext
[24, 12, 8, 6]
```

**Explanation:**  
- `answer[0] = 2 * 3 * 4 = 24`
- `answer[1] = 1 * 3 * 4 = 12`
- `answer[2] = 1 * 2 * 4 = 8`
- `answer[3] = 1 * 2 * 3 = 6`

#### Example 2:
**Input:**
```plaintext
nums = [-1, 1, 0, -3, 3]
```

**Output:**
```plaintext
[0, 0, 9, 0, 0]
```

**Explanation:**  
- Any element multiplied by 0 results in 0.
- The product of elements except `nums[2]` is `-1 * 1 * -3 * 3 = 9`.

#### Constraints:
- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

#### Follow-up:
Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires calculating the product of all elements in the array except the current element.
    - A brute-force approach would involve nested loops, but this is inefficient.
    - An optimized approach uses prefix and suffix products to compute the result in O(n) time without using division.

    Input:
        nums: List[int] - The input array of integers.

    Output:
        List[int] - An array where each element is the product of all elements in `nums` except the current element.
    """

    def brute_force_solution(self, nums: List[int]) -> List[int]:
        """
        Approach:
        - For each element in `nums`, calculate the product of all other elements using nested loops.

        T.C.: O(n^2) - Nested loops for each element.
        S.C.: O(1) - No additional space used (excluding the output array).
        """
        n = len(nums)
        answer = [1] * n

        for i in range(n):
            for j in range(n):
                if i != j:
                    answer[i] *= nums[j]

        return answer

    def optimized_solution(self, nums: List[int]) -> List[int]:
        """
        Approach:
        - Use prefix and suffix products to compute the result in O(n) time.
        - First, compute the prefix product (product of all elements to the left of the current element).
        - Then, compute the suffix product (product of all elements to the right of the current element).
        - Multiply the prefix and suffix products to get the final result.

        T.C.: O(n) - Two passes through the array.
        S.C.: O(1) - Constant space used (excluding the output array).
        """
        n = len(nums)
        answer = [1] * n

        # Compute prefix products
        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= nums[i]

        # Compute suffix products and multiply with prefix products
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]

        return answer

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    nums1 = [1, 2, 3, 4]
    print(solution.brute_force_solution(nums1))  # Output: [24, 12, 8, 6]
    print(solution.optimized_solution(nums1))    # Output: [24, 12, 8, 6]

    # Test case 2
    nums2 = [-1, 1, 0, -3, 3]
    print(solution.brute_force_solution(nums2))  # Output: [0, 0, 9, 0, 0]
    print(solution.optimized_solution(nums2))    # Output: [0, 0, 9, 0, 0]
