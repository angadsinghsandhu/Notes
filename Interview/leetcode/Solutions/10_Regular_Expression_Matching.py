# File: Leetcode/Solutions/10_Regular_Expression_Matching.py

"""
Problem Number: 10
Problem Name: Regular Expression Matching
Difficulty: Hard
Tags: String, Dynamic Programming, Recursion, NeetCode 150
Company (Frequency): Google, Amazon, Facebook, Microsoft, Apple
Leetcode Link: https://leetcode.com/problems/regular-expression-matching/description/

DESCRIPTION

Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*' where:
- '.' Matches any single character.​​​​
- '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

---

#### Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

---

#### Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

---

#### Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".

---

#### Constraints:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This is a string matching problem with state transitions.
    - The '.' character is simple: it acts as a wildcard for one index.
    - The '*' character is complex: it depends on the preceding character and can represent 0, 1, or many instances.
    - If we see a '*' at `p[j+1]`, we have two main branches:
        1. Don't use the '*': Move pattern pointer past the '*' (j + 2).
        2. Use the '*': If s[i] matches p[j], move string pointer (i + 1) and keep pattern pointer.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^(n+m))
    2. Memoization (Top-Down): O(n * m) time and space.
    3. Tabulation (Bottom-Up): O(n * m) time and space.
    """

    def is_match_memo(self, s: str, p: str) -> bool:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        memo = {}

        def dfs(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            if i >= len(s) and j >= len(p):
                return True
            if j >= len(p):
                return False

            # Check if current characters match
            match = i < len(s) and (s[i] == p[j] or p[j] == ".")

            # Case: Next character is '*'
            if (j + 1) < len(p) and p[j + 1] == "*":
                # Branch 1: Skip the '*' (don't use the character)
                # Branch 2: Use the '*' (if current match is True)
                res = dfs(i, j + 2) or (match and dfs(i + 1, j))
                memo[(i, j)] = res
                return res

            # Case: Standard match (no '*')
            if match:
                res = dfs(i + 1, j + 1)
                memo[(i, j)] = res
                return res

            memo[(i, j)] = False
            return False

        return dfs(0, 0)

    def is_match_tabulation(self, s: str, p: str) -> bool:
        """
        Approach: Bottom-Up DP (2D Table)
        - dp[i][j] represents if s[i:] matches p[j:].

        

        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
        dp[len(s)][len(p)] = True

        for i in range(len(s), -1, -1):
            for j in range(len(p) - 1, -1, -1):
                match = i < len(s) and (s[i] == p[j] or p[j] == ".")

                if (j + 1) < len(p) and p[j + 1] == "*":
                    # Skip '*' case
                    dp[i][j] = dp[i][j + 2]
                    # Use '*' case
                    if match:
                        dp[i][j] = dp[i + 1][j] or dp[i][j]
                elif match:
                    dp[i][j] = dp[i + 1][j + 1]
                    
        return dp[0][0]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ("aa", "a"),
        ("aa", "a*"),
        ("ab", ".*"),
        ("aab", "c*a*b")
    ]

    for s_str, p_str in test_cases:
        print(f"String: '{s_str}', Pattern: '{p_str}'")
        print(f"Memoization: {solution.is_match_memo(s_str, p_str)}")
        print(f"Tabulation:  {solution.is_match_tabulation(s_str, p_str)}")
        print("-" * 35)

    print(f"result: {solution.is_match_tabulation(test_cases[1][0], test_cases[1][1])}")
