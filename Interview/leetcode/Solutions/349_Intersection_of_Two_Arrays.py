# File: Leetcode/Solutions/LeetCode/349_Intersection_of_Two_Arrays.py

"""
Problem Number: 349
Problem Name: Intersection of Two Arrays
Difficulty: Easy
Tags: Array, Hash Table, Two Pointers, Binary Search, Sorting
Company (Frequency): (premium)
Leetcode Link: https://leetcode.com/problems/intersection-of-two-arrays/

DESCRIPTION

Given two integer arrays nums1 and nums2, return an array of their intersection.  
Each element in the result must be unique and you may return the result in any order.

---

#### Example 1:

Input:
nums1 = [1,2,2,1], nums2 = [2,2]

Output:
[2]

#### Example 2:

Input:
nums1 = [4,9,5], nums2 = [9,4,9,8,4]

Output:
[9,4]

Explanation: [4,9] is also accepted.

#### Constraints:

* `1 <= nums1.length, nums2.length <= 1000`
* `0 <= nums1[i], nums2[i] <= 1000`
"""

from typing import List

class Solution:
    """
    Thought Process:
    \- Brute Force: Compare every pair and collect unique matches.
    \- Optimized: Use Python set operations for O(n + m) time.
    """

    def brute_force(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Approach:
        - Nested loops to check each element in nums1 against nums2.
        - Use a set to avoid duplicates in the result.

        T.C.: O(n * m)
        S.C.: O(min(n, m))
        """
        result_set = set()
        for x in nums1:
            for y in nums2:
                if x == y:
                    result_set.add(x)
                    break
        return list(result_set)

    def optimized(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Approach:
        - Convert both lists to sets and compute their intersection.

        T.C.: O(n + m)
        S.C.: O(n + m)
        """
        set1 = set(nums1)
        set2 = set(nums2)
        return list(set1 & set2)
    
    def optimized_alternative(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Approach:
        - Use a single set to track unique elements from nums1.
        - Iterate through nums2 and check membership in the set.

        T.C.: O(n + m)
        S.C.: O(n)
        """
        result_set = set(nums1)
        return [num for num in set(nums2) if num in result_set]

if __name__ == "__main__":
    solution = Solution()

# Example 1
nums1, nums2 = [1,2,2,1], [2,2]
print(solution.brute_force(nums1, nums2))   # [2]
print(solution.optimized(nums1, nums2))     # [2]

# Example 2
nums1, nums2 = [4,9,5], [9,4,9,8,4]
print(solution.brute_force(nums1, nums2))   # [9,4] or [4,9]
print(solution.optimized(nums1, nums2))     # [9,4] or [4,9]

# Additional tests
print(solution.brute_force([], [1,2,3]))    # []
print(solution.optimized([7,7,7], [7]))     # [7]
