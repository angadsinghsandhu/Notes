# File: Leetcode/Solutions/LeetCode/2091_Removing_Minimum_and_Maximum_From_Array.py

"""
Problem Number: 2091
Problem Name: Removing Minimum and Maximum From Array
Difficulty: Medium
Tags: Array, Math, Two Pointers
Company (Frequency): (premium)
Leetcode Link: https://leetcode.com/problems/removing-minimum-and-maximum-from-array/

DESCRIPTION

You are given a 0-indexed array of distinct integers nums.

There is an element in nums with the lowest value and an element with the highest value. We call them the minimum and maximum, respectively. Your goal is to remove both these elements from the array.

A deletion is defined as either removing an element from the front of the array or removing an element from the back of the array.

Return the minimum number of deletions it would take to remove both the minimum and maximum element from the array.

---

#### Example 1:

Input:
nums = [2,10,7,5,4,1,8,6]

Output:

5

Explanation:
The minimum element is at index 5 (value 1), the maximum at index 1 (value 10).
Remove 2 from front and 3 from back → 2 + 3 = 5.

#### Example 2:

Input:

nums = [0,-4,19,1,8,-2,-3,5]

Output:
3

Explanation:
The minimum at index 1 (value -4), maximum at index 2 (value 19).
Remove 3 from front → 3 deletions.

#### Example 3:

Input:
nums = [101]

Output:

1

Explanation:
Only one element, so it is both min and max. One deletion removes it.

#### Constraints:

- $1 \leq nums.length \leq 10^5$
- $-10^5 \leq nums[i] \leq 10^5$
- All integers in nums are distinct.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - Identify the indices of the minimum and maximum elements.
    - Brute Force: Try every possible split of deletions between front and back.
    For k = 1 to n deletions total, for x deletions from front and (k-x) from back,
    check if both min and max have been removed.
    Time Complexity: O(n^2), Space Complexity: O(1).
    - Optimized:
    Consider just four scenarios (all front, all back, min front & max back, max front & min back)
    and take the minimum.
    
    Time Complexity: O(n), Space Complexity: O(1).
    """

    def brute_force(self, nums: List[int]) -> int:
        """
        Brute-force by simulating all possible ways to delete k elements
        from front/back until both min and max are gone.
        """
        n = len(nums)
        # find positions of min and max
        i_min = nums.index(min(nums))
        i_max = nums.index(max(nums))
        for k in range(1, n+1):
            for front in range(k+1):
                back = k - front
                # removed indices are [0..front-1] from front and [n-back..n-1] from back
                removed = lambda idx: idx < front or idx >= n - back
                if removed(i_min) and removed(i_max):
                    return k
        return n  # fallback, shouldn't reach here

    def optimized(self, nums: List[int]) -> int:
        """
        Compute directly by evaluating the 4 possible removal strategies:
        1) remove both from front
        2) remove both from back
        3) remove min from front, max from back
        4) remove max from front, min from back
        """
        n = len(nums)
        i_min = nums.index(min(nums))
        i_max = nums.index(max(nums))
        # strategy 1: both from front => max(i_min, i_max) + 1 deletions
        front_both = max(i_min, i_max) + 1
        # strategy 2: both from back => max(n - i_min, n - i_max)
        back_both = max(n - i_min, n - i_max)
        # strategy 3: min front & max back => (i_min + 1) + (n - i_max)
        min_front_max_back = (i_min + 1) + (n - i_max)
        # strategy 4: max front & min back => (i_max + 1) + (n - i_min)
        max_front_min_back = (i_max + 1) + (n - i_min)
        return min(front_both, back_both, min_front_max_back, max_front_min_back)

if __name__ == "__main__":
    solution = Solution()


# Example test cases
print(solution.brute_force([2,10,7,5,4,1,8,6]))   # Output: 5
print(solution.optimized([2,10,7,5,4,1,8,6]))     # Output: 5

print(solution.brute_force([0,-4,19,1,8,-2,-3,5]))  # Output: 3
print(solution.optimized([0,-4,19,1,8,-2,-3,5]))    # Output: 3

print(solution.brute_force([101]))  # Output: 1
print(solution.optimized([101]))    # Output: 1

# Additional tests
print(solution.optimized([1, 2, 3, 4, 5]))       # min at front, max at back: 1+1=2
print(solution.optimized([5, 1, 2, 3, 4]))       # max front, min at idx1: min(max_front,min_back)=?
print(solution.optimized([3, 1, 5, 2, 4]))       # mixed positions