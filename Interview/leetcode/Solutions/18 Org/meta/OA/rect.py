"""
File: rect.py

You are given operations, an array containing the following two types of operations:

- [0, a, b]: Create and save a rectangle of size a × b.
- [1, a, b]: Answer the question: "Could every one of the earlier saved rectangles fit in a box of size a × b?" It is possible to rotate rectangles by 90 degrees; i.e., a rectangle of dimensions a × b can be rotated so that its dimensions are b × a. Note: We're trying to fit each rectangle within the box separately (not all at the same time).

Your task is to return an array of booleans, representing the answers to the second type of operation, in the order they appear.

Note: The operations should be processed iteratively, so when operations[i] is executed only the results of the previous operations 0, 1, ..., i - 1 are available.

Example:

For operations = [[1, 1, 1]], the output should be:

solution(operations) = [True]

There are no rectangles, so they all can fit in any box.

For:

operations = [
    [0, 1, 3],
    [0, 4, 2],
    [1, 3, 4],
    [1, 3, 2]
]

the output should be:

solution(operations) = [True, False]

Explanation:

1. A 1 × 3 rectangle is added.
2. A 4 × 2 rectangle is added.
3. We need to check if it's possible to store each of the rectangles from operations 1 and 2 into a 3 × 4 area.
   - The rectangle from the 1st operation can be stored as-is.
   - The rectangle from the 2nd operation can be rotated to become 2 × 4, and after that, it will fit.
   - Both rectangles will fit, so add a True to the result.
4. We need to check if it's possible to store each of the rectangles from operations 1 and 2 into a 3 × 2 area.
   - The rectangle from the 1st operation can be rotated to become 3 × 1, and after that, it will fit.
   - The rectangle from the 2nd operation will not fit, even if it's rotated.
   - Not all rectangles could be stored, so add a False to the result.

So the final answer is [True, False].
"""

class Solution:
    """
    The Solution class contains methods to process a list of operations involving rectangles and queries.
    The general approach is to keep track of the maximum dimensions of the rectangles added so far,
    considering possible rotations. When a query operation is encountered, we check if the box dimensions
    are sufficient to fit the largest rectangle (in terms of width and height) added so far.

    The class provides an efficient way to answer each query by maintaining two variables:
    - max_min_side: the maximum among the minimum sides of all rectangles added.
    - max_max_side: the maximum among the maximum sides of all rectangles added.

    This allows us to answer each query in constant time.
    """

    def rectangleOperations(self, operations):
        """
        Processes a list of operations and returns the answers to the query operations.

        Args:
            operations (List[List[int]]): A list of operations, where each operation is of the form [op_type, a, b].

        Returns:
            List[bool]: A list of booleans representing the answers to the query operations.

        Thought Process:
        - For each add operation [0, a, b], update the maximum dimensions considering rotation.
        - For each query operation [1, a, b], check if both the maximum dimensions are less than or equal to
          the query box dimensions (considering rotation).
        - Since rotation is allowed, we always consider the minimum and maximum sides for comparison.

        Time Complexity: O(n), where n is the number of operations.
        Space Complexity: O(1), as we only maintain a few variables regardless of the input size.
        """
        max_min_side = 0
        max_max_side = 0
        result = []

        for op in operations:
            op_type, a, b = op
            min_side = min(a, b)
            max_side = max(a, b)

            if op_type == 0:
                # Update the maximum dimensions
                max_min_side = max(max_min_side, min_side)
                max_max_side = max(max_max_side, max_side)
            elif op_type == 1:
                # Check if the box can fit all rectangles added so far
                box_min_side = min_side
                box_max_side = max_side

                can_fit = (max_min_side <= box_min_side) and (max_max_side <= box_max_side)
                result.append(can_fit)
            else:
                # Invalid operation type, you may handle errors as needed
                continue

        return result

# Sample usage
solution = Solution()

# Sample Input 1
operations1 = [
    [1, 1, 1]
]
result1 = solution.rectangleOperations(operations1)
print(f"Sample Output 1: {result1}")  # Expected Output: [True]

# Sample Input 2
operations2 = [
    [0, 1, 3],
    [0, 4, 2],
    [1, 3, 4],
    [1, 3, 2]
]
result2 = solution.rectangleOperations(operations2)
print(f"Sample Output 2: {result2}")  # Expected Output: [True, False]

# Additional Sample Input
operations3 = [
    [0, 2, 2],
    [0, 3, 5],
    [1, 3, 5],
    [0, 4, 4],
    [1, 4, 5],
    [1, 2, 2]
]
result3 = solution.rectangleOperations(operations3)
print(f"Sample Output 3: {result3}")  # Expected Output: [True, True, False]
