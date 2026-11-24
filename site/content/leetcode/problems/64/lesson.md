# Minimum Path Sum

Each cell of a rectangular grid has a weight from 0 to 200. Starting at the top left, move right or down one cell at a time until you reach the bottom right. Return the smallest total weight, counting both endpoints. Each dimension ranges from 1 to 200. [Official problem and constraints](https://leetcode.com/problems/minimum-path-sum/)

## Work through the inputs

- A single column `[[2], [0], [7], [1]]` costs `10`. Every move is down, and the zero still counts as a visited cell.
- In `[[1, 9, 1, 1], [2, 2, 8, 1], [9, 1, 1, 1]]` the cheapest route is down, right, down, right, right. The six weights add to `8`.
- A single cell `[[0]]` costs `0`. The start and finish are the same cell, counted once.
- In a two-by-three grid of ones, every legal path costs `4`. When candidates tie, either would give the same total.

## Memoize the cost from each cell

Start at the top left and ask how much it costs to finish from there. At the destination, the answer is just its own weight. At any other cell, add its weight to the minimum cost from its valid down and right neighbors. On the bottom edge, only right is legal. On the right edge, only down is legal.

Each move reduces the number of steps remaining. Inducting on that number gives the recurrence: the destination is correct, and every other path must take one of the valid next steps before following a path covered by the induction hypothesis. Memoization makes each cell's first result available to every later call that needs it.

The trace fills in the costs as recursive calls return. A blank cell has yet to be saved. For the single column, the saved costs appear from bottom to top as `1, 8, 8, 10`. The highlighted cell is the one just saved.

## Keep a single row of costs

For a forward scan, store the cheapest cost **to** reach a cell. The origin starts at its own weight. On the first row the only predecessor is to the left, and on the first column it's above. Everywhere else, take the cheaper predecessor and add the current weight.

In a left-to-right scan, just before writing column `c`, its slot still holds the cost from the row above. Slot `c - 1` has already been updated to the current row. These are exactly the two candidates for an interior cell. The boundary updates use their sole predecessor, and the origin has none. This preserves the invariant at each step, so the last slot eventually holds the cost to reach the destination.

Each frame shows the row immediately after an update. The highlight marks the slot just written. Slots to its left reflect the current row, and those to its right reflect the previous row or are blank during the first row. The single-column trace shows `2, 2, 9, 10`, one running total per row.

## Compare the costs

For `R` rows and `C` columns, both solvers take `O(RC)` time with tracing off. Memoization keeps `O(RC)` cached costs and up to `O(R + C)` nested calls. The forward scan eliminates recursion and needs `O(C)` auxiliary space. Both leave the caller's grid intact and return the cost alone.

Tracing copies a whole grid or a single row per update so each frame preserves its own state. The examples are bounded to at most 12 cell updates each. An independent check propagates distances along diagonals to verify the costs shown in both traces.

The source map records the archived solver as provenance for this problem. The lesson and its two annotated implementations were authored for this curriculum.
