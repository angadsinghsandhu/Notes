# File: Leetcode/Solutions/LeetCode/2149_Rearrange_Array_Elements_by_Sign.py

"""
Problem Number: 2149
Problem Name: Rearrange Array Elements by Sign
Difficulty: Medium
Tags: Array, Two Pointers, Simulation
Company (Frequency): (premium)
Leetcode Link: https://leetcode.com/problems/rearrange-array-elements-by-sign/

DESCRIPTION

You are given a 0-indexed integer array nums of even length consisting of an equal number of positive and negative integers.

You should return the array of nums such that the array follows the given conditions:

1. Every consecutive pair of integers have opposite signs.
2. For all integers with the same sign, the order in which they were present in nums is preserved.
3. The rearranged array begins with a positive integer.

Return the modified array after rearranging the elements to satisfy the aforementioned conditions.

---

#### Example 1:
Input:
nums = [3,1,-2,-5,2,-4]

Output:
[3,-2,1,-5,2,-4]

#### Example 2:

Input:
nums = [-1,1]

Output:
[1,-1]

#### Constraints:

* `2 <= nums.length <= 2 * 10^5`
* `nums.length` is even.
* `1 <= |nums[i]| <= 10^5`
* `nums` consists of an equal number of positive and negative integers.
* It is *not* required to do the modifications in-place.
"""
from typing import List

class Solution:
    """
    Thought Process:
    \- Brute Force: Separate positives and negatives into two lists, then interleave them.
    \- Optimized: Place positives and negatives directly into correct positions in result array using index pointers.
    """

    def brute_force(self, nums: List[int]) -> List[int]:
        """
        Approach:
        - Extract positives and negatives preserving order.
        - Build result by alternating from positives and negatives.

        T.C.: O(n)
        S.C.: O(n)
        """
        positives = [x for x in nums if x > 0]
        negatives = [x for x in nums if x < 0]
        result: List[int] = []
        for p, n in zip(positives, negatives):
            result.append(p)
            result.append(n)
        return result

    def optimized(self, nums: List[int]) -> List[int]:
        """
        Approach:
        - Allocate result list of same length.
        - Use two pointers: pos_idx at 0 for positives, neg_idx at 1 for negatives.
        - Single pass: place each number in correct position and increment pointer by 2.

        T.C.: O(n)
        S.C.: O(n)
        """
        n = len(nums)
        res = [0] * n
        pos_idx, neg_idx = 0, 1
        for x in nums:
            if x > 0:
                res[pos_idx] = x
                pos_idx += 2
            else:
                res[neg_idx] = x
                neg_idx += 2
        return res

if __name__ == "__main__":
    solution = Solution()

# Example 1
nums1 = [3,1,-2,-5,2,-4]
print(solution.brute_force(nums1))   # [3,-2,1,-5,2,-4]
print(solution.optimized(nums1))     # [3,-2,1,-5,2,-4]

# Example 2
nums2 = [-1,1]
print(solution.brute_force(nums2))   # [1,-1]
print(solution.optimized(nums2))     # [1,-1]

# Additional test
nums3 = [4,-1,-2,3,-5,2]
# positives: [4,3,2], negatives: [-1,-2,-5]
print(solution.brute_force(nums3))   # [4,-1,3,-2,2,-5]
print(solution.optimized(nums3))     # [4,-1,3,-2,2,-5]
