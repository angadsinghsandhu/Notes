# DECODE WAYS

# Problem number: 91
# Difficulty: Medium
# Tags: Dynamic Programming, String
# Link: https://leetcode.com/problems/decode-ways/

class Solution:
    """
    This problem requires counting the number of ways a given string of digits can be decoded
    based on the mapping '1' -> 'A', '2' -> 'B', ..., '26' -> 'Z'. 
    The solution uses dynamic programming to keep track of the number of ways to decode 
    substrings of different lengths.

    We will implement a dynamic programming approach that ensures efficient computation 
    while checking valid combinations of single and two-digit numbers.
    """

    def numDecodings(self, s: str) -> int:
        """
        DP approach to count the number of ways to decode the string.
        
        T.C. : O(n) where n is the length of the string
        S.C. : O(n) for the DP array
        """
        if not s or s[0] == '0':  # A string starting with '0' cannot be decoded
            return 0

        # Initialize dp array where dp[i] represents the number of ways to decode s[:i]
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1  # Base case: an empty string can be decoded in 1 way
        dp[1] = 1  # A single non-'0' digit can be decoded in 1 way

        for i in range(2, n + 1):
            # Check if the single digit is valid (1-9)
            if s[i - 1] != '0':
                dp[i] += dp[i - 1]

            # Check if the two digits form a valid number (10-26)
            two_digit = int(s[i - 2:i])
            if 10 <= two_digit <= 26:
                dp[i] += dp[i - 2]

        return dp[n]

# Best Method: The dynamic programming approach ensures that we avoid recomputation
# while checking valid single and two-digit numbers in the string.

# Sample Test Cases
solution = Solution()
print(solution.numDecodings("12"))   # Expected output: 2 ("AB", "L")
print(solution.numDecodings("226"))  # Expected output: 3 ("BZ", "VF", "BBF")
print(solution.numDecodings("06"))   # Expected output: 0 (Invalid due to leading zero)
