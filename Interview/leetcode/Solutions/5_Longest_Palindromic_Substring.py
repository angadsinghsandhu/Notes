# File: Leetcode/Solutions/5_Longest_Palindromic_Substring.py

"""
Problem Number: 5
Problem Name: Longest Palindromic Substring
Difficulty: Medium
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Microsoft, Google, Adobe, Facebook
Leetcode Link: https://leetcode.com/problems/longest-palindromic-substring/description/

DESCRIPTION

Given a string `s`, return the longest palindromic substring in `s`.

---

#### Example 1:

Input:
s = "babad"

Output:
"bab"

Explanation:
"aba" is also a valid answer.

---

#### Example 2:

Input:
s = "cbbd"

Output:
"bb"

---

#### Constraints:

- 1 <= s.length <= 1000
- `s` consist of only digits and English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - A palindrome reads the same forwards and backwards.
    - Brute Force: Check every possible substring. There are O(n^2) substrings, and checking each takes O(n), totaling O(n^3).
    - Dynamic Programming: A substring s[i...j] is a palindrome if s[i] == s[j] and s[i+1...j-1] is a palindrome.
    - Expand Around Center: A palindrome can be centered at a single character (odd length) or between two characters (even length). Since there are 2n-1 such centers, and expanding takes O(n), the total time is O(n^2).
    - Manacher's Algorithm: A more advanced approach that solves this in O(n) by reusing work from previous expansions.

    Input:
        s: str - The input string.

    Output:
        str - The longest palindromic substring.
    """

    def longest_palindrome_brute_force(self, s: str) -> str:
        """
        Approach: Brute Force
        - Generate all possible substrings.
        - Check if each is a palindrome.
        - Track the longest one found.

        T.C.: O(n^3)
        S.C.: O(1)
        """
        def is_palindrome(sub):
            return sub == sub[::-1]

        res = ""
        for i in range(len(s)):
            for j in range(i, len(s)):
                substring = s[i:j+1]
                if len(substring) > len(res) and is_palindrome(substring):
                    res = substring
        return res

    def longest_palindrome_dp(self, s: str) -> str:
        """
        Approach: Dynamic Programming (Top-Down Matrix)
        - We use a 2D boolean matrix `dp` where `dp[i][j]` is True if `s[i...j]` is a palindrome.
        - Base cases: `dp[i][i] = True` (single characters) and `dp[i][i+1] = (s[i] == s[i+1])`.
        - Transitions: `dp[i][j] = (s[i] == s[j] and dp[i+1][j-1])`.

        T.C.: O(n^2)
        S.C.: O(n^2)
        """
        n = len(s)
        if n <= 1:
            return s
        
        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1
        
        # All substrings of length 1 are palindromes
        for i in range(n):
            dp[i][i] = True
            
        # Check for substrings of length 2
        for i in range(n - 1):
            if s[i] == s[i+1]:
                dp[i][i+1] = True
                start = i
                max_len = 2
                
        # Check for lengths greater than 2
        # k is the length of the substring
        for k in range(3, n + 1):
            for i in range(n - k + 1):
                j = i + k - 1
                if s[i] == s[j] and dp[i+1][j-1]:
                    dp[i][j] = True
                    if k > max_len:
                        start = i
                        max_len = k
                        
        return s[start : start + max_len]

    def longest_palindrome_expand_center(self, s: str) -> str:
        """
        Approach: Expand Around Center (Optimal Space)
        - Treat each character (and the gap between characters) as a potential center.
        - Expand outwards as long as the characters match.
        
        

        T.C.: O(n^2)
        S.C.: O(1)
        """
        if not s:
            return ""
        
        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Return the substring that was valid before the while loop failed
            return s[left + 1 : right]

        res = ""
        for i in range(len(s)):
            # Odd length palindromes (center is s[i])
            p1 = expand(i, i)
            if len(p1) > len(res):
                res = p1
                
            # Even length palindromes (center is between s[i] and s[i+1])
            p2 = expand(i, i + 1)
            if len(p2) > len(res):
                res = p2
                
        return res

    def longest_palindrome_manacher(self, s: str) -> str:
        """
        Approach: Manacher's Algorithm
        - This is a complex algorithm to find the longest palindrome in linear time.
        - It uses previously computed palindrome lengths to skip redundant comparisons.
        
        

        T.C.: O(n)
        S.C.: O(n)
        """
        # Transform string to handle even/odd lengths: "aba" -> "#a#b#a#"
        T = "#" + "#".join(s) + "#"
        n = len(T)
        P = [0] * n # Array to store radii of palindromes at each center
        center = right = 0
        
        for i in range(n):
            mirror = 2 * center - i
            
            if i < right:
                P[i] = min(right - i, P[mirror])
                
            # Attempt to expand around i
            try:
                while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
                    P[i] += 1
            except IndexError:
                pass
                
            # Update center and right boundary if expanded past current right
            if i + P[i] > right:
                center = i
                right = i + P[i]
                
        max_len, center_index = max((n, i) for i, n in enumerate(P))
        start = (center_index - max_len) // 2
        return s[start : start + max_len]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    s1 = "babad"
    print(f"Input: {s1}")
    print(f"DP Result:     {solution.longest_palindrome_dp(s1)}")
    print(f"Expand Result: {solution.longest_palindrome_expand_center(s1)}")
    print(f"Manacher:      {solution.longest_palindrome_manacher(s1)}")
    print("-" * 30)

    # Test Case 2
    s2 = "cbbd"
    print(f"Input: {s2}")
    print(f"Expand Result: {solution.longest_palindrome_expand_center(s2)}") # Expected "bb"
    print("-" * 30)

    # Test Case 3: Edge Case
    s3 = "a"
    print(f"Input: {s3}")
    print(f"Result: {solution.longest_palindrome_expand_center(s3)}")
