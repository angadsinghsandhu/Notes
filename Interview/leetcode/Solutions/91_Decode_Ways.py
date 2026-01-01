# File: Leetcode/Solutions/91_Decode_Ways.py

"""
Problem Number: 91
Problem Name: Decode Ways
Difficulty: Medium
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Google, Amazon, Facebook, Microsoft
Leetcode Link: https://leetcode.com/problems/decode-ways/description/

DESCRIPTION

A message containing letters from A-Z can be encoded into numbers using the following mapping:
'A' -> "1", 'B' -> "2", ..., 'Z' -> "26"

To decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, "11106" can be mapped into:
- "AAJF" with the grouping (1 1 10 6)
- "KJF" with the grouping (11 10 6)

Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06".

Given a string s containing only digits, return the number of ways to decode it.

---

#### Example 1:
Input: s = "12"
Output: 2
Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

---

#### Example 2:
Input: s = "226"
Output: 3
Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

---

#### Example 3:
Input: s = "06"
Output: 0
Explanation: "06" cannot be mapped to "F" because of the leading zero.

---

#### Constraints:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s).
"""

from typing import Dict

class Solution:
    """
    Thought Process:
    - This is a variation of the "Climbing Stairs" problem. 
    - At any position `i`, we can take 1 digit (if it's not '0') or 2 digits (if they form a number between 10 and 26).
    - If `s[i]` is '0', it cannot be decoded as a single digit.
    - If `s[i-1...i]` is between "10" and "26", it's a valid 2-digit jump.
    
    Approach Hierarchy:
    1. Brute Force (Recursion): O(2^n)
    2. Memoization (Top-Down): O(n) time, O(n) space
    3. Tabulation (Bottom-Up): O(n) time, O(n) space
    4. Space Optimized: O(n) time, O(1) space
    """

    def num_decodings_recursive(self, s: str) -> int:
        """
        Approach: Pure Recursion
        T.C.: O(2^n)
        S.C.: O(n)
        """
        def solve(index):
            if index == len(s):
                return 1
            if s[index] == '0':
                return 0
            
            # Ways by taking 1 digit
            ways = solve(index + 1)
            
            # Ways by taking 2 digits
            if index + 1 < len(s) and (s[index] == '1' or (s[index] == '2' and s[index+1] in "0123456")):
                ways += solve(index + 2)
            
            return ways

        return solve(0)

    def num_decodings_memoization(self, s: str) -> int:
        """
        Approach: Top-Down DP with Memoization
        T.C.: O(n)
        S.C.: O(n)
        """
        memo = {}

        def solve(index):
            if index == len(s):
                return 1
            if s[index] == '0':
                return 0
            if index in memo:
                return memo[index]
            
            res = solve(index + 1)
            if index + 1 < len(s) and (s[index] == '1' or (s[index] == '2' and s[index+1] in "0123456")):
                res += solve(index + 2)
            
            memo[index] = res
            return res

        return solve(0)

    def num_decodings_tabulation(self, s: str) -> int:
        """
        Approach: Bottom-Up DP
        T.C.: O(n)
        S.C.: O(n)
        """
        if not s or s[0] == '0':
            return 0
            
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1 # Base case: empty string
        dp[1] = 1 # We already checked s[0] != '0'
        
        for i in range(2, n + 1):
            # Check 1-digit jump
            if s[i-1] != '0':
                dp[i] += dp[i-1]
            
            # Check 2-digit jump
            two_digit = int(s[i-2:i])
            if 10 <= two_digit <= 26:
                dp[i] += dp[i-2]
                
        return dp[n]

    def num_decodings_optimized(self, s: str) -> int:
        """
        Approach: Space Optimized DP
        T.C.: O(n)
        S.C.: O(1)
        """
        if not s or s[0] == '0':
            return 0
            
        n = len(s)
        prev2 = 1 # dp[i-2]
        prev1 = 1 # dp[i-1]
        
        

        for i in range(2, n + 1):
            current = 0
            # Single digit
            if s[i-1] != '0':
                current += prev1
            
            # Double digit
            two_digit = int(s[i-2:i])
            if 10 <= two_digit <= 26:
                current += prev2
            
            prev2 = prev1
            prev1 = current
            
        return prev1

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = ["12", "226", "06", "10", "2101"]

    for t in test_cases:
        print(f"Input string: '{t}'")
        # Recursion is slow for large strings, but fine for these
        print(f"Recursive: {solution.num_decodings_recursive(t)}")
        print(f"Memoization: {solution.num_decodings_memoization(t)}")
        print(f"Tabulation: {solution.num_decodings_tabulation(t)}")
        print(f"Optimized: {solution.num_decodings_optimized(t)}")
        print("-" * 30)

    # Large case to show efficiency
    large_s = "111111111111"
    print(f"Large Input: {large_s}")
    print(f"result: {solution.num_decodings_optimized(large_s)}")
