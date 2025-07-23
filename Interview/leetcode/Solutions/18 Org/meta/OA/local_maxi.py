"""
File: local_maxi.py

You are given a matrix of integers matrix, your goal is to find all local maximums in it. An element is considered to be a local maximum if it is not zero and there are no greater or equal elements in its region. The region for the element matrix[i][j] is the square with the side length of matrix[i][j] * 2 + 1 and center coordinates at (i, j), excluding the square's corner elements. The coordinates of the element are 0-based indices of the corresponding row and column.

Note: If the region is not fully inside the matrix, no special rules are applied. You should only consider the part of the region within the matrix.

Return the 2-dimensional array, where each element is the array of size 2, containing coordinates (row, col) of every local maximum within matrix. The coordinates in the resulting array should be sorted in ascending order by row index or, in case of a tie, by column index.

Note: You are not expected to provide the most optimal solution, but a solution with time complexity not worse than O(matrix.length^2 × matrix[0].length^2) will fit within the execution time limit.

Example:

For:

matrix = [
  [3, 0, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 2, 0, 0],
  [0, 0, 0, 0, 0]
]

The output should be:

solution(matrix) = [[0, 0], [2, 2]]

Explanation:

- For matrix[0][0] = 3, there are two non-zero elements inside the region: matrix[1][2] = 1 and matrix[2][2] = 2. Since both are lower than the checked element, the matrix[0][0] = 3 is a local maximum. Coordinates [0, 0] are appended to the resulting array.
- For matrix[1][2] = 1, there is one non-zero element inside the region — matrix[2][2] = 2. One of the elements within the region is not lower than the checked element: matrix[2][2] > matrix[1][2]. So, the matrix[1][2] = 1 is not a local maximum.
- For matrix[2][2] = 2, there is one non-zero element inside the region — matrix[1][2] = 1. Since matrix[1][2] < matrix[2][2], the matrix[2][2] = 2 is a local maximum. Coordinates [2, 2] are appended to the resulting array.
- The resulting array is [[0, 0], [2, 2]].
"""

class Solution:
    """
    The Solution class contains methods to find all local maximums in a given matrix as per the defined criteria.
    The general approach is to iterate over all non-zero elements in the matrix, and for each, define its region
    based on its value. Then, we check all positions within that region (excluding the corners and the element itself)
    to see if any non-zero element is greater than or equal to the current element. If none are found, the element is
    considered a local maximum.
    """

    def findLocalMaximums(self, matrix):
        """
        Finds all local maximums in the given matrix.

        Args:
            matrix (List[List[int]]): A 2D list of integers representing the matrix.

        Returns:
            List[List[int]]: A list of [row, col] coordinates of local maximums sorted as per the requirements.

        Thought Process:
        - For each non-zero element in the matrix, calculate its region based on its value.
        - Iterate over the region (excluding the corners and the element itself).
        - Check if any non-zero element within the region is greater than or equal to the current element.
        - If none are found, add the coordinates to the result list.
        - Finally, sort the result list by row index and then by column index.

        Time Complexity: O(n * m * max_s^2), where n and m are the dimensions of the matrix, and max_s is the maximum side length of the regions.
        Space Complexity: O(k), where k is the number of local maximums found.
        """
        n = len(matrix)
        m = len(matrix[0]) if n > 0 else 0
        result = []

        for i in range(n):
            for j in range(m):
                if matrix[i][j] != 0:
                    value = matrix[i][j]
                    s = value * 2 + 1

                    row_min = max(0, i - value)
                    row_max = min(n - 1, i + value)
                    col_min = max(0, j - value)
                    col_max = min(m - 1, j + value)

                    is_local_maximum = True

                    for r in range(row_min, row_max + 1):
                        for c in range(col_min, col_max + 1):
                            if (r == i and c == j):
                                continue  # Skip the element itself
                            # Exclude the corners
                            if abs(r - i) == value and abs(c - j) == value:
                                continue
                            if matrix[r][c] != 0 and matrix[r][c] >= value:
                                is_local_maximum = False
                                break
                        if not is_local_maximum:
                            break

                    if is_local_maximum:
                        result.append([i, j])

        # Sort the result as per the requirements
        result.sort(key=lambda x: (x[0], x[1]))
        return result

# Sample usage
solution = Solution()

# Sample Input
matrix = [
    [3, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0]
]

result = solution.findLocalMaximums(matrix)
print(f"Local maximums: {result}")  # Expected Output: [[0, 0], [2, 2]]