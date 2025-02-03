# TODO: revisit

# File: Leetcode/Solutions/XXX_Wine_Selling_Problem.py

"""
Problem Number: XXX
Problem Name: Wine Selling Problem
Difficulty: Medium
Tags: Dynamic Programming, Recursion
Company (Frequency): Various (Not specified)
Leetcode Link: N/A
Similar to: https://leetcode.com/problems/maximize-the-profit-as-the-salesman/description/

DESCRIPTION

Given `n` wines in a row, with integers denoting the cost of each wine respectively. Each year you can sell the first or the last wine in the row. Let the initial profits from the wines be P1, P2, P3…Pn. In the Yth year, the profit from the ith wine will be Y * P[i]. The goal is to calculate the maximum profit that can be earned by selling all the wines.

---

#### Example 1:
**Input:**
```plaintext
wines = [2, 4, 6, 2, 5]
```

**Output:**
```plaintext
64
```

**Explanation:**  
The maximum profit can be achieved by selling the wines in the following order:
- Year 1: Sell wine at index 0 (price = 2 * 1 = 2)
- Year 2: Sell wine at index 4 (price = 5 * 2 = 10)
- Year 3: Sell wine at index 3 (price = 2 * 3 = 6)
- Year 4: Sell wine at index 1 (price = 4 * 4 = 16)
- Year 5: Sell wine at index 2 (price = 6 * 5 = 30)
Total profit = 2 + 10 + 6 + 16 + 30 = 64

#### Constraints:
- `1 <= n <= 1000`
- `1 <= P[i] <= 1000`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves maximizing profit by selling wines from either end over multiple years.
    - A brute-force approach involves checking all possible sequences of selling wines, but this is inefficient.
    - An optimized approach uses dynamic programming to store intermediate results and avoid redundant calculations.

    Input:
        wines: List[int] - A list of wine prices.

    Output:
        int - The maximum profit achievable.
    """

    def brute_force_solution(self, wines: List[int]) -> int:
        """
        Approach:
        - Recursively check all possible sequences of selling wines from either end.
        - Calculate the profit for each sequence and track the maximum profit.

        T.C.: O(2^n) - Exponential time complexity due to recursive branching.
        S.C.: O(n) - Recursive stack space.
        """
        def dfs(start: int, end: int, year: int) -> int:
            if start > end:
                return 0
            # Sell the first wine
            left_profit = wines[start] * year + dfs(start + 1, end, year + 1)
            # Sell the last wine
            right_profit = wines[end] * year + dfs(start, end - 1, year + 1)
            return max(left_profit, right_profit)

        return dfs(0, len(wines) - 1, 1)

    def optimized_solution(self, wines: List[int]) -> int:
        """
        Approach:
        - Use dynamic programming to store the maximum profit for selling wines from index `i` to `j`.
        - Avoid redundant calculations by reusing previously computed results.

        T.C.: O(n^2) - Quadratic time complexity due to filling the DP table.
        S.C.: O(n^2) - Space for the DP table.
        """
        n = len(wines)
        dp = [[0] * n for _ in range(n)]  # DP table to store maximum profit
        # dp[i][j] = maximum profit from selling wines from index i to j

        # Fill the DP table for subarrays of increasing lengths
        for length in range(1, n + 1):
            for start in range(n - length + 1):
                end = start + length - 1
                year = n - (end - start)  # Calculate the current year
                if start == end:
                    dp[start][end] = wines[start] * year
                else:
                    # Sell the first wine
                    left_profit = wines[start] * year + dp[start + 1][end]
                    # Sell the last wine
                    right_profit = wines[end] * year + dp[start][end - 1]
                    dp[start][end] = max(left_profit, right_profit)

        return dp[0][n - 1]
    
    def greedy_2pointer_solution(self, wines: List[int]) -> int:
        """
        Approach:
        - Use two pointers to simulate selling wines from either end.
        - Calculate the profit for each wine and track the maximum profit.

        T.C.: O(n) - Linear time complexity due to traversing the wines.
        S.C.: O(1) - Constant space complexity.
        """
        n = len(wines)
        left, right = 0, n - 1

        max_profit = 0
        year = 1

        while left <= right:
            if wines[left] < wines[right]:
                max_profit += wines[left] * year
                left += 1
            else:
                max_profit += wines[right] * year
                right -= 1
            year += 1

        return max_profit

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    wines1 = [2, 4, 6, 2, 5]
    print(solution.brute_force_solution(wines1))  # Output: 64
    print(solution.optimized_solution(wines1))    # Output: 64
    print(solution.optimized_2pointer_solution(wines1))  # Output: 64

    # Test case 2
    wines2 = [1, 2, 3, 4, 5]
    print(solution.brute_force_solution(wines2))  # Output: 50
    print(solution.optimized_solution(wines2))    # Output: 50
    print(solution.optimized_2pointer_solution(wines2))  # Output: 50
