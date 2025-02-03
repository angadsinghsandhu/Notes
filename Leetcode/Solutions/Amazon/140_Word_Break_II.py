# TODO: revisit [IMP]

# File: Leetcode/Solutions/140_Word_Break_II.py

"""
Problem Number: 140
Problem Name: Word Break II
Difficulty: Hard
Tags: Trie, Memoization, Array, Hash Table, String, Dynamic Programming, Backtracking
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/word-break-ii/description/

DESCRIPTION

Given a string `s` and a dictionary of strings `wordDict`, add spaces in `s` to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

---

#### Example 1:
**Input:**
```plaintext
s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
```

**Output:**
```plaintext
["cats and dog","cat sand dog"]
```

**Explanation:**  
The string "catsanddog" can be segmented into "cats and dog" or "cat sand dog".

#### Example 2:
**Input:**
```plaintext
s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
```

**Output:**
```plaintext
["pine apple pen apple","pineapple pen apple","pine applepen apple"]
```

**Explanation:**  
The string "pineapplepenapple" can be segmented into multiple valid sentences.

#### Constraints:
- `1 <= s.length <= 20`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 10`
- `s` and `wordDict[i]` consist of only lowercase English letters.
- All the strings of `wordDict` are unique.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding all possible ways to segment a string into words from a given dictionary.
    - A brute-force approach involves checking all possible segmentations, but this is inefficient.
    - An optimized approach uses backtracking with memoization to avoid redundant computations.

    Input:
        s: str - The input string to be segmented.
        wordDict: List[str] - A list of words in the dictionary.

    Output:
        List[str] - A list of all possible sentences formed by segmenting `s` into words from `wordDict`.
    """

    def brute_force_solution(self, s: str, wordDict: List[str]) -> List[str]:
        """
        Approach:
        - Recursively check all possible segmentations of `s` using words from `wordDict`.
        - If a segmentation results in the entire string being segmented, add it to the result.

        T.C.: O(2^n) - Exponential time complexity due to recursive branching.
        S.C.: O(n) - Recursive stack space.
        """
        wordSet = set(wordDict)

        def backtrack(s: str) -> List[List[str]]:
            if not s:
                return [[]]
            result = []
            for i in range(1, len(s) + 1):
                prefix = s[:i]
                if prefix in wordSet:
                    for suffix_segment in backtrack(s[i:]):
                        result.append([prefix] + suffix_segment)
            return result

        return [" ".join(words) for words in backtrack(s)]

    def optimized_mem_solution(self, s: str, wordDict: List[str]) -> List[str]:
        """
        Approach:
        - Use backtracking with memoization to avoid redundant computations.
        - Store intermediate results to reuse them when the same substring is encountered again.

        T.C.: O(n^2 * m) - Where n is the length of `s` and m is the number of words in `wordDict`.
        S.C.: O(n^2) - Space for memoization and recursive stack.
        """
        wordSet = set(wordDict)
        memo = {}

        def backtrack(s: str) -> List[List[str]]:
            if s in memo:
                return memo[s]
            if not s:
                return [[]]
            result = []
            for i in range(1, len(s) + 1):
                prefix = s[:i]
                if prefix in wordSet:
                    for suffix_segment in backtrack(s[i:]):
                        result.append([prefix] + suffix_segment)
            memo[s] = result
            return result

        return [" ".join(words) for words in backtrack(s)]
    
    def optimized_tab_solution(self, s: str, wordDict: List[str]) -> List[str]:
        """
        Approach:
        - Use dynamic programming with tabulation.
        - dp[i] will store all possible sentences that can be formed with s[0:i].
        - Start with dp[0] initialized with an empty string to serve as the base case.
        - For each index i, if there are sentences in dp[i], then try to extend these sentences 
          by matching words in wordDict starting from index i.
        - Update dp[i + len(word)] accordingly.
        
        T.C.: O(n^2 * m) in the worst case, where n is the length of s and m is the number of words in wordDict.
        S.C.: O(n * k) where k is the average number of sentences per index.
        """
        wordSet = set(wordDict)
        n = len(s)
        # dp[i] holds a list of sentences that can be formed with s[:i]
        dp = [[] for _ in range(n + 1)]
        dp[0] = [""]  # Base case: an empty string represents the starting point

        for i in range(n):
            # Only proceed if there is at least one valid sentence ending at index i
            if dp[i]:
                for word in wordSet:
                    # Check if the word fits starting at position i
                    if s.startswith(word, i):
                        # Build new sentences for dp[i + len(word)]
                        for sentence in dp[i]:
                            # Append the current word to the sentence (handle the base case to avoid leading spaces)
                            if sentence == "":
                                dp[i + len(word)].append(word)
                            else:
                                dp[i + len(word)].append(sentence + " " + word)

        return dp[n]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    s1 = "catsanddog"
    wordDict1 = ["cat", "cats", "and", "sand", "dog"]
    print(solution.brute_force_solution(s1, wordDict1))  # Output: ["cats and dog", "cat sand dog"]
    print(solution.optimized_mem_solution(s1, wordDict1))    # Output: ["cats and dog", "cat sand dog"]
    print(solution.optimized_tab_solution(s1, wordDict1))    # Output: ["cats and dog", "cat sand dog"]

    # Test case 2
    s2 = "pineapplepenapple"
    wordDict2 = ["apple", "pen", "applepen", "pine", "pineapple"]
    print(solution.brute_force_solution(s2, wordDict2))  # Output: ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]
    print(solution.optimized_mem_solution(s2, wordDict2))    # Output: ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]
    print(solution.optimized_tab_solution(s2, wordDict2))    # Output: ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]

    # Test case 3
    s3 = "catsandog"
    wordDict3 = ["cats", "dog", "sand", "and", "cat"]
    print(solution.brute_force_solution(s3, wordDict3))  # Output: []
    print(solution.optimized_mem_solution(s3, wordDict3))    # Output: []
    print(solution.optimized_tab_solution(s3, wordDict3))    # Output: []
