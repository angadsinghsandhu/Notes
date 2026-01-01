# File: Leetcode/Solutions/139_Word_Break.py

"""
Problem Number: 139
Problem Name: Word Break
Difficulty: Medium
Tags: Hash Table, String, Dynamic Programming, Trie, Memoization, NeetCode 150
Company (Frequency): Amazon, Facebook, Google, Bloomberg, Microsoft
Leetcode Link: https://leetcode.com/problems/word-break/description/

DESCRIPTION

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

---

#### Example 1:
Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".

---

#### Example 2:
Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
Note that you are allowed to reuse a dictionary word.

---

#### Example 3:
Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false

---

#### Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters.
- All the strings of wordDict are unique.
"""

from typing import List, Set

class Solution:
    """
    Thought Process:
    - We need to determine if a string can be partitioned based on a dictionary.
    - At any point in the string `i`, we check if any word in the dictionary matches the prefix starting at `i`.
    - If it matches, we recursively check the remainder of the string.
    - This problem has overlapping subproblems (e.g., "aaaaa" with dict ["a", "aa"]), making DP/Memoization ideal.

    Approach Hierarchy:
    1. Brute Force Recursion: O(2^n)
    2. Top-Down Memoization: O(n * m * k) where n=len(s), m=len(wordDict), k=avg word length.
    3. Bottom-Up Tabulation: O(n * m * k)
    4. BFS: O(n^2) - Treat indices as nodes in a graph.
    """

    def word_break_recursive(self, s: str, wordDict: List[str]) -> bool:
        """
        Approach: Pure Recursion
        T.C.: O(2^n)
        S.C.: O(n)
        """
        def solve(start):
            if start == len(s):
                return True
            
            for word in wordDict:
                if s.startswith(word, start):
                    if solve(start + len(word)):
                        return True
            return False

        return solve(0)

    def word_break_memoization(self, s: str, wordDict: List[str]) -> bool:
        """
        Approach: Top-Down DP with Memoization
        T.C.: O(n * m * k)
        S.C.: O(n)
        """
        memo = {}
        words = set(wordDict) # O(1) lookups

        def solve(start):
            if start == len(s):
                return True
            if start in memo:
                return memo[start]
            
            for end in range(start + 1, len(s) + 1):
                if s[start:end] in words and solve(end):
                    memo[start] = True
                    return True
            
            memo[start] = False
            return False

        return solve(0)

    def word_break_tabulation(self, s: str, wordDict: List[str]) -> bool:
        """
        Approach: Bottom-Up DP
        - dp[i] means s[i:] can be segmented.
        - We work backwards from the end of the string.
        
        

        T.C.: O(n * m) - where n is string length and m is dictionary size.
        S.C.: O(n)
        """
        dp = [False] * (len(s) + 1)
        dp[len(s)] = True # Base case: empty string can be "segmented"

        for i in range(len(s) - 1, -1, -1):
            for w in wordDict:
                # If there's enough room and the word matches
                if (i + len(w)) <= len(s) and s[i : i + len(w)] == w:
                    dp[i] = dp[i + len(w)]
                if dp[i]: # Optimization: break if we found a valid way for this index
                    break
                    
        return dp[0]

    def word_break_bfs(self, s: str, wordDict: List[str]) -> bool:
        """
        Approach: Breadth-First Search (BFS)
        - Nodes are indices in the string.
        - Edge exists from i to j if s[i:j] is a valid word.
        
        T.C.: O(n^2)
        S.C.: O(n)
        """
        word_set = set(wordDict)
        queue = [0]
        visited = set()

        while queue:
            start = queue.pop(0)
            if start == len(s):
                return True
            
            for end in range(start + 1, len(s) + 1):
                if end not in visited and s[start:end] in word_set:
                    queue.append(end)
                    visited.add(end)
        return False

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ("leetcode", ["leet", "code"]),
        ("applepenapple", ["apple", "pen"]),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"]),
        ("aaaaaaa", ["aaaa", "aaa"])
    ]

    for s_str, d in test_cases:
        print(f"String: '{s_str}', Dict: {d}")
        print(f"Memoization: {solution.word_break_memoization(s_str, d)}")
        print(f"Tabulation:  {solution.word_break_tabulation(s_str, d)}")
        print(f"BFS:         {solution.word_break_bfs(s_str, d)}")
        print("-" * 35)

    print(f"result: {solution.word_break_tabulation(test_cases[0][0], test_cases[0][1])}")