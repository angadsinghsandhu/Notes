# Backtracking Problem Solving Guide

Welcome to this guide on solving backtracking problems, a common topic in coding interviews and challenges. We will explore a versatile backtracking template that can be applied to various problems, such as the N-Queens problem and Sudoku solver.

---

## Introduction to Backtracking

Backtracking is a problem-solving technique that involves exploring all possible solutions to a problem by building up candidates and discarding them if they do not satisfy the problem constraints. This approach is useful for problems that require finding all possible solutions, such as puzzles and combinatorial problems.

### Key Concepts in Backtracking

1. **State**: Represents a potential solution at any given point during the problem-solving process. For example, in the N-Queens problem, a state might be the placement of some queens on a chessboard.

2. **Valid State**: A state that meets all the problem constraints. In the N-Queens problem, a valid state ensures that no two queens can attack each other.

3. **Candidate**: A possible option that can be added to the current state to form a new state. For instance, in the N-Queens problem, a candidate could be the placement of the next queen on the board.

4. **Backtracking**: The process of undoing a previous decision (state) to explore alternative candidates when a valid solution is not found.

---

## Backtracking Template Overview

The backtracking template consists of four primary functions:

1. **`is_valid_state(state, n)`**: Validates whether a given state is a final solution. Returns a boolean.

2. **`get_candidates(state, n)`**: Finds a list of candidates that can be used to construct the next state.

3. **`search(state, solutions, n)`**: A recursive function that calls the previous two helper functions to explore possible states and find valid solutions.

4. **`solve(n)`**: The main function that initializes the process, calls the search function, and returns the list of valid solutions.

### Using the Template

This template is versatile and can be adapted to solve various backtracking problems. Let’s explore its application through examples.

---

## Example 1: Solving the N-Queens Problem

### Problem Statement 1

Given an integer `n`, return all distinct solutions to the N-Queens puzzle. A solution must ensure that no two queens attack each other on an `n x n` chessboard.

### Representation of the Problem 1

Instead of using a 2D array, we can represent the board as a 1D list where each index corresponds to a row, and the value at that index represents the column position of the queen in that row.

### Implementation 1

1. **`solve(n)` Function**:
    - Initializes an empty list for solutions.
    - Starts with an empty state (no queens placed yet).
    - Calls the `search` function to explore possible solutions.
    - Returns the list of valid solutions.

2. **`is_valid_state(state, n)` Function**:
    - Checks if the length of the state is `n`, meaning all queens are placed.
    - If true, it verifies that no queens can attack each other.

3. **`get_candidates(state, n)` Function**:
    - Identifies the next position to place a queen.
    - Filters out candidates that are invalid based on the current state (e.g., columns or diagonals already occupied).

4. **`search(state, solutions, n)` Function**:
    - Recursively explores each candidate.
    - Adds valid states to the solutions list.
    - Backtracks by removing the last candidate and continues searching.

### Example Code Snippet 1

```python
def solve(n):
    solutions = []
    state = []
    search(state, solutions, n)
    return solutions

def is_valid_state(state, n):
    return len(state) == n

def get_candidates(state, n):
    if not state:
        return range(n)
    candidates = set(range(n))
    position = len(state)
    for row, column in enumerate(state):
        candidates.discard(column)
        distance = position - row
        candidates.discard(column + distance)
        candidates.discard(column - distance)
    return candidates

def search(state, solutions, n):
    if is_valid_state(state, n):
        solutions.append(state.copy())
        return
    for candidate in get_candidates(state, n):
        state.append(candidate)
        search(state, solutions, n)
        state.pop()
```

### Example Output 1

For `n = 4`, the output will be two valid configurations of the queens on a 4x4 chessboard.

---

## Example 2: Solving the Sudoku Problem

### Problem Statement 2

Write a program to solve a Sudoku puzzle by filling the empty cells with digits from 1 to 9 such that each row, column, and 3x3 sub-box contains all the digits from 1 to 9 exactly once.

### Representation of the Problem 2

The board is represented as a 9x9 grid. Empty cells are denoted by a dot `.`.

### Implementation 2

1. **`solve(board)` Function**:
    - Modifies the board in place.
    - Calls the `search` function to find the solution.

2. **`is_valid_state(board)` Function**:
    - Validates the board by checking each row, column, and sub-box.

3. **`get_candidates(board, row, col)` Function**:
    - Identifies valid digits that can be placed in a specific cell based on the current board state.

4. **`search(board)` Function**:
    - Recursively fills the board with valid digits.
    - Backtracks if a digit placement leads to an invalid board.

### Example Code Snippet 2

```python
def solve(board):
    search(board)

def is_valid_state(board):
    for row in get_rows(board):
        if set(row) != set('123456789'):
            return False
    for col in get_columns(board):
        if set(col) != set('123456789'):
            return False
    for grid in get_grids(board):
        if set(grid) != set('123456789'):
            return False
    return True

def get_candidates(board, row, col):
    used_digits = set()
    used_digits.update(get_row(board, row))
    used_digits.update(get_column(board, col))
    used_digits.update(get_grid(board, row, col))
    return set('123456789') - used_digits

def search(board):
    if is_valid_state(board):
        return True
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                for candidate in get_candidates(board, row, col):
                    board[row][col] = candidate
                    if search(board):
                        return True
                    board[row][col] = '.'
                return False
    return True
```

### Example Output 2

The program will fill the Sudoku board with a valid configuration that satisfies all constraints.

---

## Recap

### Backtracking Template

- **`is_valid_state`**: Validates a state.
- **`get_candidates`**: Generates valid candidates.
- **`search`**: Recursively explores states.
- **`solve`**: Initiates the backtracking process and returns solutions.

### Identifying Backtracking Problems

Backtracking problems often involve finding all possible solutions and may ask for solutions to be returned in any order. Practice with problems like the N-Queens, Sudoku, and subsets to get familiar with the pattern.

---

## Additional Resources

For more practice, visit [LeetCode Backtracking Problems](https://leetcode.com/tag/backtracking/).

---
