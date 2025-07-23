# EDIT DISTANCE

# Problem number: 72
# Difficulty: Medium
# Tags: Dynamic Programming
# link: https://leetcode.com/problems/edit-distance/

class Solution:
    """
    This problem involves finding the minimum number of operations needed to convert one string into another.
    The allowed operations are insertion, deletion, or replacement of a character. We can solve this problem 
    using dynamic programming by defining a 2D DP array where dp[i][j] represents the minimum number of operations 
    needed to convert the first i characters of word1 to the first j characters of word2.

    T.C. : O(n * m)
    S.C. : O(n * m)

    Input:
        - word1 : str : the first word
        - word2 : str : the second word

    Output:
        - int : minimum number of operations required to convert word1 to word2
    """
    def minDistance(self, word1: str, word2: str) -> int:
        # get the length of the words and create a DP array
        n, m = len(word1), len(word2)
        dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        
        # initialize the base cases
        for i in range(1, n + 1):
            dp[i][0] = i
        for j in range(1, m + 1):
            dp[0][j] = j
        
        # fill the DP array
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if word1[i - 1] == word2[j - 1]:
                    # if characters are the same, no new operation is needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # if characters are different, consider the three possible operations
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
        
        # return the last element of the DP array, which contains the answer
        return dp[-1][-1]

# Sample Inputs
word1 = "horse"
word2 = "ros"

# Expected Output : 3
print(Solution().minDistance(word1, word2))