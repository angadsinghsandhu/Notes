"""
Problem Number: 127
Problem Name: Word Ladder
Difficulty: Hard
Tags: Breadth-First Search (BFS), Hash Table, String, Neetcode 150
Company (Frequency): Amazon, Microsoft, Apple, Google, Adobe (High)
Leetcode Link: https://leetcode.com/problems/word-ladder/

DESCRIPTION

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

- Every adjacent pair of words differs by a single letter.
- Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
- sk == endWord.

Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Example 1:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> "cog", which is 5 words long.

Example 2:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: The endWord "cog" is not in wordList, so no transformation exists.

Constraints:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.
"""

from typing import List
from collections import deque, defaultdict

class Solution:
    """
    Thought Process:
    - The problem is modeled as finding the shortest path in an unweighted graph where nodes are words and edges connect words differing by one character.
    - BFS is optimal for shortest path problems. To efficiently find neighboring words (those differing by one character), we preprocess words into patterns.
    - Each word's pattern is created by replacing each character position with a wildcard (e.g., "hot" becomes "*ot", "h*t", "ho*").
    - A dictionary maps these patterns to all valid words matching them, allowing O(1) neighbor lookups during BFS traversal.

    Approach:
    1. Pre-check if endWord exists in wordList. If not, return 0 immediately.
    2. Preprocess all words (including beginWord) into a pattern dictionary for efficient neighbor lookups.
    3. Use BFS starting from beginWord, tracking visited words to avoid cycles.
    4. For each level of BFS (representing a transformation step), explore all valid neighbors via pattern matching.
    5. Return the transformation depth (level count) when endWord is found. If BFS completes without finding it, return 0.

    Time Complexity: O(M^2 * N), where M = word length and N = number of words. 
      - Pattern creation: O(M*N) words * O(M) time per pattern
      - BFS traversal: Each edge (word connection) is visited once
    Space Complexity: O(M^2 * N) for storing patterns and their mappings.
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        # Preprocess words into pattern mappings
        pattern_map = defaultdict(list)
        wordList.append(beginWord)  # Include beginWord in pattern generation
        
        for word in wordList:
            for i in range(len(word)):
                pattern = word[:i] + "#" + word[i+1:]
                pattern_map[pattern].append(word)
        
        visited = set([beginWord])
        queue = deque([beginWord])
        level = 1  # Start counting from beginWord
        
        while queue:
            # Process all words at current level before incrementing level
            for _ in range(len(queue)):
                current_word = queue.popleft()
                
                if current_word == endWord:
                    return level
                
                # Generate all possible patterns for current word
                for i in range(len(current_word)):
                    pattern = current_word[:i] + "#" + current_word[i+1:]
                    
                    # Explore all unvisited neighbors matching any pattern
                    for neighbor in pattern_map[pattern]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
            
            level += 1  # Move to next transformation level
        
        return 0  # No path found


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    beginWord1 = "hit"
    endWord1 = "cog"
    wordList1 = ["hot","dot","dog","lot","log","cog"]
    print(solution.ladderLength(beginWord1, endWord1, wordList1))  # Expected Output: 5

    # Test case 2
    beginWord2 = "hit"
    endWord2 = "cog"
    wordList2 = ["hot","dot","dog","lot","log"]
    print(solution.ladderLength(beginWord2, endWord2, wordList2))  # Expected Output: 0

    # Test case 3 (Custom: shortest path with one step)
    beginWord3 = "a"
    endWord3 = "c"
    wordList3 = ["b", "c"]
    print(solution.ladderLength(beginWord3, endWord3, wordList3))  # Expected Output: 2