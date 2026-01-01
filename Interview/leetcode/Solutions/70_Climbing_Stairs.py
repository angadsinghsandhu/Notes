# File: Leetcode/Solutions/70_Climbing_Stairs.py

"""
Problem Number: 70
Problem Name: Climbing Stairs
Difficulty: Easy
Tags: Math, Dynamic Programming, Memoization, NeetCode 150
Company (Frequency): Amazon, Google, Microsoft, Facebook, Apple
Leetcode Link: https://leetcode.com/problems/climbing-stairs/description/

DESCRIPTION

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

---

#### Example 1:

Input:
n = 2

Output:
2

Explanation:
There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

---

#### Example 2:

Input:
n = 3

Output:
3

Explanation:
There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

---

#### Constraints:

- 1 <= n <= 45
"""

from typing import List, Dict

class Solution:
    """
    Thought Process:
    - This problem is a classic application of the Fibonacci sequence. To reach the nth step, you must have come from either the (n-1)th step or the (n-2)th step.
    - Thus, the total ways to reach step n is: ways(n) = ways(n-1) + ways(n-2).
    - We will explore five different approaches:
        1. Recursive (Brute Force): Simple but highly inefficient due to redundant calculations.
        2. Memoization (Top-Down): Optimizes recursion by storing previously computed results.
        3. Tabulation (Bottom-Up): Iteratively builds up the solution using an array.
        4. Space Optimized: Further reduces space by only storing the last two states.
        5. Matrix Exponentiation: The most mathematically advanced way to solve linear recurrences in logarithmic time.

    Input:
        n: int - The number of steps.

    Output:
        int - The number of distinct ways to reach the top.
    """

    def climb_stairs_recursive(self, n: int) -> int:
        """
        Approach: Pure Recursion (Brute Force)
        - This approach explores every possible combination of 1 and 2 steps.
        - The recurrence relation is f(n) = f(n-1) + f(n-2).
        - It results in a massive recursion tree where many subproblems are solved multiple times.

        T.C.: O(2^n)
        S.C.: O(n) - Maximum depth of the recursion stack.
        """
        if n <= 2:
            return n
        return self.climb_stairs_recursive(n - 1) + self.climb_stairs_recursive(n - 2)

    def climb_stairs_memoization(self, n: int) -> int:
        """
        Approach: Top-Down DP (Memoization)
        - We use a dictionary or array to store the result of each 'n' we calculate.
        - Before performing recursion, we check if the result is already in the 'memo'.

        T.C.: O(n)
        S.C.: O(n) - For the memo storage and recursion stack.
        """
        memo = {}

        def solve(step):
            if step <= 2:
                return step
            if step in memo:
                return memo[step]
            memo[step] = solve(step - 1) + solve(step - 2)
            return memo[step]

        return solve(n)

    def climb_stairs_tabulation(self, n: int) -> int:
        """
        Approach: Bottom-Up DP (Tabulation)
        - We build a table 'dp' from the base cases (1 and 2) up to n.
        - This avoids the overhead of recursion.

        T.C.: O(n)
        S.C.: O(n) - To store the dp array.
        """
        if n <= 2:
            return n
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]

    def climb_stairs_space_optimized(self, n: int) -> int:
        """
        Approach: Space Optimized DP
        - Since we only need the two previous values to calculate the current value, we don't need a full array.
        - We use two variables to track the previous two steps.

        T.C.: O(n)
        S.C.: O(1)
        """
        if n <= 2:
            return n
        first = 1
        second = 2
        for i in range(3, n + 1):
            third = first + second
            first = second
            second = third
        return second

    def climb_stairs_matrix_exponentiation(self, n: int) -> int:
        """
        Approach: Matrix Exponentiation
        - The Fibonacci recurrence can be represented in matrix form:
          [[1, 1], [1, 0]] ^ n-1 * [[f(1)], [f(0)]]
        - By using binary exponentiation (power function), we can calculate the matrix power in O(log n).

        T.C.: O(log n)
        S.C.: O(1)
        """
        if n <= 2:
            return n

        def multiply(A, B):
            C = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        C[i][j] += A[i][k] * B[k][j]
            return C

        def power(A, p):
            res = [[1, 0], [0, 1]]
            while p > 0:
                if p % 2 == 1:
                    res = multiply(res, A)
                A = multiply(A, A)
                p //= 2
            return res

        T = [[1, 1], [1, 0]]
        # We want the n-th Fibonacci number. 
        # For n steps, the sequence is 1, 2, 3, 5, 8...
        # This matches Fibonacci(n+1) where Fib(1)=1, Fib(2)=1, Fib(3)=2.
        T_n = power(T, n)
        return T_n[0][0]

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_n = 5
    print("Results for n =", test_n)
    
    # 
    
    print("Recursive (Brute Force):", solution.climb_stairs_recursive(test_n))
    print("Memoization (Top-Down): ", solution.climb_stairs_memoization(test_n))
    print("Tabulation (Bottom-Up): ", solution.climb_stairs_tabulation(test_n))
    print("Space Optimized:        ", solution.climb_stairs_space_optimized(test_n))
    print("Matrix Exponentiation:  ", solution.climb_stairs_matrix_exponentiation(test_n))
    
    # Large case to demonstrate efficiency
    large_n = 35
    print("\nLarge Case (n =", large_n, ")")
    print("Matrix Exponentiation (Fastest):", solution.climb_stairs_matrix_exponentiation(large_n))
