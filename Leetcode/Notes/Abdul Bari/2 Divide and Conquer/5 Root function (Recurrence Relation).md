# 2.5 Root Function (Recurrence Relation)

## Overview

This lecture delves into the analysis of a recurrence relation where the recursive call is made by passing the square root of the input size, `n`. We'll explore how this affects the recursion depth and the overall time complexity of the algorithm.

## Recurrence Relation Formation

- **Base Condition**: We start with `n > 2` because solving the recurrence for values less than or equal to 2 might not be feasible.
- **Recurrence Formula**: The recurrence relation derived from the algorithm is given by:
  - `T(n) = T(sqrt(n)) + 1`

## Solving the Recurrence

To solve this recurrence relation, we employ a method of repeated substitution:

### Step-by-Step Substitution

1. **First Substitution**:
   - Substitute once: `T(n) = T(n^(1/2)) + 1`
2. **Second Substitution**:
   - Substitute twice: `T(n) = T(n^(1/4)) + 2`
3. **Third Substitution**:
   - Substitute three times: `T(n) = T(n^(1/8)) + 3`

### General Form After k Substitutions

- After `k` substitutions, the relation becomes:
  - `T(n) = T(n^(1/2^k)) + k`

### Assumption for Further Analysis

- Assume `n` is a power of 2, i.e., `n = 2^m`.
- After `k` substitutions, `T(2^m) = T(2^(m/2^k)) + k`.
- We then assume the reduction reaches a base case when `2^(m/2^k) = 2`, leading to `m/2^k = 1`.

### Solving for k

- The equation `m/2^k = 1` simplifies to `m = 2^k`.
- Solving for `k` gives `k = log_2(m)`.
- Substituting `m = log_2(n)` into the equation for `k` results in:
  - `k = log_2(log_2(n))`

## Complexity Analysis

- The depth of the recursion, and thus the time complexity of the algorithm, is Θ(log log n), where `n` is the size of the input.

## Practical Implications and Alternative Approaches

- **Back Substitution Method**: The method used in this lecture provides a practical example of solving complex recurrence relations by iteratively reducing the problem size to its root.
- **Master's Theorem**: Alternatively, one could apply the Master's Theorem for dividing recurrences to directly derive the time complexity.

## Summary

This lecture covered the derivation and solution of a recurrence relation for an algorithm using the root function as a recursive call. By understanding and applying the method of repeated substitutions and making logical assumptions about the problem size, we arrived at a time complexity of Θ(log log n). This approach illustrates the depth and precision required in analyzing algorithms with non-linear recurrence relations.
