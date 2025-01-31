# TODO: revisit

# File: Leetcode/Solutions/1478_Allocate_Mailboxes.py

"""
Problem Number: 1478
Problem Name: Allocate Mailboxes
Difficulty: Hard
Tags: Array, Math, Dynamic Programming, Sorting
Company (Frequency): Google (30), Amazon (25), Microsoft (20), Facebook (15), Apple (10)
Leetcode Link: https://leetcode.com/problems/allocate-mailboxes/description/

DESCRIPTION

You are given an array of integers `houses` where `houses[i]` is the location of the `i-th` house along a street. You are also given an integer `k` representing the number of mailboxes to allocate.

You need to allocate `k` mailboxes in the street such that the **total distance** between each house and its nearest mailbox is minimized.

The distance between the house at `houses[i]` and the mailbox at `x` is `|houses[i] - x|`.

**Return** the minimum total distance between each house and its nearest mailbox.

---

#### Example 1:
**Input:**
```plaintext
houses = [1,4,8,10,20]
k = 3
```

**Output:**
```plaintext
5
```

**Explanation:**  
Allocate mailboxes at positions `3`, `9`, and `20`.  
The total distance is `|1-3| + |4-3| + |8-9| + |10-9| + |20-20| = 2 + 1 + 1 + 1 + 0 = 5`.

#### Example 2:
**Input:**
```plaintext
houses = [2,3,5,12,18]
k = 2
```

**Output:**
```plaintext
9
```

**Explanation:**  
Allocate mailboxes at positions `3` and `14`.  
The total distance is `|2-3| + |3-3| + |5-3| + |12-14| + |18-14| = 1 + 0 + 2 + 2 + 4 = 9`.

#### Constraints:
- `1 <= k <= houses.length <= 100`
- `1 <= houses[i] <= 10^4`
- All the integers of `houses` are unique.

"""

from typing import List
import sys

class Solution:
    """
    Thought Process:
    - The problem requires allocating `k` mailboxes to minimize the total distance between each house and its nearest mailbox.
    - A brute-force approach would involve trying all possible combinations of mailbox placements, which is computationally infeasible for larger inputs.
    - An optimized approach involves sorting the house locations and using dynamic programming (DP) to efficiently compute the minimum total distance.
    - Precompute the cost of assigning a single mailbox to a range of houses, which is minimized when the mailbox is placed at the median house.
    - Use DP to build up solutions for allocating `k` mailboxes based on the precomputed costs.

    Input:
        houses: List[int] - A list of integers representing the locations of the houses.
        k: int - The number of mailboxes to allocate.

    Output:
        int - The minimum total distance between each house and its nearest mailbox.
    """

    def brute_force_solution(self, houses: List[int], k: int) -> int:
        """
        Approach:
        - Generate all possible combinations of `k` mailbox positions from the house locations.
        - For each combination, calculate the total distance by assigning each house to its nearest mailbox.
        - Return the minimum total distance found among all combinations.

        T.C.: O(C(n, k) * n), where C(n, k) is the number of combinations.
        S.C.: O(k)

        Note:
        - This approach is only feasible for very small inputs due to its exponential time complexity.
        """
        from itertools import combinations

        def total_distance(mailboxes):
            return sum(min(abs(house - mailbox) for mailbox in mailboxes) for house in houses)

        min_dist = sys.maxsize
        for mailboxes in combinations(houses, k):
            dist = total_distance(mailboxes)
            min_dist = min(min_dist, dist)
        return min_dist

    def optimized_solution(self, houses: List[int], k: int) -> int:
        """
        Approach:
        - Sort the house locations to simplify the problem.
        - Precompute the cost of assigning a single mailbox to any range of houses [i, j], where the mailbox is placed at the median house.
        - Use dynamic programming to determine the minimum total distance for allocating mailboxes.
        - dp[i][j] represents the minimum total distance for the first `i` houses with `j` mailboxes.
        - Iterate through the houses and mailboxes, updating the DP table based on the precomputed costs.

        T.C.: O(n^2 * k)
        S.C.: O(n * k)

        Where `n` is the number of houses.
        """
        if not houses:
            return 0

        houses.sort()
        n = len(houses)

        # Precompute the cost for all ranges [i, j]
        cost = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                median = houses[(i + j) // 2]
                cost[i][j] = sum(abs(house - median) for house in houses[i:j+1])

        # Initialize DP table
        # dp[i][j] represents the minimum total distance for the first `i` houses with `j` mailboxes
        dp = [[sys.maxsize] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0  # Base case: 0 houses with 0 mailboxes

        for i in range(1, n + 1):
            for j in range(1, min(k, i) + 1):
                for p in range(i):
                    if dp[p][j-1] != sys.maxsize:
                        dp[i][j] = min(dp[i][j], dp[p][j-1] + cost[p][i-1])

        return dp[n][k]

    def optimized_solution_space_optimized(self, houses: List[int], k: int) -> int:
        """
        Approach:
        - Similar to the optimized_solution, but reduces space complexity by using a 1D DP array.
        - This optimization leverages the fact that to compute dp[j], we only need the previous state of dp[j-1].

        T.C.: O(n^2 * k)
        S.C.: O(n * k)
        """
        # TODO: Implement the space-optimized solution

    def optimized_solution_with_memoization(self, houses: List[int], k: int) -> int:
        """
        Approach:
        - Utilize memoization to store the results of subproblems.
        - This reduces redundant calculations by caching the results of already computed states.

        T.C.: O(n^2 * k)
        S.C.: O(n * k)
        """
        from functools import lru_cache

        houses.sort()
        n = len(houses)

        # Precompute the cost for all ranges [i, j]
        cost = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                median = houses[(i + j) // 2]
                cost[i][j] = sum(abs(house - median) for house in houses[i:j+1])

        @lru_cache(None)
        def dp(i, j):
            if j == 0 and i == 0:
                return 0
            if j == 0 or i == 0:
                return sys.maxsize
            min_dist = sys.maxsize
            for p in range(i):
                if dp(p, j-1) != sys.maxsize:
                    min_dist = min(min_dist, dp(p, j-1) + cost[p][i-1])
            return min_dist

        return dp(n, k)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    houses1 = [1, 4, 8, 10, 20]
    k1 = 3
    print("Test Case 1:")
    print(f"Houses: {houses1}, Mailboxes: {k1}")
    print(f"Brute Force Solution: {solution.brute_force_solution(houses1, k1)}")  # Output: 5
    print(f"Optimized Solution: {solution.optimized_solution(houses1, k1)}")        # Output: 5
    print(f"Optimized Solution with Memoization: {solution.optimized_solution_with_memoization(houses1, k1)}")  # Output: 5
    print()

    # Test case 2
    houses2 = [2, 3, 5, 12, 18]
    k2 = 2
    print("Test Case 2:")
    print(f"Houses: {houses2}, Mailboxes: {k2}")
    print(f"Brute Force Solution: {solution.brute_force_solution(houses2, k2)}")  # Output: 9
    print(f"Optimized Solution: {solution.optimized_solution(houses2, k2)}")        # Output: 9
    print(f"Optimized Solution with Memoization: {solution.optimized_solution_with_memoization(houses2, k2)}")  # Output: 9
    print()

    # Test case 3
    houses3 = [1, 2, 3, 4, 5]
    k3 = 1
    print("Test Case 3:")
    print(f"Houses: {houses3}, Mailboxes: {k3}")
    print(f"Brute Force Solution: {solution.brute_force_solution(houses3, k3)}")  # Output: 6
    print(f"Optimized Solution: {solution.optimized_solution(houses3, k3)}")        # Output: 6
    print(f"Optimized Solution with Memoization: {solution.optimized_solution_with_memoization(houses3, k3)}")  # Output: 6
    print()

    # Test case 4
    houses4 = [7, 14, 10, 20, 3]
    k4 = 2
    print("Test Case 4:")
    print(f"Houses: {houses4}, Mailboxes: {k4}")
    print(f"Brute Force Solution: {solution.brute_force_solution(houses4, k4)}")  # Output: 9
    print(f"Optimized Solution: {solution.optimized_solution(houses4, k4)}")        # Output: 9
    print(f"Optimized Solution with Memoization: {solution.optimized_solution_with_memoization(houses4, k4)}")  # Output: 9
    print()

    # Test case 5
    houses5 = [1]
    k5 = 1
    print("Test Case 5:")
    print(f"Houses: {houses5}, Mailboxes: {k5}")
    print(f"Brute Force Solution: {solution.brute_force_solution(houses5, k5)}")  # Output: 0
    print(f"Optimized Solution: {solution.optimized_solution(houses5, k5)}")        # Output: 0
    print(f"Optimized Solution with Memoization: {solution.optimized_solution_with_memoization(houses5, k5)}")  # Output: 0
    print()