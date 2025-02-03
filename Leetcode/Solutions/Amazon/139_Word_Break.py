# TODO: revisit

# File: Leetcode/Solutions/139_Word_Break.py

"""
Problem Number: 139
Problem Name: Word Break
Difficulty: Medium
Tags: Dynamic Programming, Trie, Memoization, Hash Table, String
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/word-break/description/

DESCRIPTION

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

---

#### Example 1:
**Input:**
```plaintext
s = "leetcode", wordDict = ["leet","code"]
```

**Output:**
```plaintext
true
```

**Explanation:**  
Return true because "leetcode" can be segmented as "leet code".

#### Example 2:
**Input:**
```plaintext
s = "applepenapple", wordDict = ["apple","pen"]
```

**Output:**
```plaintext
true
```

**Explanation:**  
Return true because "applepenapple" can be segmented as "apple pen apple".

#### Example 3:
**Input:**
```plaintext
s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
```

**Output:**
```plaintext
false
```

**Explanation:**  
No valid segmentation exists.

#### Constraints:
- `1 <= s.length <= 300`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 20`
- `s` and `wordDict[i]` consist of only lowercase English letters.
- All the strings of `wordDict` are unique.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves determining if a string can be segmented into words from a given dictionary.
    - A brute-force approach involves checking all possible segmentations, but this is inefficient.
    - An optimized approach uses dynamic programming to track whether substrings of `s` can be segmented.

    Input:
        s: str - The input string to be segmented.
        wordDict: List[str] - A list of words in the dictionary.

    Output:
        bool - True if `s` can be segmented into words from `wordDict`, otherwise False.
    """

    def brute_force_solution(self, s: str, wordDict: List[str]) -> bool:
        """
        Approach:
        - Recursively check all possible segmentations of `s` using words from `wordDict`.
        - If any segmentation results in the entire string being covered, return True.

        T.C.: O(2^n) - Exponential time due to recursive branching.
        S.C.: O(n) - Recursion stack space.
        """
        def dfs(start):
            if start == len(s):
                return True
            for word in wordDict:
                if s.startswith(word, start):
                    if dfs(start + len(word)):
                        return True
            return False

        return dfs(0)

    def optimized_solution(self, s: str, wordDict: List[str]) -> bool:
        """
        Approach:
        - Use dynamic programming to track whether substrings of `s` can be segmented.
        - Initialize a `dp` array where `dp[i]` is True if `s[0:i]` can be segmented.
        - Iterate through the string and update the `dp` array based on valid word matches.

        T.C.: O(n * m * k) - Where `n` is the length of `s`, `m` is the number of words in `wordDict`, and `k` is the maximum word length.
        S.C.: O(n) - Space for the `dp` array.
        """
        wordSet = set(wordDict)  # Convert wordDict to a set for O(1) lookups
        dp = [False] * (len(s) + 1)
        dp[0] = True  # Empty string can always be segmented

        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in wordSet:
                    dp[i] = True
                    break

        return dp[len(s)]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    s1 = "leetcode"
    wordDict1 = ["leet", "code"]
    print(solution.brute_force_solution(s1, wordDict1))  # Output: True
    print(solution.optimized_solution(s1, wordDict1))    # Output: True

    # Test case 2
    s2 = "applepenapple"
    wordDict2 = ["apple", "pen"]
    print(solution.brute_force_solution(s2, wordDict2))  # Output: True
    print(solution.optimized_solution(s2, wordDict2))    # Output: True

    # Test case 3
    s3 = "catsandog"
    wordDict3 = ["cats", "dog", "sand", "and", "cat"]
    print(solution.brute_force_solution(s3, wordDict3))  # Output: False
    print(solution.optimized_solution(s3, wordDict3))    # Output: False
