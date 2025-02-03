# TODO: new

# File: Leetcode/Solutions/1392_Longest_Happy_Prefix.py

"""
Problem Number: 1392
Problem Name: Longest Happy Prefix
Difficulty: Hard
Tags: String, String Matching, Hash Function, Rolling Hash
Company (Frequency): Google (10), Facebook (8), Microsoft (7)
Leetcode Link: https://leetcode.com/problems/longest-happy-prefix/description/

DESCRIPTION

A string is called a "happy prefix" if it is a **non-empty prefix** that is also a suffix (excluding itself).

Given a string `s`, return the **longest happy prefix** of `s`. If no such prefix exists, return an empty string `""`.

---

#### Example 1:
**Input:**
```plaintext
s = "level"
```
**Output:**
```plaintext
"l"
```
**Explanation:**  
The prefixes of "level" excluding itself are: "l", "le", "lev", "leve".  
The suffixes are: "l", "el", "vel", "evel".  
The largest prefix that is also a suffix is "l".

#### Example 2:
**Input:**
```plaintext
s = "ababab"
```
**Output:**
```plaintext
"abab"
```
**Explanation:**  
"abab" is the longest prefix that is also a suffix. It can overlap in the original string.

#### Constraints:
- `1 <= s.length <= 10^5`
- `s` contains only lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires finding the longest prefix that is also a suffix (excluding the entire string itself).
    - A brute-force approach would involve checking all substrings, but this is inefficient.
    - An optimized approach uses **KMP (Knuth-Morris-Pratt) prefix function** to efficiently compute the longest border of `s`.

    Input:
        s: str - A string containing lowercase English letters.

    Output:
        str - The longest prefix that is also a suffix.
    """

    def brute_force_solution(self, s: str) -> str:
        """
        Approach:
        - Try all prefixes and check if they match a corresponding suffix.
        - This approach slices the string and compares substrings at each step.

        T.C.: O(n^2) - Substring comparison in a loop.
        S.C.: O(1) - No additional space used.
        """
        for i in range(len(s) - 1, 0, -1):
            if s[:i] == s[-i:]:
                return s[:i]
        return ""

    def optimized_solution(self, s: str) -> str:
        """
        Approach:
        - Use **KMP (Knuth-Morris-Pratt) prefix function** to find the longest border.
        - The prefix function calculates the longest proper prefix which is also a suffix for each position.

        T.C.: O(n) - Linear time complexity using KMP algorithm.
        S.C.: O(n) - Storing prefix function values.
        """
        n = len(s)
        lps = [0] * n  # Longest Prefix Suffix (LPS) array
        j = 0  # Length of the longest border

        for i in range(1, n):
            while j > 0 and s[i] != s[j]:
                j = lps[j - 1]
            if s[i] == s[j]:
                j += 1
                lps[i] = j
        
        return s[:lps[-1]]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    s1 = "level"
    print(solution.brute_force_solution(s1))  # Output: "l"
    print(solution.optimized_solution(s1))    # Output: "l"

    # Test case 2
    s2 = "ababab"
    print(solution.brute_force_solution(s2))  # Output: "abab"
    print(solution.optimized_solution(s2))    # Output: "abab"

    # Test case 3
    s3 = "aabaacaabaa"
    print(solution.brute_force_solution(s3))  # Output: "aabaa"
    print(solution.optimized_solution(s3))    # Output: "aabaa"
