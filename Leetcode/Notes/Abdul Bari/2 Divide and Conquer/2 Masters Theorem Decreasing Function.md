# 2.2 Master's Theorem for Decreasing Functions

## Overview

This lecture explores the Master's Theorem in the context of decreasing functions. Through an analysis of previously discussed recurrence relations, we derive general forms and discuss implications for different coefficients. This session builds on earlier content, so viewing prior videos (1 to 4) is recommended for a complete understanding.

## Examples of Recurrence Relations

We review several key recurrence relations and their solutions to lay the groundwork for understanding the Master's Theorem for decreasing functions:

- `T(n) = T(n-1) + 1` yields `O(n)`.
- `T(n) = T(n-1) + n` yields `O(n^2)`.
- `T(n) = T(n-1) + log(n)` yields `O(n log n)`.
- `T(n) = 2T(n-1) + 1` yields `2^n`.

## General Form of Recurrence Relations

The general form for our decreasing function recurrence relations is given by:

```plaintext
T(n) = aT(n-b) + f(n)
```

Where:

- `a > 0`: Coefficient of the recursive term.
- `b > 0`: The subtractive constant in the recursive call.
- `f(n)`: An additional function which we assume is in the form of `O(n^k)`, where `k >= 0`.

## Key Observations and Cases

From our observations of various coefficients and their effects, we can categorize the outcomes into three primary cases:

### Case 1: Coefficient `a = 1`

- The function `f(n)` is effectively multiplied by `n`.
- If `f(n) = n^k`, the recurrence solves to `O(n^(k+1))`.

### Case 2: Coefficient `a > 1`

- The function `f(n)` is multiplied by `a^n`.
- Adjustments for `b` greater than 1 might lead to further divisions, such as `n/b`.

### Case 3: Coefficient `a < 1`

- The function simplifies to `f(n)`, maintaining the order `O(n^k)`.

## Practical Application of Master's Theorem

By understanding these cases, one can effectively solve any recurrence relation of the decreasing form. It is critical to spend time understanding these relationships through practice and application to fully grasp their implications and use them proficiently in algorithm analysis.

## Summary

This lecture solidified the application of the Master's Theorem for decreasing functions in recurrence relations. The categorization into different cases based on the coefficient `a` provides a structured approach to solving these problems. Students are encouraged to review the examples provided and practice deriving these relations to enhance their understanding and retention of the material.
