# EXCLUSIVE TIME OF FUNCTIONS

# Problem number: 636
# Difficulty: Medium
# Tags: Stack, Simulation
# Link: https://leetcode.com/problems/exclusive-time-of-functions/

from typing import List

class Solution:
    """
    The problem requires calculating the exclusive execution time for each function 
    in a program that runs on a single-threaded CPU. Each function has unique start 
    and end logs that indicate when the function starts and ends. We must calculate 
    the total time each function spends executing, excluding time when other functions 
    are called in between (recursive calls or otherwise).
    
    We will implement the solution using a stack to track the current function's 
    start time and handle nested or sequential function calls.

    T.C. : O(m) where m is the number of logs (length of logs)
    S.C. : O(m) for the stack used to track function calls
    """

    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        """
        Stack-based approach to track the start and end of function calls and calculate
        the exclusive time for each function.
        
        T.C. : O(m) where m is the number of logs
        S.C. : O(m) for stack usage
        """
        result = [0] * n  # To store the exclusive time of each function
        stack = []  # To track function calls
        prev_time = 0  # To track the previous timestamp

        for log in logs:
            # Parse the log
            func_id, event, time = log.split(':')
            func_id, time = int(func_id), int(time)

            if event == "start":
                # If the stack is not empty, update the time for the function at the top of the stack
                if stack:
                    result[stack[-1]] += time - prev_time
                # Push the current function onto the stack
                stack.append(func_id)
                # Update the previous timestamp
                prev_time = time
            else:
                # End event: function completes, pop it from the stack
                result[stack.pop()] += time - prev_time + 1
                # Update the previous timestamp to time + 1 for the next potential function
                prev_time = time + 1

        return result

# Best Method: The stack approach is optimal for this type of problem due to the need 
# to manage nested function calls and compute their exclusive time efficiently.

# Sample Inputs for Testing
n = 2
logs = ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]

# Testing the method
solution = Solution()
output = solution.exclusiveTime(n, logs)

# Expected output: [3, 4]
print(output)
