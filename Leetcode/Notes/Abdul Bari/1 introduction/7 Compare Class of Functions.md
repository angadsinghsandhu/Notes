# 1.7 Compare Class of Functions

## Overview

This lecture focuses on understanding the relative growth rates of different classes of functions used in time complexity analysis. We will examine how these functions are ordered in terms of their computational weight and the implications this has for algorithm performance as the input size increases.

## Ordering of Complexity Classes

We categorize common time complexities in increasing order of growth as follows:

- **Constant Time: O(1)**: Independent of input size.
- **Logarithmic Time: O(log n)**: Grows slower compared to linear time, increasing logarithmically with input size.
- **Linear Time: O(n)**: Increases directly in proportion to the input size.
- **Linearithmic Time: O(n log n)**: Combines linear and logarithmic growth, common in efficient sorting algorithms like mergesort.
- **Polynomial Time**:
  - **Quadratic Time: O(n²)**: Grows as the square of the input size.
  - **Cubic Time: O(n³)**: Grows as the cube of the input size.
- **Exponential Time: O(2^n), O(3^n), etc.**: Grows exponentially, much faster than polynomial time.

## Growth Rate Comparison

To demonstrate the growth rates of these complexities, consider the following comparisons with specific values of `n`:

- **For `n = 1`**:
  - Logarithmic: log(1) = 0
  - Linear: n = 1
  - Quadratic: n² = 1
  - Exponential: 2^n = 2
- **For `n = 2`**:
  - Logarithmic: log(2) = 1
  - Linear: n = 2
  - Quadratic: n² = 4
  - Exponential: 2^n = 4
- **For `n = 8`**:
  - Logarithmic: log(8) = 3
  - Linear: n = 8
  - Quadratic: n² = 64
  - Exponential: 2^n = 256

These values illustrate how, for smaller `n`, the differences might not be significant, but as `n` increases, the growth rate differences become much more pronounced.

## Visualizing Growth Rates

Imagine plotting these complexities on a graph:

- The logarithmic line starts very steep and flattens out, indicating a slow increase as `n` grows.
- The linear line increases steadily at a constant angle.
- The quadratic and cubic lines start slower but begin to rise rapidly, overtaking the linear and logarithmic lines.
- The exponential line starts the slowest but then skyrockets, surpassing all other complexities as `n` increases.

## Summary

Understanding these growth rates is crucial for selecting the appropriate algorithm based on the expected input size. It helps in predicting performance and optimizing algorithms efficiently. The key takeaway is that as the input size grows, even seemingly small differences in the big O notation can lead to significant differences in performance.
