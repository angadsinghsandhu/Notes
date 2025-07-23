# 2.9 Strassen's Matrix Multiplication

## Overview

Strassen's Matrix Multiplication is an advanced algorithm that applies the divide and conquer strategy to improve the efficiency of matrix multiplication. This lecture covers the standard matrix multiplication approach, the application of divide and conquer, and Strassen's enhancements.

## Standard Matrix Multiplication

- **Introduction**: Multiplication of two matrices occurs when the number of columns in the first matrix equals the number of rows in the second. The resulting matrix will have the same number of rows as the first matrix and the same number of columns as the second.
- **Example**:
  - For two 2x2 matrices **A** and **B**, the resultant matrix **C** will also be 2x2.
  - Each element **C(i, j)** is computed as the sum of products of corresponding elements from row **i** of **A** and column **j** of **B**.

## Divide and Conquer Strategy

- **Concept**: This strategy involves breaking the problem into smaller subproblems, solving them independently, and combining their results to solve the larger problem.
- **Application**: For matrices larger than 2x2, the problem is divided until subproblems of manageable size (2x2 matrices) are obtained, which are then multiplied directly.

## Strassen's Algorithm

- **Improvement**: Strassen's algorithm reduces the complexity of matrix multiplication by decreasing the number of required multiplications.
- **Process**:
  - **Subdivision**: Each matrix is divided into four submatrices until they reach a base size of 2x2.
  - **Base Case**: Direct multiplication of 2x2 matrices using specialized formulas that reduce the multiplication steps.
  - **Recursive Step**: Apply Strassen's formulas recursively to the submatrices to perform multiplications and additions efficiently.

## Algorithmic Details

- **Three Nested Loops**: Traditional matrix multiplication uses three nested loops, resulting in a time complexity of O(n^3).
- **Strassen's Approach**:
  - Reduces the multiplications in each recursive step from eight to seven using innovative formulas.
  - These formulas involve additional additions and subtractions but ultimately reduce the overall time complexity.

## Time Complexity Analysis

- **Standard Matrix Multiplication**: O(n^3) due to three nested loops.
- **Strassen's Algorithm**: Improves complexity to approximately O(n^2.81), leveraging the divide and conquer strategy and fewer multiplications per recursive step.

## Practical Implications

- **Efficiency**: Strassen's algorithm is particularly beneficial for large matrices where its reduced complexity significantly cuts down computation time.
- **Application Scenarios**: Ideal for computer graphics, scientific computing, and other fields requiring heavy matrix calculations.

## Summary

Strassen's Matrix Multiplication algorithm represents a significant advancement in computational mathematics by applying divide and conquer techniques to reduce the number of multiplications. This lecture detailed both the traditional and Strassen's methods, emphasizing the efficiency gains achieved through innovative algorithmic strategies.
