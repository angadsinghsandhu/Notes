# File: Leetcode/Solutions/72_Edit_Distance.py

"""
Problem Number: 72
Problem Name: Edit Distance
Difficulty: Medium
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, Adobe
Leetcode Link: https://leetcode.com/problems/edit-distance/description/

DESCRIPTION

Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.

You have the following three operations permitted on a word:
1. Insert a character
2. Delete a character
3. Replace a character

---

#### Example 1:
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation: 
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')

---

#### Example 2:
Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation: 
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')

---

#### Constraints:
- 0 <= word1.length, word2.length <= 500
- `word1` and `word2` consist of lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - We want to transform word1 into word2 using minimum operations.
    - If word1[i] == word2[j], no operation is needed for this pair; move to the next.
    - If they don't match, we have three choices:
        1. Insert: Move pointer in word2, keep pointer in word1 (dfs(i, j + 1))
        2. Delete: Move pointer in word1, keep pointer in word2 (dfs(i + 1, j))
        3. Replace: Move both pointers (dfs(i + 1, j + 1))
    - Base Case: If one string is empty, we must delete/insert all characters of the other string.

    Approach Hierarchy:
    1. Brute Force (Recursion): O(3^(n+m))
    2. Memoization (Top-Down): O(n * m) time and space.
    3. Tabulation (Bottom-Up): O(n * m) time and space.
    4. Space Optimized DP: O(m) space.
    """

    def min_distance_memo(self, word1: str, word2: str) -> int:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        memo = {}

        def dfs(i, j):
            # Base cases: if one string is exhausted, return remaining length of the other
            if i == len(word1): return len(word2) - j
            if j == len(word2): return len(word1) - i
            
            if (i, j) in memo:
                return memo[(i, j)]

            if word1[i] == word2[j]:
                res = dfs(i + 1, j + 1)
            else:
                # Calculate costs for all three operations and take the minimum
                insert = 1 + dfs(i, j + 1)
                delete = 1 + dfs(i + 1, j)
                replace = 1 + dfs(i + 1, j + 1)
                res = min(insert, delete, replace)
            
            memo[(i, j)] = res
            return res

        return dfs(0, 0)

    def min_distance_tabulation(self, word1: str, word2: str) -> int:
        """
        Approach: Bottom-Up DP (2D Grid)
        - dp[i][j] represents the min distance between word1[i:] and word2[j:].
        
        

        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base cases: filling boundaries
        for i in range(m + 1):
            dp[i][n] = m - i
        for j in range(n + 1):
            dp[m][j] = n - j

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    # min(Insert, Delete, Replace)
                    dp[i][j] = 1 + min(dp[i][j + 1], dp[i + 1][j], dp[i + 1][j + 1])
        
        return dp[0][0]

    def min_distance_optimized(self, word1: str, word2: str) -> int:
        """
        Approach: Space Optimized DP
        - Reduces space from O(n*m) to O(n) by using only two rows.
        
        T.C.: O(n * m)
        S.C.: O(min(n, m))
        """
        if len(word1) < len(word2):
            word1, word2 = word2, word1
        
        m, n = len(word1), len(word2)
        prev = list(range(n, -1, -1))

        for i in range(m - 1, -1, -1):
            curr = [0] * (n + 1)
            curr[n] = m - i
            for j in range(n - 1, -1, -1):
                if word1[i] == word2[j]:
                    curr[j] = prev[j + 1]
                else:
                    curr[j] = 1 + min(curr[j + 1], prev[j], prev[j + 1])
            prev = curr
            
        return prev[0]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ("horse", "ros"),
        ("intention", "execution"),
        ("", "abc")
    ]

    for w1, w2 in test_cases:
        print(f"Word1: '{w1}', Word2: '{w2}'")
        print(f"Memoization: {solution.min_distance_memo(w1, w2)}")
        print(f"Tabulation:  {solution.min_distance_tabulation(w1, w2)}")
        print(f"Optimized:   {solution.min_distance_optimized(w1, w2)}")
        print("-" * 35)

    print(f"result: {solution.min_distance_tabulation(test_cases[0][0], test_cases[0][1])}")
