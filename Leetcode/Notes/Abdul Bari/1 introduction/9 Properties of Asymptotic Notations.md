# 1.9 Properties of Asymptotic Notations

## Overview

This lecture segment explores essential properties of asymptotic notations including Big O, Omega, and Theta. These notations help describe the upper, lower, and tight bounds of algorithms with respect to their input sizes.

## General Property

- **Definition**: If a function `f(n)` is `O(g(n))`, then `a * f(n)` is also `O(g(n))` for any constant `a`.
- **Example**:
  - Consider `f(n) = 2n^2 + 5`. If `f(n)` is `O(n^2)`, then `7 * f(n) = 14n^2 + 35` is also `O(n^2)`.

## Reflexive Property

- **Definition**: For any function `f(n)`, it holds that `f(n)` is `O(f(n))`.
- **Example**:
  - If `f(n) = n^2`, then `f(n)` is `O(n^2)`.
  
## Transitive Property

- **Definition**: If `f(n)` is `O(g(n))` and `g(n)` is `O(h(n))`, then `f(n)` is `O(h(n))`.
- **Example**:
  - Let `f(n) = n`, `g(n) = n^2`, and `h(n) = n^3`. If `n` is `O(n^2)` and `n^2` is `O(n^3)`, then `n` is `O(n^3)`.

## Symmetric Property (Theta Notation Only)

- **Definition**: If `f(n)` is `Θ(g(n))`, then `g(n)` is `Θ(f(n))`.
- **Example**:
  - If `f(n) = n^2` and `g(n) = n^2`, then `f(n)` is `Θ(g(n))` and vice versa.

## Mixed Properties

- **Big O and Omega Relation**:
  - If `f(n)` is `O(g(n))`, then `g(n)` is `Ω(f(n))` and vice versa.
  - **Example**: If `f(n) = n` and `g(n) = n^2`, then `n` is `O(n^2)` and `n^2` is `Ω(n)`.

## Practical Implications

### Combined Function Analysis

- **Sum of Functions**:
  - If `f(n)` is `O(g(n))` and `d(n)` is `O(e(n))`, then `f(n) + d(n)` is `O(max(g(n), e(n)))`.
  - **Example**: For `f(n) = n` and `d(n) = n^2`, `f(n) + d(n)` is `O(n^2)`.

### Product of Functions

- **Product Rule**:
  - If `f(n)` is `O(g(n))` and `d(n)` is `O(e(n))`, then `f(n) * d(n)` is `O(g(n) * e(n))`.
  - **Example**: If `f(n) = n` and `d(n) = n^2`, then `f(n) * d(n)` is `O(n^3)`.

## Summary

This lecture provides a foundational understanding of asymptotic notations, emphasizing their applicability in evaluating the efficiency of algorithms. The properties discussed, such as general, reflexive, transitive, and symmetric, are crucial for proper algorithm analysis and form the core of theoretical computer science studies.
