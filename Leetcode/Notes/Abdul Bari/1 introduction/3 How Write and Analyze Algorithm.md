# 1.3 How to Write and Analyze an Algorithm

## Overview

This lecture covers the essential aspects of writing and analyzing algorithms, focusing on the flexibility of representation and the criteria for analysis.

## Writing an Algorithm

- **Flexibility in Representation**: When writing an algorithm, the syntax can be flexible. Unlike programming, where specific syntax and data types are required, algorithms can be written using pseudocode or simple descriptions that are understandable to the intended audience. This allows the use of various symbols or structures, like using assignment symbols from different programming languages (e.g., Pascal).
- **Importance of Clarity**: Regardless of the chosen syntax or symbols, the key is that the algorithm must be clear and understandable to everyone involved in the project, whether they are writing the program or using the algorithm to build solutions.

## Analyzing an Algorithm

- **Time Analysis**:
  - The primary criterion for analyzing an algorithm is its efficiency in terms of time. This involves estimating how much time an algorithm will take to complete, typically represented as a function of the size of the input (time complexity).
  - A simple algorithm's time can sometimes be represented as a constant or a function that does not depend on the input size.
  - In analysis, each operation (e.g., assignment, arithmetic operation) is often considered to take one unit of time, regardless of the complexity that might be involved when these operations are translated into actual machine instructions.

- **Space Analysis**:
  - The second major criterion is the space an algorithm uses, which includes counting the memory used by variables and any temporary or auxiliary storage required.
  - Like time complexity, space usage is expressed in terms of the amount of input but can also be a constant, especially for simpler algorithms.

- **Other Criteria**:
  - Depending on the application, other factors might be considered, such as data transfer, network consumption, power consumption, and CPU usage (especially in terms of how many CPU registers are used).
  - These factors are particularly relevant for applications that run on diverse devices or require efficient data handling and minimal power consumption.

## Example Analysis

- **Example Given**: Swapping two numbers.
  - **Time Complexity**: Analyzed by counting the number of statements executed, which in simple cases might be a small constant.
  - **Space Complexity**: Determined by the number of variables used, which in the given example was three, suggesting a constant space complexity.

## Summary

Writing and analyzing algorithms involve understanding not just the steps of the algorithm but also predicting how they will perform in terms of time and space requirements. Flexibility in writing and a methodical approach in analysis ensure that algorithms are both understandable and efficient in terms of computational resources.
