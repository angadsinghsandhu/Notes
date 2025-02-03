# TODO: new

# File: Leetcode/Solutions/212_Word_Search_II.py

"""
Problem Number: 212
Problem Name: Word Search II
Difficulty: Hard
Tags: Trie, Array, String, Backtracking, Matrix
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/word-search-ii/description/

DESCRIPTION

Given an `m x n` board of characters and a list of strings `words`, return all words on the board.

Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

---

#### Example 1:
**Input:**
```plaintext
board = [
  ["o","a","a","n"],
  ["e","t","a","e"],
  ["i","h","k","r"],
  ["i","f","l","v"]
]
words = ["oath","pea","eat","rain"]
```

**Output:**
```plaintext
["eat","oath"]
```

**Explanation:**  
The words "eat" and "oath" can be constructed from the board.

#### Example 2:
**Input:**
```plaintext
board = [
  ["a","b"],
  ["c","d"]
]
words = ["abcb"]
```

**Output:**
```plaintext
[]
```

**Explanation:**  
The word "abcb" cannot be constructed from the board.

#### Constraints:
- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `board[i][j]` is a lowercase English letter.
- `1 <= words.length <= 3 * 10^4`
- `1 <= words[i].length <= 10`
- `words[i]` consists of lowercase English letters.
- All the strings of `words` are unique.
"""

from typing import List

class TrieNode:
    """
    Trie Node class to store characters and references to child nodes.
    """
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.word = None    # To mark the end of a word

class Solution:
    """
    Thought Process:
    - The problem involves searching for multiple words in a 2D grid.
    - A brute-force approach would be inefficient due to the large number of words.
    - We can use a Trie data structure to store all words and perform a DFS with backtracking to search for words in the grid.
    - The Trie allows us to efficiently check if a sequence of characters forms a prefix of any word.
    - During DFS, we mark cells as visited to avoid reusing them in the same word.

    Input:
        board: List[List[str]] - A 2D grid of characters.
        words: List[str] - A list of words to search for in the grid.

    Output:
        List[str] - A list of words that can be constructed from the grid.
    """

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Approach:
        - Build a Trie from the list of words.
        - Perform DFS from each cell in the grid to search for words.
        - Use backtracking to mark cells as visited and restore them after exploration.
        - Collect all valid words found during the DFS.

        T.C.: O(M * N * 4^L) - Where M and N are the dimensions of the board, and L is the maximum length of a word.
        S.C.: O(W * L) - Where W is the number of words and L is the average length of a word.
        """
        # Initialize the Trie and insert all words
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word  # Mark the end of a word

        m, n = len(board), len(board[0])
        result = []

        def dfs(i: int, j: int, node: TrieNode):
            """
            DFS function to explore the board and find words.
            """
            char = board[i][j]
            if char not in node.children:
                return

            child = node.children[char]
            if child.word:
                result.append(child.word)
                child.word = None  # Avoid adding the same word multiple times

            board[i][j] = '#'  # Mark the cell as visited
            for x, y in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                if 0 <= x < m and 0 <= y < n and board[x][y] != '#':
                    dfs(x, y, child)
            board[i][j] = char  # Restore the cell

        # Perform DFS from each cell in the board
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)

        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    board1 = [
        ["o","a","a","n"],
        ["e","t","a","e"],
        ["i","h","k","r"],
        ["i","f","l","v"]
    ]
    words1 = ["oath","pea","eat","rain"]
    print(solution.findWords(board1, words1))  # Output: ["eat","oath"]

    # Test case 2
    board2 = [
        ["a","b"],
        ["c","d"]
    ]
    words2 = ["abcb"]
    print(solution.findWords(board2, words2))  # Output: []
