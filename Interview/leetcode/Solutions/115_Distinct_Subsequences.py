# File: Leetcode/Solutions/115_Distinct_Subsequences.py

"""
Problem Number: 115
Problem Name: Distinct Subsequences
Difficulty: Hard
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Google, Amazon, Microsoft, Adobe
Leetcode Link: https://leetcode.com/problems/distinct-subsequences/description/

DESCRIPTION

Given two strings s and t, return the number of distinct subsequences of s which equals t.

The test cases are generated so that the answer fits in a 32-bit signed integer.

---

#### Example 1:
Input: s = "rabbbit", t = "rabbit"
Output: 3
Explanation:
As shown below, there are 3 ways you can generate "rabbit" from s.
1. **rabb**b**it**
2. **rab**b**bit**
3. **ra**b**bbit**

---

#### Example 2:
Input: s = "babgbag", t = "bag"
Output: 5
Explanation:
As shown below, there are 5 ways you can generate "bag" from s.
1. **ba**b**g**bag
2. **ba**bgba**g**
3. **b**abg**bag**
4. ba**bgbag**
5. babg**bag**

---

#### Constraints:
- 1 <= s.length, t.length <= 1000
- s and t consist of English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - We want to find how many ways we can pick characters from `s` to form `t`.
    - If s[i] == t[j], we have two choices:
        1. Use s[i]: Move to next characters in both (dfs(i+1, j+1)).
        2. Skip s[i]: Try to find t[j] in the rest of s (dfs(i+1, j)).
    - If s[i] != t[j], we MUST skip s[i] (dfs(i+1, j)).
    - Base Cases:
        1. If t is empty (j == len(t)): We found 1 way (return 1).
        2. If s is empty but t isn't (i == len(s)): We found 0 ways (return 0).

    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n)
    2. Memoization (Top-Down): O(n * m) time and space.
    3. Tabulation (Bottom-Up): O(n * m) time and space.
    4. Space Optimized DP: O(m) space.
    """

    def num_distinct_memo(self, s: str, t: str) -> int:
        """
        Approach: Top-Down DP (Memoization)
        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        memo = {}

        def dfs(i, j):
            if j == len(t):
                return 1
            if i == len(s):
                return 0
            if (i, j) in memo:
                return memo[(i, j)]

            # Option 1: Always possible to skip current s[i]
            res = dfs(i + 1, j)
            
            # Option 2: If characters match, we can choose to use s[i]
            if s[i] == t[j]:
                res += dfs(i + 1, j + 1)
            
            memo[(i, j)] = res
            return res

        return dfs(0, 0)

    def num_distinct_tabulation(self, s: str, t: str) -> int:
        """
        Approach: Bottom-Up DP (2D Table)
        - dp[i][j] represents number of ways to form t[j:] using s[i:].

        

        T.C.: O(n * m)
        S.C.: O(n * m)
        """
        m, n = len(s), len(t)
        # dp table of size (m+1) x (n+1)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base case: if t is empty, there is 1 subsequence (the empty one)
        for i in range(m + 1):
            dp[i][n] = 1

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                # We always carry over ways from skipping s[i]
                dp[i][j] = dp[i + 1][j]
                
                # If characters match, add ways from using s[i]
                if s[i] == t[j]:
                    dp[i][j] += dp[i + 1][j + 1]
                    
        return dp[0][0]

    def num_distinct_optimized(self, s: str, t: str) -> int:
        """
        Approach: Space Optimized DP (1D Table)
        - Since we only look at the 'next' row (i+1), we can reduce space.
        T.C.: O(n * m)
        S.C.: O(n)
        """
        m, n = len(s), len(t)
        dp = [0] * (n + 1)
        dp[n] = 1 # Base case: empty t

        for i in range(m - 1, -1, -1):
            # We must use a temp variable or update carefully to avoid 
            # using the updated value of the current row
            prev_diagonal = dp[n] 
            for j in range(n - 1, -1, -1):
                old_dp_j = dp[j]
                if s[i] == t[j]:
                    dp[j] += dp[j + 1]
                # dp[j] now contains the value for current i, j
                # (effectively dp[i][j] = dp[i+1][j] + dp[i+1][j+1] if match)
                
        # Note: A simpler 1D update is often done by iterating j forwards 
        # but requires careful mapping. Backwards is safer for 0/1 logic.
        return dp[0]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ("rabbbit", "rabbit"),
        ("babgbag", "bag"),
    ]

    for s_str, t_str in test_cases:
        print(f"s: '{s_str}', t: '{t_str}'")
        print(f"Memoization: {solution.num_distinct_memo(s_str, t_str)}")
        print(f"Tabulation:  {solution.num_distinct_tabulation(s_str, t_str)}")
        print("-" * 35)

    print(f"result: {solution.num_distinct_tabulation(test_cases[0][0], test_cases[0][1])}")