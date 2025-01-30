# File: Leetcode/Solutions/Amazon/53_Maximum_Subarray.py

"""
Problem Number: 53
Problem Name: Maximum Subarray
Difficulty: Medium
Tags: Array, Divide and Conquer, Dynamic Programming
Company (Frequency): Amazon (95)
Leetcode Link: <https://leetcode.com/problems/maximum-subarray/description/>

DESCRIPTION

Given an integer array `nums`, find the subarray with the largest sum and return its sum.

---

#### Example 1:
**Input:**
```plaintext
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
```

**Output:**
```plaintext
6
```

**Explanation:**  
The subarray `[4, -1, 2, 1]` has the largest sum `6`.

#### Example 2:
**Input:**
```plaintext
nums = [1]
```

**Output:**
```plaintext
1
```

**Explanation:**  
The subarray `[1]` has the largest sum `1`.

#### Example 3:
**Input:**
```plaintext
nums = [5, 4, -1, 7, 8]
```

**Output:**
```plaintext
23
```

**Explanation:**  
The subarray `[5, 4, -1, 7, 8]` has the largest sum `23`.

#### Constraints:
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

---

**Follow up:**  
If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding the contiguous subarray with the largest sum.
    - A brute force solution would involve checking all possible subarrays, but it is inefficient (O(n^2)).
    - Optimized solutions include Kadane's Algorithm (O(n)) and the Divide and Conquer approach (O(n log n)).

    Input:
        nums: List[int] - The input array of integers.

    Output:
        int - The sum of the subarray with the largest sum.
    """

    def brute_force_solution(self, nums: List[int]) -> int:
        """
        Approach:
        - Check all possible subarrays and calculate their sums.
        - Track the maximum sum found.

        T.C.: O(n^2)
        S.C.: O(1)
        """
        max_sum = float('-inf')
        n = len(nums)

        for i in range(n):
            current_sum = 0
            for j in range(i, n):
                current_sum += nums[j]
                max_sum = max(max_sum, current_sum)

        return max_sum

    def kadanes_algorithm(self, nums: List[int]) -> int:
        """
        Approach:
        - Use Kadane's Algorithm to find the maximum subarray sum in a single pass.
        - Maintain two variables: `current_sum` (sum of the current subarray) and `max_sum` (maximum sum found so far).
        - If `current_sum` becomes negative, reset it to the current element.

        T.C.: O(n)
        S.C.: O(1)
        """
        max_sum = float('-inf')
        current_sum = 0

        for num in nums:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum

    def divide_and_conquer_solution(self, nums: List[int]) -> int:
        """
        Approach:
        - Use the Divide and Conquer strategy to find the maximum subarray sum.
        - Divide the array into two halves and recursively find the maximum subarray sum in each half.
        - Also, find the maximum subarray sum that crosses the midpoint.
        - Return the maximum of the three sums.

        T.C.: O(n log n)
        S.C.: O(log n) (due to recursion stack)
        """
        def helper(left, right):
            if left == right:
                return nums[left]

            mid = (left + right) // 2

            # Maximum subarray sum in the left half
            left_max = helper(left, mid)

            # Maximum subarray sum in the right half
            right_max = helper(mid + 1, right)

            # Maximum subarray sum crossing the midpoint
            cross_max = cross_sum(left, right, mid)

            return max(left_max, right_max, cross_max)

        def cross_sum(left, right, mid):
            # Calculate the maximum sum starting from mid and extending to the left
            left_sum = float('-inf')
            current_sum = 0
            for i in range(mid, left - 1, -1):
                current_sum += nums[i]
                left_sum = max(left_sum, current_sum)

            # Calculate the maximum sum starting from mid + 1 and extending to the right
            right_sum = float('-inf')
            current_sum = 0
            for i in range(mid + 1, right + 1):
                current_sum += nums[i]
                right_sum = max(right_sum, current_sum)

            return left_sum + right_sum

        return helper(0, len(nums) - 1)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.brute_force_solution([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Output: 6
    print(solution.kadanes_algorithm([1]))  # Output: 1
    print(solution.divide_and_conquer_solution([5, 4, -1, 7, 8]))  # Output: 23