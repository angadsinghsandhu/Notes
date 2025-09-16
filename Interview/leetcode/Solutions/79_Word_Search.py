# TODO; revisit

# File: Leetcode/Solutions/79_Word_Search.py

"""
Problem Number: 79
Problem Name: Word Search
Difficulty: Medium
Tags: Backtracking, Matrix, DFS, Neetcode 150
Company (Frequency): Amazon, Microsoft, Apple, Google, Adobe (High)
Leetcode Link: <https://leetcode.com/problems/word-search/>

DESCRIPTION

Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

Example 1:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true

Example 2:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true

Example 3:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters.
"""

from typing import List
from collections import Counter

class Solution:
    """
    Thought Process:
    - Use backtracking with DFS to explore all possible paths starting from each cell.
    - Check if the word can be formed using the characters present in the grid (pruning).
    - Mark cells as visited temporarily during the DFS and restore them afterward.

    Approach:
    - For each cell in the grid, start a DFS if the cell matches the first character of the word.
    - Use backtracking to explore all four possible directions (up, down, left, right).
    - Track the current index in the word to determine when a complete match is found.
    - Optimize by checking character counts before starting the search to prune impossible cases.

    T.C.: O(n * m * k), where n is the number of rows, m is the number of columns, and k is the length of the word.
    S.C.: O(k)
    """

    def exist(self, board: List[List[str]], word: str) -> bool:
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        # Early exit if word is longer than the number of cells
        if len(word) > rows * cols:
            return False

        # Check if all characters in word are present in sufficient quantity
        board_counts = Counter(cell for row in board for cell in row)
        word_counts = Counter(word)
        for char, count in word_counts.items():
            if board_counts[char] < count:
                return False

        def backtrack(i: int, j: int, index: int) -> bool:
            # Check boundaries and character match
            if i < 0 or i >= rows or j < 0 or j >= cols or board[i][j] != word[index]:
                return False
            # Check if all characters are matched
            if index == len(word) - 1:
                return True
            # Mark as visited
            temp = board[i][j]
            board[i][j] = '#'
            # Explore all directions
            for dx, dy in directions:
                if backtrack(i + dx, j + dy, index + 1):
                    board[i][j] = temp  # Restore before returning
                    return True
            # Restore and backtrack
            board[i][j] = temp
            return False

        # Iterate through each cell to start the search
        for i in range(rows):
            for j in range(cols):
                if backtrack(i, j, 0):
                    return True
        return False

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    board1 = [["A","B","C","E"], ["S","F","C","S"], ["A","D","E","E"]]
    word1 = "ABCCED"
    print(solution.exist(board1, word1))  # Expected Output: True

    # Test case 2
    board2 = [["A","B","C","E"], ["S","F","C","S"], ["A","D","E","E"]]
    word2 = "SEE"
    print(solution.exist(board2, word2))  # Expected Output: True

    # Test case 3
    board3 = [["A","B","C","E"], ["S","F","C","S"], ["A","D","E","E"]]
    word3 = "ABCB"
    print(solution.exist(board3, word3))  # Expected Output: False