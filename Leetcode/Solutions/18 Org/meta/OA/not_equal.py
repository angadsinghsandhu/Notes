"""
File: not_equal.py

Given an array of integers numbers, your task is to count all numbers that are *not equal* to numbers[0] or numbers[1], if they exist in the array.

Assume that array indices are 0-based.

Note: You are not expected to provide the most optimal solution, but a solution with time complexity not worse than O(numbers.length^2) will fit within the execution time limit.

#### Example

- For numbers = [4, 3, 2, 3, 2, 5, 4, 3], the output should be solution(numbers) = 3.

  *Explanation:*
  - numbers[0] and numbers[1] are 4 and 3 respectively. There are three elements in numbers that are not equal to 4 or 3:
    - numbers[2] = 2
    - numbers[4] = 2
    - numbers[5] = 5
  - So, the answer is 3.

- For numbers = [3, 3, 1, 1, 3], the output should be solution(numbers) = 2.

  *Explanation:*
  - numbers[0] and numbers[1] are both 3. There are two elements in numbers that are not equal to 3:
    - numbers[2] = 1
    - numbers[3] = 1
  - So, the answer is 2.

- For numbers = [-2], the output should be solution(numbers) = 0.

  *Explanation:*
  - numbers[0] is -2, and numbers[1] does not exist, so the only requirement is to count numbers different from -2.
  - There are no elements in numbers that are not equal to -2, so the answer is 0.
"""

class Solution:
    """
    The Solution class contains methods to solve the problem of counting the number of elements in an array
    that are not equal to the first one or two elements. The general approach is to identify the first and
    second elements (if they exist) and iterate through the array to count elements that are different from them.
    """

    def countNotEqualToFirstTwo(self, numbers):
        """
        Counts all numbers in the array that are not equal to numbers[0] or numbers[1], if numbers[1] exists.

        Args:
            numbers (List[int]): An array of integers.

        Returns:
            int: The count of numbers not equal to numbers[0] or numbers[1].

        Thought Process:
        - Determine the values of numbers[0] and numbers[1] (if it exists).
        - Iterate through the array and count the elements that are not equal to these values.
        - Handle edge cases where the array has less than two elements.

        Time Complexity: O(n), where n is the length of the numbers array.
        Space Complexity: O(1), as we use a constant amount of extra space.
        """
        if not numbers:
            return 0

        first_value = numbers[0]
        second_value = numbers[1] if len(numbers) > 1 else None

        count = 0
        for num in numbers:
            if num != first_value and (second_value is None or num != second_value):
                count += 1

        return count

# Sample usage
solution = Solution()

# Sample Input 1
numbers1 = [4, 3, 2, 3, 2, 5, 4, 3]
result1 = solution.countNotEqualToFirstTwo(numbers1)
print(f"Sample Output 1: {result1}")  # Expected Output: 3

# Sample Input 2
numbers2 = [3, 3, 1, 1, 3]
result2 = solution.countNotEqualToFirstTwo(numbers2)
print(f"Sample Output 2: {result2}")  # Expected Output: 2

# Sample Input 3
numbers3 = [-2]
result3 = solution.countNotEqualToFirstTwo(numbers3)
print(f"Sample Output 3: {result3}")  # Expected Output: 0
