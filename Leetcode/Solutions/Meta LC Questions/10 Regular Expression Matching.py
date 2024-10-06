# REGULAR EXPRESSION MATCHING

# Problem number: 10
# Difficulty: Hard
# Tags: Dynamic Programming, String, Backtracking
# Link: https://leetcode.com/problems/regular-expression-matching/
# Similar Problems: 44 (Wildcard Matching), 65 (Valid Number)

class Solution:
    """
    This problem requires implementing a regular expression matcher that supports
    two special characters:
    1. '.' which matches any single character.
    2. '*' which matches zero or more of the preceding element.

    The solution uses Dynamic Programming (DP) to break the problem into subproblems.
    We will fill a 2D DP table where dp[i][j] indicates if the first i characters of s
    match the first j characters of p.

    We will implement two approaches:
    1. Dynamic Programming (Bottom-up)
    2. Recursion with Memoization (Top-down)
    """

    def isMatch_DP(self, s: str, p: str) -> bool:
        """
        DP approach to solve regular expression matching.
        
        T.C. : O(m * n) where m is the length of string s and n is the length of pattern p
        S.C. : O(m * n) for the DP table
        """
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]

        # Empty string matches empty pattern
        dp[0][0] = True

        # Handle patterns with '*' at the beginning (e.g., a*, a*b* matches empty string)
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        # Fill the DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                elif p[j - 1] == '*':
                    dp[i][j] = dp[i][j - 2]  # '*' acts as zero occurrences
                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                        dp[i][j] = dp[i][j] or dp[i - 1][j]

        return dp[m][n]

    def isMatch_Memoization(self, s: str, p: str) -> bool:
        """
        Recursive approach with memoization to solve regular expression matching.
        
        T.C. : O(m * n) where m is the length of string s and n is the length of pattern p
        S.C. : O(m * n) for memoization
        """
        memo = {}

        def dfs(i: int, j: int) -> bool:
            if (i, j) in memo:
                return memo[(i, j)]

            if j == len(p):
                return i == len(s)

            match = i < len(s) and (p[j] == s[i] or p[j] == '.')

            if j + 1 < len(p) and p[j + 1] == '*':
                memo[(i, j)] = dfs(i, j + 2) or (match and dfs(i + 1, j))
            else:
                memo[(i, j)] = match and dfs(i + 1, j + 1)

            return memo[(i, j)]

        return dfs(0, 0)

# Best Method: The DP approach is generally preferred for its clarity and bottom-up structure,
# but the memoization approach can be more intuitive to implement.

# Sample Inputs for Testing
solution = Solution()

# Testing DP Method
print(solution.isMatch_DP("aa", "a"))    # Output: False
print(solution.isMatch_DP("aa", "a*"))   # Output: True
print(solution.isMatch_DP("ab", ".*"))   # Output: True

# Testing Memoization Method
print(solution.isMatch_Memoization("aa", "a"))    # Output: False
print(solution.isMatch_Memoization("aa", "a*"))   # Output: True
print(solution.isMatch_Memoization("ab", ".*"))   # Output: True
