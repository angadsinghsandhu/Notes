# File: Leetcode/Solutions/Amazon/45_Jump_Game_II.py

"""
Problem Number: 45
Problem Name: Jump Game II
Difficulty: Medium
Tags: Array, Dynamic Programming, Greedy
Company (Frequency): Not explicitly stated, but common in top tech companies like Amazon (implied by file path)
Leetcode Link: <https://leetcode.com/problems/jump-game-ii/description/>

DESCRIPTION

You are given a 0-indexed array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.
Each element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at `nums[i]`, you can jump to any `nums[i + j]` where:
0 <= j <= nums[i]` and
`i + j < n`
Return the minimum number of jumps to reach `nums[n - 1]`. The test cases are generated such that you can reach `nums[n - 1]`.

---

#### Example 1:

Input:
nums = [2,3,1,1,4]

Output:
2

Explanation:
The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.

---

#### Example 2:

Input:
nums = [2,3,0,1,4]

Output:
2

---

#### Constraints:

- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 1000
- It's guaranteed that you can reach `nums[n - 1]`.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem asks for the minimum number of jumps to reach the last index. This often suggests a Breadth-First Search (BFS) like approach or a greedy strategy.
    - A direct BFS would involve exploring all reachable indices from the current position, which could be inefficient if `nums[i]` is large.
    - The greedy approach seems more promising: from the current position, we want to make a jump that allows us to reach furthest. However, the "furthest" doesn't necessarily mean the next jump should be `nums[i]`. It means, among all reachable positions from the current jump, which one allows us to extend our reach the most with the *next* jump?
    - We can keep track of the `current_jump_end` (the furthest index reachable with the current number of jumps) and `farthest_reach` (the furthest index we can reach with one more jump from any point within the current jump's range).

    Input:
        nums: List[int] - The array of integers representing jump lengths.

    Output:
        int - The minimum number of jumps.
    """

    def greedy_solution(self, nums: List[int]) -> int:
        """
        Approach: Greedy (Level by Level BFS-like)
        - This solution is optimal with O(n) time complexity and O(1) space complexity.
        - We iterate through the array, keeping track of the `current_jump_end` (the maximum index reachable with the current number of jumps) and `farthest_reach` (the maximum index we can reach from any point within the current jump's span).
        - When we reach `current_jump_end`, it means we've completed one jump, so we increment `jumps` and update `current_jump_end` to `farthest_reach`.
        - The `farthest_reach` is continuously updated by considering `i + nums[i]` for each `i`.

        T.C.: O(n)
        S.C.: O(1)
        """
        n = len(nums)
        if n <= 1:
            return 0

        jumps = 0
        current_jump_end = 0  # The farthest index reachable with the current number of jumps
        farthest_reach = 0    # The maximum index we can reach from any point within current_jump_end

        # Iterate up to, but not including, the last element.
        # If we are at the last element, we don't need to jump anymore.
        for i in range(n - 1):
            # Update the farthest index reachable from the current position `i`
            farthest_reach = max(farthest_reach, i + nums[i])

            # If we have reached the end of the current jump's range
            if i == current_jump_end:
                jumps += 1
                current_jump_end = farthest_reach
                # If current_jump_end has reached or surpassed the last index,
                # we've found the minimum jumps. This check can be optimized
                # as the loop naturally handles this by stopping at n-1.
                # However, an explicit check can short-circuit if the last jump
                # lands exactly on the last index or beyond.
                if current_jump_end >= n - 1:
                    break

        return jumps

    def dynamic_programming_solution(self, nums: List[int]) -> int:
        """
        Approach: Dynamic Programming (Less optimal for this problem)
        - `dp[i]` represents the minimum number of jumps needed to reach index `i`.
        - Initialize `dp[0] = 0` and `dp[i] = infinity` for `i > 0`.
        - For each `i` from `1` to `n-1`:
            - For each `j` from `0` to `i-1`:
                - If `j + nums[j] >= i` (meaning we can reach `i` from `j`):
                    - `dp[i] = min(dp[i], dp[j] + 1)`
        - Return `dp[n-1]`.
        - This approach is correct but has a higher time complexity due to nested loops.

        T.C.: O(n^2) (can be optimized to O(n) with careful state management, but then it becomes similar to greedy)
        S.C.: O(n)
        """
        n = len(nums)
        if n <= 1:
            return 0

        dp = [float('inf')] * n
        dp[0] = 0

        for i in range(1, n):
            for j in range(i):
                if j + nums[j] >= i:
                    dp[i] = min(dp[i], dp[j] + 1)
                    # Optimization: If we find a way to reach `i` from `j`,
                    # and `dp[j]` is already known, we can potentially break
                    # inner loop if we are looking for the *first* such `j`
                    # that can reach `i` with min jumps.
                    # However, in DP, we need to check all `j`s to find the global min.
                    # The greedy solution implicitly handles this more efficiently.
        return dp[n-1]


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    nums1 = [2,3,1,1,4]
    expected1 = 2

    # Using Greedy Solution
    result1_greedy = solution.greedy_solution(list(nums1))
    print(f"Greedy Solution for {nums1}: {result1_greedy} (Expected: {expected1})")

    # Using Dynamic Programming Solution (less efficient for this problem)
    result1_dp = solution.dynamic_programming_solution(list(nums1))
    print(f"DP Solution for {nums1}: {result1_dp} (Expected: {expected1})")
    print("-" * 20)

    # Test Case 2
    nums2 = [2,3,0,1,4]
    expected2 = 2

    # Using Greedy Solution
    result2_greedy = solution.greedy_solution(list(nums2))
    print(f"Greedy Solution for {nums2}: {result2_greedy} (Expected: {expected2})")

    # Using Dynamic Programming Solution
    result2_dp = solution.dynamic_programming_solution(list(nums2))
    print(f"DP Solution for {nums2}: {result2_dp} (Expected: {expected2})")
    print("-" * 20)

    # Additional Test Case: Large jumps
    nums3 = [5,9,3,2,1,0,2,3,3,1,0,0]
    expected3 = 3 # 5->9 (index 1) -> 2 or 3 (index 3 or 4) -> 0 (index 11)
    result3_greedy = solution.greedy_solution(list(nums3))
    print(f"Greedy Solution for {nums3}: {result3_greedy} (Expected: {expected3})")
    result3_dp = solution.dynamic_programming_solution(list(nums3))
    print(f"DP Solution for {nums3}: {result3_dp} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Single element
    nums4 = [0]
    expected4 = 0
    result4_greedy = solution.greedy_solution(list(nums4))
    print(f"Greedy Solution for {nums4}: {result4_greedy} (Expected: {expected4})")
    result4_dp = solution.dynamic_programming_solution(list(nums4))
    print(f"DP Solution for {nums4}: {result4_dp} (Expected: {expected4})")
    print("-" * 20)

    # Additional Test Case: Two elements
    nums5 = [1,1]
    expected5 = 1
    result5_greedy = solution.greedy_solution(list(nums5))
    print(f"Greedy Solution for {nums5}: {result5_greedy} (Expected: {expected5})")
    result5_dp = solution.dynamic_programming_solution(list(nums5))
    print(f"DP Solution for {nums5}: {result5_dp} (Expected: {expected5})")
    print("-" * 20)