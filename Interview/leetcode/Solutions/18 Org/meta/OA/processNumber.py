"""
File: processNumber.py

You are given a string number consisting of digits, your task is to repeatedly apply the following operation to the string while it has consecutive equal digits (while the same digit repeats):

Replace all ranges of consecutive equal digits with their sum in the string. For example, the number 999433 should become 2746, because 9 + 9 + 9 = 27 and 3 + 3 = 6, and 44488366664 should become 12163244 after this operation, following the same logic.

This operation should be repeated on the previous result until there are no consecutive equal digits.

Return the resulting string.

Note: You are not expected to provide the most optimal solution, but a solution with time complexity not worse than O(number.length) will fit within the execution time limit.

#### Example

- For number = "666644319333", the output should be solution(number) = "26328".

  Explanation:
  - There are three ranges of consecutive equal digits: [6666][44]319[333]. Each such range should be replaced by the sum of digits it consists of: [24][8]319[9], so the result of the operation is 2483199.
  - The number still has consecutive equal digits [99], so the operation will be applied once more, after which the number becomes 2483118.
  - Lastly, [11]83[118] will become 26328, and the process will stop on this string.
  - After all, the output should be "26328".

- For number = "0044886", the output should be solution(number) = "084".

  Explanation:
  - After one operation, number = "08166". Then it sequentially becomes 08112, 0822, and 084, so the final result is "084".

- For number = "429201", the output should be solution(number) = "429201".

  Explanation:
  - There are no consecutive equal numbers, so the result is the same as the input.
"""

class Solution:
    """
    The Solution class contains methods to process a given number string by replacing ranges of consecutive
    equal digits with their sum. The general approach is to iterate through the string, identify ranges
    of consecutive equal digits, compute their sums, and replace those ranges with the sums. This process
    repeats until there are no more consecutive equal digits in the string.
    """

    def processNumber(self, number):
        """
        Repeatedly replaces ranges of consecutive equal digits with their sums until no consecutive
        equal digits remain.

        Args:
            number (str): The input string consisting of digits.

        Returns:
            str: The resulting string after all replacements.

        Thought Process:
        - Use a loop that continues until there are no consecutive equal digits.
        - In each iteration:
            - Traverse the string and identify ranges of consecutive equal digits.
            - For each range, calculate the sum of its digits.
            - Replace the range in the string with the sum.
        - Repeat the process with the new string.

        Time Complexity: O(n), where n is the length of the number string, for each iteration.
        Space Complexity: O(n), for storing the new string in each iteration.
        """
        import re

        # Regular expression pattern to find consecutive equal digits
        pattern = re.compile(r'(\d)\1+')

        while True:
            new_number = ''
            i = 0
            changed = False

            while i < len(number):
                j = i
                # Find the end of the current sequence of identical digits
                while j + 1 < len(number) and number[j + 1] == number[i]:
                    j += 1

                if j > i:
                    # Found a sequence of consecutive equal digits
                    seq = number[i:j + 1]
                    sum_of_digits = sum(int(d) for d in seq)
                    new_number += str(sum_of_digits)
                    changed = True
                    i = j + 1
                else:
                    # Single digit, copy as is
                    new_number += number[i]
                    i += 1

            if not changed:
                # No changes in this iteration, break the loop
                break

            number = new_number

        return number

# Sample usage
solution = Solution()

# Sample Input 1
number1 = "666644319333"
result1 = solution.processNumber(number1)
print(f"Resulting string: {result1}")  # Expected Output: "26328"

# Sample Input 2
number2 = "0044886"
result2 = solution.processNumber(number2)
print(f"Resulting string: {result2}")  # Expected Output: "084"

# Sample Input 3
number3 = "429201"
result3 = solution.processNumber(number3)
print(f"Resulting string: {result3}")  # Expected Output: "429201"
