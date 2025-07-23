# 2.4.1 Master's Theorem in Algorithms for Dividing Functions (Part-1)

## Overview

This lecture examines the Master's Theorem, a pivotal tool in determining the time complexity of divide-and-conquer algorithms through recurrence relations. The general form of a recurrence relation covered in this session is:
\[ T(n) = aT\left(\frac{n}{b}\right) + f(n) \]
where \(a \geq 1\), \(b > 1\), and \(f(n)\) is typically of the form \(\Theta(n^k (\log n)^p)\).

## Definitions

- **a**: Number of recursive calls
- **b**: Input size reduction factor per call
- **f(n)**: Non-recursive cost
- **k**: Exponent of n in \(f(n)\)
- **p**: Exponent of \(\log n\) in \(f(n)\)

## Theorem Analysis

Based on the values \( \log_b a \) (logarithm of a to the base b) and \(k\), we distinguish three main cases:

### Case 1: \(\log_b a > k\)

- **Condition**: If the logarithmic comparison of the number of subproblems \(a\) to the size reduction factor \(b\) exceeds the power of \(n\) in \(f(n)\).
- **Complexity**: \(\Theta(n^{\log_b a})\)

### Case 2: \(\log_b a = k\)

- **Sub-cases** based on the value of \(p\):
  1. **\(p > -1\)**: Complexity is \(\Theta(n^k (\log n)^{p+1})\).
  2. **\(p = -1\)**: Complexity is \(\Theta(n^k \log(\log n))\).
  3. **\(p < -1\)**: Complexity simplifies to \(\Theta(n^k)\), ignoring \(\log n\) components.

### Case 3: \(\log_b a < k\)

- **Condition**: If the growth rate of the non-recursive work \(f(n)\) exceeds the expansion rate due to recursive calls.
- **Sub-cases**:
  1. **\(p \geq 0\)**: Complexity is \(\Theta(n^k (\log n)^p)\).
  2. **\(p < 0\)**: Complexity simplifies to \(\Theta(n^k)\).

## Examples

To illustrate these cases, consider the following recurrence relations:

1. **Example for Case 1**:
   \[ T(n) = 2T\left(\frac{n}{2}\right) + 1 \]
   - \(a = 2, b = 2, f(n) = 1\)
   - Since \(\log_2 2 = 1 > 0 (k)\), complexity is \(\Theta(n)\).

2. **Example for Case 2**:
   \[ T(n) = 4T\left(\frac{n}{2}\right) + n \]
   - \(a = 4, b = 2, k = 1\), equal to \(\log_2 4\)
   - As \(p = 0\), complexity is \(\Theta(n^2)\).

3. **Example for Case 3**:
   \[ T(n) = 2T\left(\frac{n}{2}\right) + n^2 \]
   - Here, \(k = 2\) surpasses \(\log_2 2 = 1\)
   - Complexity is \(\Theta(n^2)\).

## Summary

Master's Theorem provides a systematic approach to solve recurrence relations for divide-and-conquer algorithms, offering clear computational complexity estimations based on the nature of the problem's division and the work done per division. This theorem is crucial for predicting algorithm performance and optimizing computational tasks effectively.
