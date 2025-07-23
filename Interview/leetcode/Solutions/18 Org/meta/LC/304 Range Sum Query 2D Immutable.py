# RANGE SUM QUERY 2D - IMMUTABLE

# Problem number: 304
# Difficulty: Medium
# Tags: 2D Array, Dynamic Programming, Prefix Sum
# Link: https://leetcode.com/problems/range-sum-query-2d-immutable/

from typing import List

class NumMatrix:
    """
    The goal is to efficiently calculate the sum of elements in a submatrix.
    We can achieve this using a 2D prefix sum array, which allows us to answer sum queries in O(1) time.
    
    The idea is to precompute a sum matrix where each element (i, j) contains the sum of all elements
    from (0, 0) to (i, j) in the original matrix. Once we have this sum matrix, the sum of any submatrix
    can be computed using a simple inclusion-exclusion principle.
    
    There are two methods provided:
    1. Prefix Sum Method (Optimal)
    2. Naive Method (For comparison)
    """

    def __init__(self, matrix: List[List[int]]):
        """
        Prefix Sum approach to preprocess the matrix.
        We create a sum matrix where sum_matrix[i][j] holds the sum of all elements from (0, 0) to (i, j).
        
        T.C. for __init__: O(m * n), where m and n are the number of rows and columns in the matrix
        S.C. : O(m * n), for storing the sum matrix
        """
        if not matrix:
            return
        
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.sum_matrix = [[0] * (self.cols + 1) for _ in range(self.rows + 1)]
        
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                self.sum_matrix[i][j] = matrix[i-1][j-1] + self.sum_matrix[i-1][j] + self.sum_matrix[i][j-1] - self.sum_matrix[i-1][j-1]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        """
        Uses the precomputed sum matrix to calculate the sum of the rectangle in O(1) time.
        
        T.C. : O(1)
        S.C. : O(m * n), for storing the sum matrix
        """
        return (self.sum_matrix[row2 + 1][col2 + 1]
                - self.sum_matrix[row1][col2 + 1]
                - self.sum_matrix[row2 + 1][col1]
                + self.sum_matrix[row1][col1])

# Naive method (for comparison)
class NumMatrix_Naive:
    """
    A naive approach without preprocessing. We iterate over the matrix for each query.
    
    T.C. : O((row2 - row1 + 1) * (col2 - col1 + 1)) for sumRegion
    S.C. : O(1), no extra space used
    """
    
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total_sum = 0
        for i in range(row1, row2 + 1):
            for j in range(col1, col2 + 1):
                total_sum += self.matrix[i][j]
        return total_sum

# Best Method: The Prefix Sum Method is optimal due to O(1) query time complexity.
