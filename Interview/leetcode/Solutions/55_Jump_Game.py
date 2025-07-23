# File: Leetcode/Solutions/55_Jump_Game.py

"""
Problem Number: 55
Problem Name: Jump Game
Difficulty: Medium
Tags: Array, Dynamic Programming, Greedy
Company (Frequency):
Leetcode Link: <https://leetcode.com/problems/jump-game/description/>

DESCRIPTION

You are given an integer array "nums". You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return "true" if you can reach the last index, or "false" otherwise.

---

#### Example 1:

Input:
nums = [2,3,1,1,4]

Output:
true

Explanation:
Jump 1 step from index 0 to 1, then 3 steps to the last index.

---

#### Example 2:

Input:
nums = [3,2,1,0,4]

Output:
false

Explanation:
You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.

---

#### Constraints:

* 1 <= nums.length <= 10^4
* 0 <= nums[i] <= 10^5
"""

class Solution:
    """
    Thought Process:
    - We need to determine if it's possible to walk from the first index to the last, given each value as the max jump length.
    - A dynamic programming approach can record reachability of each index.
    - An optimized greedy approach tracks the furthest reachable index as we iterate.

    Input:
        nums: List[int] - The input array of non-negative integers.

    Output:
        bool - True if the last index is reachable, False otherwise.
    """

    def dp_solution(self, nums: list[int]) -> bool:
        """
        Approach:
        - Maintain a boolean array `reachable` where reachable[i] is True if index i can be reached.
        - Initialize reachable[0] = True.
        - For each i, if reachable[i] is True, mark all j in range(i+1, i+nums[i]+1) as reachable.
        - Finally, return reachable[-1].

        T.C.: O(n^2) in the worst case
        S.C.: O(n)
        """
        n = len(nums)
        reachable = [False] * n
        reachable[0] = True

        for i in range(n):
            if not reachable[i]:
                continue
            max_jump = nums[i]
            for j in range(i + 1, min(n, i + max_jump + 1)):
                reachable[j] = True
            if reachable[-1]:
                return True

        return reachable[-1]

    def greedy_solution(self, nums: list[int]) -> bool:
        """
        Approach:
        - Keep track of `farthest`, the furthest index we can reach so far.
        - For each index i up to farthest, update farthest = max(farthest, i + nums[i]).
        - If at any point farthest >= last index, return True.
        - If i exceeds farthest, we can't move further and return False.

        T.C.: O(n)
        S.C.: O(1)
        """
        farthest = 0
        last_index = len(nums) - 1

        for i, jump in enumerate(nums):
            if i > farthest:
                # Can't reach this position
                return False
            farthest = max(farthest, i + jump)
            if farthest >= last_index:
                return True

        return False

# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

# Example 1
print(solution.dp_solution([2, 3, 1, 1, 4]))      # Output: True
print(solution.greedy_solution([2, 3, 1, 1, 4]))  # Output: True

# Example 2
print(solution.dp_solution([3, 2, 1, 0, 4]))      # Output: False
print(solution.greedy_solution([3, 2, 1, 0, 4]))  # Output: False