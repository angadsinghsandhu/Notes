# File: Leetcode/Solutions/647_Palindromic_Substrings.py

"""
Problem Number: 647
Problem Name: Palindromic Substrings
Difficulty: Medium
Tags: String, Dynamic Programming, NeetCode 150
Company (Frequency): Amazon, Google, Microsoft, Facebook
Leetcode Link: https://leetcode.com/problems/palindromic-substrings/description/

DESCRIPTION

Given a string `s`, return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.
A substring is a contiguous sequence of characters within the string.

---

#### Example 1:

Input:
s = "abc"

Output:
3

Explanation:
Three palindromic substrings: "a", "b", "c".

---

#### Example 2:

Input:
s = "aaa"

Output:
6

Explanation:
Six palindromic substrings: "a", "a", "a", "aa", "aa", "aaa".

---

#### Constraints:

- 1 <= s.length <= 1000
- `s` consists of lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - This problem is very similar to "Longest Palindromic Substring", but instead of finding the length/string, we need to count all occurrences.
    - A substring is a palindrome if it reads the same from both ends.
    - Brute Force: Iterate through all possible O(n^2) substrings and check each for palindrome property O(n). Total O(n^3).
    - Dynamic Programming: Use a 2D table where dp[i][j] is true if s[i...j] is a palindrome. This is built upon the fact that s[i...j] is a palindrome if s[i] == s[j] AND the inner part s[i+1...j-1] is also a palindrome.
    - Expand Around Center: Each character and each gap between characters can be a center. Expanding outwards from 2n-1 centers allows us to count all palindromes in O(n^2) time with O(1) space.

    Input:
        s: str - The input string.

    Output:
        int - Total count of palindromic substrings.
    """

    def count_substrings_brute_force(self, s: str) -> int:
        """
        Approach: Brute Force
        - Generate every possible substring (i, j).
        - Check if the substring is equal to its reverse.
        
        T.C.: O(n^3)
        S.C.: O(1) (or O(n) depending on string slicing implementation)
        """
        count = 0
        n = len(s)
        for i in range(n):
            for j in range(i, n):
                sub = s[i:j+1]
                if sub == sub[::-1]:
                    count += 1
        return count

    def count_substrings_dp(self, s: str) -> int:
        """
        Approach: Dynamic Programming (Top-down Matrix)
        - We use a 2D DP matrix where dp[i][j] represents if s[i...j] is a palindrome.
        - The matrix is filled based on length of substrings.
        - Single characters (len 1) are always palindromes.
        - Pairs (len 2) are palindromes if characters match.
        - Substrings (len > 2) are palindromes if s[i]==s[j] and dp[i+1][j-1] is True.

        

        T.C.: O(n^2)
        S.C.: O(n^2)
        """
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0
        
        # Base case: single letters
        for i in range(n):
            dp[i][i] = True
            count += 1
            
        # Base case: double letters
        for i in range(n - 1):
            if s[i] == s[i+1]:
                dp[i][i+1] = True
                count += 1
                
        # Substrings of length 3 or more
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i+1][j-1]:
                    dp[i][j] = True
                    count += 1
                    
        return count

    def count_substrings_expand_center(self, s: str) -> int:
        """
        Approach: Expand Around Center (Optimal Space)
        - There are 2n-1 potential centers (n characters and n-1 gaps).
        - For each center, expand outwards as long as it's a palindrome.
        - Each successful expansion represents one unique palindromic substring.

        

        T.C.: O(n^2)
        S.C.: O(1)
        """
        self.count = 0
        
        def extract_palindrome(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                self.count += 1
                left -= 1
                right += 1
                
        for i in range(len(s)):
            # Odd length: center is the character itself
            extract_palindrome(i, i)
            # Even length: center is the gap between characters
            extract_palindrome(i, i + 1)
            
        return self.count

    def count_substrings_manacher(self, s: str) -> int:
        """
        Approach: Manacher's Algorithm (Optimal)
        - We transform s into T (e.g., "aba" -> "#a#b#a#") to handle even/odd symmetry uniformly.
        - We maintain an array P where P[i] is the radius of the palindrome at T[i].
        - The number of palindromic substrings in the original string centered at i is:
          ceil(radius / 2). In our transformed radius array, it's (P[i] + 1) // 2.
        
        T.C.: O(n)
        S.C.: O(n)
        """
        if not s:
            return 0
        
        # Transform string: "aba" -> "^#a#b#a#$" 
        # (Special sentinels ^ and $ avoid boundary checks)
        T = "^#" + "#".join(s) + "#$"
        n = len(T)
        P = [0] * n
        center = right = 0
        
        for i in range(1, n - 1):
            # Use symmetry to initialize P[i]
            if i < right:
                P[i] = min(right - i, P[2 * center - i])
            
            # Attempt to expand around i
            while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
                P[i] += 1
            
            # Update center and right boundary
            if i + P[i] > right:
                center = i
                right = i + P[i]
        
        # In the transformed string, the radius P[i] directly tells us 
        # how many palindromes are centered at i in the original string.
        # Example: "#a#b#a#" center 'b' has P[i]=3, which corresponds to 
        # "b" and "aba" in the original. (3+1)//2 = 2.
        # Summing (P[i] + 1) // 2 for all i gives the total count.
        
        return sum((radius + 1) // 2 for radius in P)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    s1 = "abc"
    print(f"Test Case 1: s = '{s1}'")
    print(f"Brute Force:      {solution.count_substrings_brute_force(s1)}")
    print(f"DP Result:        {solution.count_substrings_dp(s1)}")
    print(f"Expand Center:    {solution.count_substrings_expand_center(s1)}")
    print(f"Manacher:         {solution.count_substrings_manacher(s1)}")
    print("-" * 35)

    # Test Case 2
    s2 = "aaa"
    print(f"Test Case 2: s = '{s2}'")
    print(f"DP Result:        {solution.count_substrings_dp(s2)}")
    print(f"Expand Center:    {solution.count_substrings_expand_center(s2)}")
    print(f"Manacher:         {solution.count_substrings_manacher(s2)}")
    print("-" * 35)

    # Test Case 3: Empty string (though constraints say length >= 1)
    s3 = "aba"
    print(f"Test Case 3: s = '{s3}'")
    print(f"Result: {solution.count_substrings_expand_center(s3)}") # Expected: 4 (a, b, a, aba)
    print(f"Manacher: {solution.count_substrings_manacher(s3)}")      # Expected: 4 (a, b, a, aba)
