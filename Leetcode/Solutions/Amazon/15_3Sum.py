# TODO: revisit

# File: Leetcode/Solutions/Amazon/15_3Sum.py

"""
Problem Number: 15
Problem Name: 3Sum
Difficulty: Medium
Tags: Array, Two Pointers, Sorting
Company (Frequency): Amazon (78)
Leetcode Link: <https://leetcode.com/problems/3sum/description/>

DESCRIPTION

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

---

#### Example 1:
**Input:**
```plaintext
nums = [-1, 0, 1, 2, -1, -4]
```

**Output:**
```plaintext
[[-1, -1, 2], [-1, 0, 1]]
```

**Explanation:**  
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.  
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.  
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.  
The distinct triplets are `[-1, 0, 1]` and `[-1, -1, 2]`.  
Notice that the order of the output and the order of the triplets does not matter.

#### Example 2:
**Input:**
```plaintext
nums = [0, 1, 1]
```

**Output:**
```plaintext
[]
```

**Explanation:**  
The only possible triplet does not sum up to 0.

#### Example 3:
**Input:**
```plaintext
nums = [0, 0, 0]
```

**Output:**
```plaintext
[[0, 0, 0]]
```

**Explanation:**  
The only possible triplet sums up to 0.

#### Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding all unique triplets in the array that sum to zero.
    - A brute force solution would involve three nested loops, but it is inefficient (O(n^3)).
    - An optimized solution uses sorting and the two-pointer technique to achieve O(n^2) time complexity.

    Input:
        nums: List[int] - The input array of integers.

    Output:
        List[List[int]] - A list of all unique triplets that sum to zero.
    """

    def brute_force_solution(self, nums: List[int]) -> List[List[int]]:
        """
        Approach:
        - Use three nested loops to check all possible triplets.
        - Ensure that the triplets are unique by using a set to store results.

        T.C.: O(n^3)
        S.C.: O(n) for storing results.
        """
        n = len(nums)
        result = set()

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                        result.add(triplet)

        return [list(triplet) for triplet in result]

    def optimized_solution(self, nums: List[int]) -> List[List[int]]:
        """
        Approach:
        - Sort the array to make it easier to avoid duplicates and use the two-pointer technique.
        - Iterate through the array and use two pointers to find triplets that sum to zero.
        - Skip duplicates to ensure unique triplets.

        T.C.: O(n^2)
        S.C.: O(1) (ignoring the space required for the output).
        """
        nums.sort()
        n = len(nums)
        result = []

        for i in range(n - 2):
            # Skip duplicates for the first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    # Skip duplicates for the second and third elements
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1

        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.brute_force_solution([-1, 0, 1, 2, -1, -4]))  # Output: [[-1, -1, 2], [-1, 0, 1]]
    print(solution.optimized_solution([0, 1, 1]))  # Output: []
    print(solution.optimized_solution([0, 0, 0]))  # Output: [[0, 0, 0]]