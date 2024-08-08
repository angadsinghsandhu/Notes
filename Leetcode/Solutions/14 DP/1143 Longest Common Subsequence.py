# LONGEST COMMON SUBSEQUENCE

# Problem number: 1143
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/longest-common-subsequence/

class Solution:
    """
    This is a classic DP problem, where we have to find the longest common subsequence
    between two strings. We can solve this problem using a 2D DP array. We will iterate
    over the two strings and fill the DP array. If the characters at the current index
    are equal, we will add 1 to the value of the DP array at the previous index. If the
    characters are not equal, we will take the maximum of the values of the DP array at
    the previous index of the current string and the current index of the other string.

    T.C. : O(n*m)
    S.C. : O(n*m)

    Input:
        - text1 : str : first string
        - text2 : str : second string

    Output:
        - int : length of the longest common subsequence
    """
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # get the length of the strings and create a DP array
        n, m = len(text1), len(text2)
        dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
        
        # fill the DP array
        for i in range(1, n+1):
            for j in range(1, m+1):
                if text1[i-1] == text2[j-1]:
                    # if the characters are equal, add 1 to the previous index
                    dp[i][j] = 1 + dp[i-1][j-1]
                else:
                    # if the characters are not equal, take the maximum of the previous indices
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # return the last element of the DP array
        return dp[-1][-1]
    
# Sample Inputs
text1 = "abcde"
text2 = "ace"

# Expected Output : 3
print(Solution().longestCommonSubsequence(text1, text2))




