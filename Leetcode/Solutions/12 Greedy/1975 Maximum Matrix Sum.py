# MAXIMUM MATRIX SUM

# Problem number: 1975
# Difficulty: Medium
# Tags: Greedy, Matrix
# link: https://leetcode.com/problems/maximum-matrix-sum/

from typing import List

class Solution:
    """
    This problem involves maximizing the sum of a matrix by performing operations that multiply any 
    two adjacent elements by -1. The key is to consider the overall sum of the matrix and the number 
    of negative elements to determine the optimal result. The approach involves calculating the sum of 
    absolute values of all elements and then adjusting for the smallest absolute value if the number of 
    negative elements is odd.

    T.C. : O(n^2)
    S.C. : O(1)

    Input:
        - matrix : List[List[int]] : n x n integer matrix

    Output:
        - int : maximum sum of the matrix's elements
    """
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        n = len(matrix)
        total_sum = 0
        min_abs_value = float('inf')
        negative_count = 0
        
        # iterate through the matrix
        for i in range(n):
            for j in range(n):
                value = matrix[i][j]
                total_sum += abs(value)
                min_abs_value = min(min_abs_value, abs(value))
                if value < 0:
                    negative_count += 1
        
        # If the number of negative values is odd, we need to subtract twice the minimum absolute value
        if negative_count % 2 != 0:
            total_sum -= 2 * min_abs_value
        
        return total_sum

# Sample Inputs
matrix = [[1, -1], [-1, 1]]

# Expected Output : 4
print(Solution().maxMatrixSum(matrix))