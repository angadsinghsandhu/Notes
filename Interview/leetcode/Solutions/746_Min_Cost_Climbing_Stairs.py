# File: Leetcode/Solutions/746_Min_Cost_Climbing_Stairs.py

"""
Problem Number: 746
Problem Name: Min Cost Climbing Stairs
Difficulty: Easy
Tags: Array, Dynamic Programming, Memoization, Neetcode 150
Company (Frequency): Amazon, Google, Microsoft, Adobe
Leetcode Link: https://leetcode.com/problems/min-cost-climbing-stairs/description/

DESCRIPTION

You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.
You can either start from the step with index 0, or the step with index 1.
Return the minimum cost to reach the top of the floor.

---

#### Example 1:

Input:
cost = [10,15,20]

Output:
15

Explanation:
You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.

---

#### Example 2:

Input:
cost = [1,100,1,1,1,100,1,1,100,1]

Output:
6

Explanation:
You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.

---

#### Constraints:

- 2 <= cost.length <= 1000
- 0 <= cost[i] <= 999
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The goal is to reach the top floor, which is effectively index n (one step beyond the last element of the cost array).
    - To reach any step i, you could have come from step i-1 or step i-2.
    - Since we want the minimum cost, the recurrence relation is:
      min_cost(i) = min(min_cost(i-1) + cost[i-1], min_cost(i-2) + cost[i-2])
    - We start at index 0 or index 1, meaning the cost to reach those initial starting points is 0.

    Input:
        cost: List[int] - The cost of each step.

    Output:
        int - The minimum cost to reach the top.
    """

    def min_cost_recursive(self, cost: List[int]) -> int:
        """
        Approach: Pure Recursion (Brute Force)
        - We define a recursive function that calculates the cost to reach the top from current step i.
        - Because it explores all branches without saving results, it is highly inefficient.

        T.C.: O(2^n)
        S.C.: O(n) - Recursion stack depth.
        """
        n = len(cost)

        def solve(i):
            if i >= n:
                return 0
            return cost[i] + min(solve(i + 1), solve(i + 2))

        return min(solve(0), solve(1))

    def min_cost_memoization(self, cost: List[int]) -> int:
        """
        Approach: Top-Down DP (Memoization)
        - Uses a dictionary to store results of subproblems (min cost from step i).
        - If we encounter the same step again, we return the cached value.

        T.C.: O(n)
        S.C.: O(n) - Memoization table and stack.
        """
        n = len(cost)
        memo = {}

        def solve(i):
            if i >= n:
                return 0
            if i in memo:
                return memo[i]
            
            memo[i] = cost[i] + min(solve(i + 1), solve(i + 2))
            return memo[i]

        return min(solve(0), solve(1))

    def min_cost_tabulation(self, cost: List[int]) -> int:
        """
        Approach: Bottom-Up DP (Tabulation Array)
        - We build a DP table where dp[i] is the minimum cost to reach step i.
        - We initialize dp[0] and dp[1] as 0 because we can start there for free.

        T.C.: O(n)
        S.C.: O(n)
        """
        n = len(cost)
        dp = [0] * (n + 1)
        
        # Iterating from the 2nd index to the top floor (n)
        for i in range(2, n + 1):
            take_one_step = dp[i-1] + cost[i-1]
            take_two_steps = dp[i-2] + cost[i-2]
            dp[i] = min(take_one_step, take_two_steps)
            
        return dp[n]

    def min_cost_optimized(self, cost: List[int]) -> int:
        """
        Approach: Space Optimized Bottom-Up DP
        - Since we only need the last two values (dp[i-1] and dp[i-2]), we can use two variables.
        - This reduces space complexity from linear to constant.

        T.C.: O(n)
        S.C.: O(1)
        """
        n = len(cost)
        prev2 = 0 # Cost to reach two steps back
        prev1 = 0 # Cost to reach one step back
        
        for i in range(2, n + 1):
            current = min(prev1 + cost[i-1], prev2 + cost[i-2])
            prev2 = prev1
            prev1 = current
            
        return prev1

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    cost1 = [10, 15, 20]
    print(f"Test Case 1: cost = {cost1}")
    print(f"Recursive Result:  {solution.min_cost_recursive(cost1)}")
    print(f"Tabulation Result: {solution.min_cost_tabulation(cost1)}")
    print(f"Optimized Result:  {solution.min_cost_optimized(cost1)}")
    print("-" * 30)

    # Test Case 2
    cost2 = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    print(f"Test Case 2: cost = {cost2}")
    print(f"Memoization Result: {solution.min_cost_memoization(cost2)}")
    print(f"Tabulation Result:  {solution.min_cost_tabulation(cost2)}")
    print(f"Optimized Result:   {solution.min_cost_optimized(cost2)}")
    print("-" * 30)

    # Test Case 3
    cost3 = [5, 10, 15, 20]
    print(f"Test Case 3: cost = {cost3}")
    print(f"Optimized Result:   {solution.min_cost_optimized(cost3)}")
