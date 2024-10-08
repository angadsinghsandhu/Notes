# EXPRESSION ADD OPERATORS

# Problem number: 282
# Difficulty: Hard
# Tags: Backtracking, String, Recursion
# Link: https://leetcode.com/problems/expression-add-operators/

from typing import List

class Solution:
    """
    This problem requires inserting the binary operators '+', '-', and/or '*' between the digits 
    of a given string so that the resultant expression evaluates to the target value.

    We will solve this using a backtracking approach that explores all possibilities of inserting operators.
    During the recursive exploration, we will evaluate the expression dynamically, respecting the order 
    of operations (handling multiplication carefully) to avoid recalculating previous sub-expressions.
    """

    def addOperators(self, num: str, target: int) -> List[str]:
        """
        Backtracking approach to explore all possible operator insertions.
        
        T.C. : O(4^n) where n is the length of the input string (due to the branching factor at each recursion step)
        S.C. : O(n) for the recursion depth and the size of the path being constructed
        """
        def backtrack(index: int, prev_operand: int, current_value: int, path: str):
            if index == len(num):
                # Base case: if we've reached the end of the string and the expression evaluates to target
                if current_value == target:
                    result.append(path)
                return

            for i in range(index, len(num)):
                # If the number starts with a '0', we should skip any multi-digit numbers to avoid leading zeros
                if i > index and num[index] == '0':
                    break
                
                # Convert the current substring into an integer
                current_num = int(num[index:i+1])

                if index == 0:
                    # First number, just take it and move forward
                    backtrack(i + 1, current_num, current_num, path + str(current_num))
                else:
                    # Explore the '+' operator
                    backtrack(i + 1, current_num, current_value + current_num, path + '+' + str(current_num))
                    # Explore the '-' operator
                    backtrack(i + 1, -current_num, current_value - current_num, path + '-' + str(current_num))
                    # Explore the '*' operator (carefully maintaining the previous operand for correct evaluation)
                    backtrack(i + 1, prev_operand * current_num, current_value - prev_operand + (prev_operand * current_num), path + '*' + str(current_num))

        result = []
        if not num:
            return result
        backtrack(0, 0, 0, "")
        return result

# Best Method: The backtracking approach is optimal as it explores all possibilities efficiently using recursion.

# Sample Inputs for Testing
num1, target1 = "123", 6
num2, target2 = "232", 8
num3, target3 = "3456237490", 9191

# Testing the solution
print(Solution().addOperators(num1, target1))  # Output: ["1*2*3", "1+2+3"]
print(Solution().addOperators(num2, target2))  # Output: ["2*3+2", "2+3*2"]
print(Solution().addOperators(num3, target3))  # Output: []
