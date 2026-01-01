# File: Leetcode/Solutions/1143_Longest_Common_Subsequence.py

"""
Problem Number: 1143
Problem Name: Longest Common Subsequence
Difficulty: Medium
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Google, Microsoft, Facebook
Leetcode Link: https://leetcode.com/problems/longest-common-subsequence/description/

DESCRIPTION

Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.
For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.

---

#### Example 1:
Input: text1 = "abcde", text2 = "ace" 
Output: 3  
Explanation: The longest common subsequence is "ace" and its length is 3.

---

#### Example 2:
Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

---

#### Example 3:
Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.

---

#### Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - We compare characters of both strings.
    - If text1[i] == text2[j], we have found 1 matching character. The result is 1 + LCS of the remaining strings.
    - If text1[i] != text2[j], we have two choices:
        1. Skip character in text1 and find LCS(text1[i+1:], text2[j:])
        2. Skip character in text2 and find LCS(text1[i:], text2[j+1:])
    - We take the maximum of these two choices.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^(n+m))
    2. Memoization (Top-Down): O(n * m) time and space.
    3. Tabulation (Bottom-Up): O(n * m) time and space.
    4. Space Optimized DP: O(min(n, m)) space.
    """

    def lcs_recursive(self, text1: str, text2: str) -> int:
        """
        Approach: Pure Recursion
        T.C.: O(2^(n+m))
        S.C.: O(n + m)
        """
        def solve(i, j):
            if i == len(text1) or j == len(text2):
                return 0
            if text1[i] == text2[j]:
                return 1 + solve(i + 1, j + 1)
            else:
                return max(solve(i + 1, j), solve(i, j + 1))

        return solve(0, 0)

    def lcs_memoization(self, text1: str, text2: str) -> int:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        memo = {}

        def solve(i, j):
            if i == len(text1) or j == len(text2):
                return 0
            if (i, j) in memo:
                return memo[(i, j)]
            
            if text1[i] == text2[j]:
                memo[(i, j)] = 1 + solve(i + 1, j + 1)
            else:
                memo[(i, j)] = max(solve(i + 1, j), solve(i, j + 1))
            return memo[(i, j)]

        return solve(0, 0)

    def lcs_tabulation(self, text1: str, text2: str) -> int:
        """
        Approach: Bottom-Up DP (2D Grid)
        - Create a (m+1) x (n+1) matrix.
        - If characters match, move diagonally: 1 + dp[i+1][j+1].
        - If they don't, take max of right or down: max(dp[i+1][j], dp[i][j+1]).

        

        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        dp = [[0 for _ in range(len(text2) + 1)] for _ in range(len(text1) + 1)]

        for i in range(len(text1) - 1, -1, -1):
            for j in range(len(text2) - 1, -1, -1):
                if text1[i] == text2[j]:
                    dp[i][j] = 1 + dp[i + 1][j + 1]
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

        return dp[0][0]

    def lcs_optimized(self, text1: str, text2: str) -> int:
        """
        Approach: Space Optimized DP
        - We only ever need the current row and the next row.
        - Reduces space complexity significantly.

        T.C.: O(n * m)
        S.C.: O(m)
        """
        # Ensure text2 is the shorter string to optimize space further
        if len(text2) > len(text1):
            text1, text2 = text2, text1
            
        n, m = len(text1), len(text2)
        prev = [0] * (m + 1)

        for i in range(n - 1, -1, -1):
            curr = [0] * (m + 1)
            for j in range(m - 1, -1, -1):
                if text1[i] == text2[j]:
                    curr[j] = 1 + prev[j + 1]
                else:
                    curr[j] = max(prev[j], curr[j + 1])
            prev = curr

        return prev[0]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ("abcde", "ace"),
        ("abc", "abc"),
        ("abc", "def")
    ]

    for t1, t2 in test_cases:
        print(f"Text1: '{t1}', Text2: '{t2}'")
        print(f"Memoization: {solution.lcs_memoization(t1, t2)}")
        print(f"Tabulation:  {solution.lcs_tabulation(t1, t2)}")
        print(f"Optimized:   {solution.lcs_optimized(t1, t2)}")
        print("-" * 35)

    print(f"result: {solution.lcs_optimized(test_cases[0][0], test_cases[0][1])}")
