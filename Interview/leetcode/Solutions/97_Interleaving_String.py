# File: Leetcode/Solutions/97_Interleaving_String.py

"""
Problem Number: 97
Problem Name: Interleaving String
Difficulty: Medium
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Google, Microsoft, Facebook
Leetcode Link: https://leetcode.com/problems/interleaving-string/description/

DESCRIPTION

Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed by an interleaving of `s1` and `s2`.

An interleaving of two strings s and t is a configuration where s and t are divided into n and m substrings respectively, such that:
- s = s1 + s2 + ... + sn
- t = t1 + t2 + ... + tm
- |n - m| <= 1
- The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...

Note: a + b is the concatenation of strings a and b.

---

#### Example 1:
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true

---

#### Example 2:
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: false

---

#### Constraints:
- 0 <= s1.length, s2.length <= 100
- 0 <= s3.length <= 200
- s1, s2, and s3 consist of lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - We need to match characters of s3 using characters from s1 and s2 in order.
    - If the current character of s3 matches the current character of s1, we can try to move forward in s1.
    - If it matches s2, we can try to move forward in s2.
    - If it matches both, we have a branch in our decision tree, suggesting DP or Memoization.
    - Basic check: len(s1) + len(s2) must equal len(s3).

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^(n+m))
    2. Memoization (Top-Down): O(n * m) time and space.
    3. Tabulation (Bottom-Up): O(n * m) time and space.
    4. Space Optimized DP: O(m) space.
    """

    def is_interleave_memo(self, s1: str, s2: str, s3: str) -> bool:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        if len(s1) + len(s2) != len(s3):
            return False
        
        memo = {}

        def dfs(i, j):
            # i is index in s1, j is index in s2
            # index in s3 is always (i + j)
            if i == len(s1) and j == len(s2):
                return True
            if (i, j) in memo:
                return memo[(i, j)]

            # Check if we can take from s1
            if i < len(s1) and s1[i] == s3[i + j] and dfs(i + 1, j):
                return True
            
            # Check if we can take from s2
            if j < len(s2) and s2[j] == s3[i + j] and dfs(i, j + 1):
                return True
            
            memo[(i, j)] = False
            return False

        return dfs(0, 0)

    def is_interleave_tabulation(self, s1: str, s2: str, s3: str) -> bool:
        """
        Approach: Bottom-Up DP (2D Table)
        - dp[i][j] represents if s1[i:] and s2[j:] can form s3[i+j:].
        
        

        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        if len(s1) + len(s2) != len(s3):
            return False

        # dp[i][j] = can we interleave s1[i:] and s2[j:] to get s3[i+j:]
        dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        dp[len(s1)][len(s2)] = True

        for i in range(len(s1), -1, -1):
            for j in range(len(s2), -1, -1):
                if i < len(s1) and s1[i] == s3[i + j] and dp[i + 1][j]:
                    dp[i][j] = True
                if j < len(s2) and s2[j] == s3[i + j] and dp[i][j + 1]:
                    dp[i][j] = True
        
        return dp[0][0]

    def is_interleave_optimized(self, s1: str, s2: str, s3: str) -> bool:
        """
        Approach: Space Optimized DP
        - We only need the previous row (or column) to calculate the current state.
        T.C.: O(n * m)
        S.C.: O(m)
        """
        if len(s1) + len(s2) != len(s3):
            return False

        dp = [False] * (len(s2) + 1)
        dp[len(s2)] = True

        for i in range(len(s1), -1, -1):
            for j in range(len(s2), -1, -1):
                # Update current state based on "below" (previous i) and "right" (current i, next j)
                res = False
                if i < len(s1) and s1[i] == s3[i + j] and dp[j]:
                    res = True
                if j < len(s2) and s2[j] == s3[i + j] and dp[j + 1]:
                    res = True
                dp[j] = res
                # Edge case: for the very last cell (len1, len2), we manually set True
                if i == len(s1) and j == len(s2):
                    dp[j] = True
                    
        return dp[0]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ("aabcc", "dbbca", "aadbbcbcac"),
        ("aabcc", "dbbca", "aadbbbaccc"),
        ("", "", "")
    ]

    for s1, s2, s3 in test_cases:
        print(f"s1: '{s1}', s2: '{s2}', s3: '{s3}'")
        print(f"Memoization: {solution.is_interleave_memo(s1, s2, s3)}")
        print(f"Tabulation:  {solution.is_interleave_tabulation(s1, s2, s3)}")
        print(f"Optimized:   {solution.is_interleave_optimized(s1, s2, s3)}")
        print("-" * 35)

    print(f"result: {solution.is_interleave_optimized(test_cases[0][0], test_cases[0][1], test_cases[0][2])}")
