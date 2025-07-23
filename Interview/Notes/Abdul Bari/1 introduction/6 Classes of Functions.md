# 1.6 Classes of Functions

## Overview

This lecture segment examines the various classes of functions typically encountered in time complexity analysis. We will define each class and discuss how they represent the efficiency of different algorithms relative to the size of their input.

## Constant Time Complexity: O(1)

- **Description**: Time complexity is considered constant if it does not depend on the size of the input.
- **Examples**:
  - Any operation or function that executes in a fixed amount of time, such as accessing an array element or returning a static value, regardless of whether it takes 2, 5, or 5000 units of time.

## Logarithmic Time Complexity: O(log n)

- **Description**: Complexity increases logarithmically with the size of the input.
- **Base Variance**: The base of the logarithm (base 2, base 3, etc.) affects the growth rate, but all are considered logarithmic.
- **Applications**: Algorithms that divide the problem space in half each iteration, such as binary search.

## Linear Time Complexity: O(n)

- **Description**: Complexity is directly proportional to the input size.
- **Examples**:
  - Functions like `f(n) = 2n + 3` or `f(n) = 500n + 700`. Regardless of additional constants or coefficients, these functions are linear because they scale directly with `n`.

## Polynomial Time Complexity

### Quadratic: O(n²)

- **Description**: Time complexity grows quadratically with input size.
- **Common in**: Algorithms that involve nested iterations over the data, such as bubble sort or simple matrix multiplication.

### Cubic: O(n³)

- **Applications**: More complex polynomial algorithms, such as naive matrix multiplication involving three nested loops.

## Exponential Time Complexity: O(2^n), O(3^n), etc

- **Description**: Complexity doubles with each additional input unit, leading to very rapid increases in execution time.
- **Context**: Typically seen in brute-force algorithms or those that generate all possible combinations of inputs.

## Summary

Time complexities provide a theoretical framework for estimating algorithm performance. By classifying functions into constant, logarithmic, linear, polynomial (quadratic and cubic), and exponential categories, we can better understand and predict how changes in input size impact execution time. These classes serve as a fundamental tool in algorithm design and analysis, guiding the development of more efficient computational solutions.
