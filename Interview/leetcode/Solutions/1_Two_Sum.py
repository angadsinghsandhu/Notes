# File: Leetcode/Solutions/1_Two_Sum.py

"""
Problem Number: 1
Problem Name: Two Sum
Difficulty: Easy
Tags: Array, Hash Table, Two-Pointer, Neetcode 150
Company (Frequency): Amazon (117)
Leetcode Link: <https://leetcode.com/problems/two-sum/description/>

DESCRIPTION

Given an array of integers `nums` and an integer `target`, return the **indices** of the two numbers such that they add up to `target`.

You may assume that each input has **exactly one solution**, and you may not use the same element twice.

The solution can be returned in any order.

---

#### Example 1:
**Input:**
```plaintext
nums = [2, 7, 11, 15], target = 9
```

**Output:**
```plaintext
[0, 1]
```

**Explanation:**  
`nums[0] + nums[1] = 2 + 7 = 9`  
Thus, we return `[0, 1]`.

#### Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.

"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding two indices such that their corresponding values in the array sum to the target value.
    - A brute force solution iterates through each pair (O(n^2)), but this is suboptimal.
    - Optimized solutions leverage hash tables for efficient lookups (O(n)).

    Input:
        nums: List[int] - Array of integers.
        target: int - Target sum value.

    Output:
        List[int] - Indices of the two numbers that add up to the target.
    """

    def brute_force_solution(self, nums: List[int], target: int) -> List[int]:
        """
        Approach:
        - Use two nested loops to check all possible pairs.
        
        T.C.: O(n^2)
        S.C.: O(1)
        """
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]

        # If no solution is found, raise an error (since the problem guarantees one solution)
        raise ValueError("No two sum solution exists")

    def optimized_solution(self, nums: List[int], target: int) -> List[int]:
        """
        Approach:
        - Use a hash table to store the complement of each number while iterating.
        - Check if the current number exists in the hash table, which would mean a pair is found.

        T.C.: O(n)
        S.C.: O(n)
        """
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i

        # If no solution is found, raise an error (since the problem guarantees one solution)
        raise ValueError("No two sum solution exists")

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.brute_force_solution([2, 7, 11, 15], 9))  # Output: [0, 1]
    print(solution.optimized_solution([3, 2, 4], 6))         # Output: [1, 2]
    print(solution.optimized_solution([3, 3], 6))           # Output: [0, 1]