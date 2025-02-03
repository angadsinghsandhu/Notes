# TODO: revisit

# File: Leetcode/Solutions/128_Longest_Consecutive_Sequence.py

"""
Problem Number: 128
Problem Name: Longest Consecutive Sequence
Difficulty: Medium
Tags: Array, Hash Table, Union Find
Company (Frequency): Amazon (20), Microsoft (15), Google (10)
Leetcode Link: https://leetcode.com/problems/longest-consecutive-sequence/description/

DESCRIPTION

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

---

#### Example 1:
**Input:**
```plaintext
nums = [100, 4, 200, 1, 3, 2]
```

**Output:**
```plaintext
4
```

**Explanation:**  
The longest consecutive elements sequence is `[1, 2, 3, 4]`. Therefore, its length is 4.

#### Constraints:
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires finding the longest sequence of consecutive numbers in an unsorted array.
    - A brute-force approach involves sorting the array and then finding the longest sequence, but this is O(n log n).
    - An optimized approach uses a hash set to achieve O(n) time complexity by checking for sequences efficiently.

    Input:
        nums: List[int] - An unsorted list of integers.

    Output:
        int - The length of the longest consecutive sequence.
    """

    def brute_force_solution(self, nums: List[int]) -> int:
        """
        Approach:
        - Sort the array and iterate through it to find the longest consecutive sequence.

        T.C.: O(n log n) - Due to sorting.
        S.C.: O(1) - No additional space used (ignoring the space used by sorting).
        """
        if not nums:
            return 0

        nums.sort()
        longest_streak = 1
        current_streak = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                if nums[i] == nums[i - 1] + 1:
                    current_streak += 1
                else:
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1

        return max(longest_streak, current_streak)

    def optimized_solution(self, nums: List[int]) -> int:
        """
        Approach:
        - Use a hash set to store all numbers for O(1) lookups.
        - Iterate through the array and for each number, check if it is the start of a sequence.
        - If it is the start, extend the sequence as far as possible and update the longest streak.

        T.C.: O(n) - Each number is visited at most twice.
        S.C.: O(n) - Space used by the hash set.
        """
        num_set = set(nums)
        longest_streak = 0

        for num in num_set:
            # Check if the current number is the start of a sequence
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1

                # Extend the sequence as far as possible
                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                # Update the longest streak
                longest_streak = max(longest_streak, current_streak)

        return longest_streak

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    nums1 = [100, 4, 200, 1, 3, 2]
    print(solution.brute_force_solution(nums1))  # Output: 4
    print(solution.optimized_solution(nums1))    # Output: 4

    # Test case 2
    nums2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    print(solution.brute_force_solution(nums2))  # Output: 9
    print(solution.optimized_solution(nums2))    # Output: 9