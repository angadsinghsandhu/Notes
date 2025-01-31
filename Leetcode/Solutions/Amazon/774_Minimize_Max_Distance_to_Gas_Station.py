# TODO: revisit

# File: Leetcode/Solutions/774_Minimize_Max_Distance_to_Gas_Station.py

"""
Problem Number: 774
Problem Name: Minimize Max Distance to Gas Station
Difficulty: Hard
Tags: Array, Binary Search
Company (Frequency): Google (40), Amazon (35), Facebook (25), Apple (15), Microsoft (10)
Leetcode Link: https://leetcode.com/problems/minimize-max-distance-to-gas-station/description/

DESCRIPTION

On a horizontal number line, there are gas stations at positions `stations[0], stations[1], ..., stations[N-1]`, where `N = stations.length`.

Now, you are allowed to add `K` more gas stations anywhere on the number line.

Your goal is to minimize the maximum distance `D` between any two adjacent gas stations after adding the `K` new stations.

Return the smallest possible value of `D`. Answers within `10^-6` of the actual answer will be accepted as correct.

---

#### Example 1:
**Input:**
```plaintext
stations = [1,2,3,4,5,6,7,8,9,10], K = 9
```

**Output:**
```plaintext
0.500000
```

**Explanation:**  
Add one gas station between each pair of existing stations to achieve a maximum distance of `0.5`.

#### Example 2:
**Input:**
```plaintext
stations = [1,2,3,4,5,6,7,8,9,10], K = 1
```

**Output:**
```plaintext
1.000000
```

**Explanation:**  
No need to add any gas station as the maximum distance is already `1`.

#### Example 3:
**Input:**
```plaintext
stations = [1,2,3,4,5,6,7,8,9,10], K = 0
```

**Output:**
```plaintext
1.000000
```

**Explanation:**  
No new gas stations are added, so the maximum distance remains `1`.

#### Constraints:
- `stations.length` will be an integer in the range `[10, 2000]`.
- `stations[i]` will be an integer in the range `[0, 10^8]`.
- `K` will be an integer in the range `[1, 10^6]`.
- All `stations[i]` are unique and sorted in increasing order.

"""

from typing import List
import sys

class Solution:
    """
    Thought Process:
    - The problem requires adding `K` new gas stations to minimize the maximum distance between any two adjacent gas stations.
    - A brute-force approach would involve trying all possible placements of `K` gas stations, which is computationally infeasible due to the large constraints.
    - An optimized approach involves using binary search to find the smallest possible maximum distance `D` such that all gas stations can be placed within `D` distance apart using at most `K` additional stations.
    - The key idea is to perform a binary search on the range of possible distances and use a helper function to check the feasibility of each distance.

    Input:
        stations: List[int] - A list of integers representing the positions of existing gas stations on the number line.
        K: int - The number of additional gas stations that can be added.

    Output:
        float - The smallest possible maximum distance between adjacent gas stations after adding the `K` new stations.
    """

    def minmaxGasDist_brute_force(self, stations: List[int], K: int) -> float:
        """
        Approach:
        - This brute-force approach attempts to place `K` new gas stations optimally to minimize the maximum distance `D`.
        - Due to the problem's constraints, this approach is not feasible for large inputs but serves as a conceptual understanding.

        Steps:
        1. Identify all possible gaps between existing gas stations.
        2. For each gap, consider placing gas stations at positions that divide the gap as evenly as possible.
        3. Calculate the maximum distance after placing the gas stations.
        4. Return the smallest such maximum distance found.

        T.C.: Exponential, O((n + K)^n) - Not feasible for large inputs.
        S.C.: O(1) - Constant space.

        Note:
        - This method is purely illustrative and not recommended for actual problem-solving due to inefficiency.
        """
        # This method is not implemented due to infeasibility.
        pass

    def minmaxGasDist_binary_search(self, stations: List[int], K: int) -> float:
        """
        Approach:
        - Utilize binary search to find the minimal possible maximum distance `D`.
        - Define the search range between 0 and the maximum possible gap between stations.
        - Use a helper function to determine if a given `D` is feasible by calculating the number of additional stations needed.

        Steps:
        1. Initialize `left` to 0 and `right` to the maximum gap between consecutive stations.
        2. While the difference between `right` and `left` is greater than the precision `1e-6`:
            a. Calculate `mid` as the average of `left` and `right`.
            b. Use the helper function to check if it's possible to achieve `D = mid` with at most `K` additional stations.
            c. If feasible, set `right` to `mid`; otherwise, set `left` to `mid`.
        3. Return `left` as the minimal possible maximum distance.

        T.C.: O(N * log((max_gap)/precision)), where `N` is the number of stations.
        S.C.: O(1) - Constant space.

        Where:
        - `max_gap` is the initial maximum distance between any two consecutive stations.
        - `precision` is `1e-6`.
        """
        def is_possible(D: float) -> bool:
            """
            Helper Function:
            - Determines if it's possible to ensure that no two adjacent gas stations are more than distance `D` apart by adding at most `K` gas stations.

            Parameters:
                D (float): The maximum allowed distance between any two adjacent gas stations.

            Returns:
                bool: True if feasible, False otherwise.
            """
            required = 0
            for i in range(1, len(stations)):
                gap = stations[i] - stations[i - 1]
                # Number of additional stations needed in this gap
                # Subtract 1 to handle exact multiples
                required += gap // D
            return required <= K

        # Initialize binary search boundaries
        left, right = 0.0, max(stations[i] - stations[i - 1] for i in range(1, len(stations)))

        # Perform binary search with precision up to 1e-6
        while right - left > 1e-6:
            mid = (left + right) / 2
            if is_possible(mid):
                right = mid
            else:
                left = mid

        return left

    def minmaxGasDist_math_approach(self, stations: List[int], K: int) -> float:
        """
        Approach:
        - This method is essentially the same as the binary search approach but emphasizes the mathematical reasoning behind determining the number of required stations.

        Steps:
        1. Sort the `stations` array to ensure proper gap calculations.
        2. Initialize `left` and `right` for binary search.
        3. Iterate using binary search to find the minimal `D`.
        4. In each iteration, calculate the number of required stations for the current `mid`.
        5. Adjust `left` and `right` based on feasibility.

        T.C.: O(N * log((max_gap)/precision))
        S.C.: O(1) - Constant space.
        """
        return self.minmaxGasDist_binary_search(stations, K)

    def minmaxGasDist_optimized(self, stations: List[int], K: int) -> float:
        """
        Approach:
        - This is a synonym for the binary search approach but can include minor optimizations such as precomputing all gaps.

        Steps:
        1. Precompute all gaps between consecutive stations.
        2. Use binary search to find the minimal `D`.
        3. In each binary search iteration, iterate through precomputed gaps to determine required stations.

        T.C.: O(N * log((max_gap)/precision))
        S.C.: O(1) - Constant space.
        """
        gaps = [stations[i] - stations[i - 1] for i in range(1, len(stations))]
        def is_possible_optimized(D: float) -> bool:
            required = 0
            for gap in gaps:
                required += int(gap / D)
            return required <= K

        left, right = 0.0, max(gaps)

        while right - left > 1e-6:
            mid = (left + right) / 2
            if is_possible_optimized(mid):
                right = mid
            else:
                left = mid
        return left

    def minmaxGasDist_final(self, stations: List[int], K: int) -> float:
        """
        Final Optimized Solution:
        - Combines the binary search approach with precomputed gaps for efficiency.

        Steps:
        1. Precompute the gaps between consecutive stations.
        2. Initialize `left` and `right` for binary search.
        3. Perform binary search to find the minimal possible `D`.
        4. In each iteration, determine if the current `D` is feasible by summing the required stations.
        5. Adjust the search boundaries based on feasibility.

        T.C.: O(N * log((max_gap)/precision))
        S.C.: O(1) - Constant space.
        """
        gaps = [stations[i] - stations[i - 1] for i in range(1, len(stations))]
        left, right = 0.0, max(gaps)

        while right - left > 1e-6:
            mid = (left + right) / 2.0
            required = 0
            for gap in gaps:
                required += int(gap / mid)
            if required <= K:   # Feasible
                right = mid
            else:               # Not feasible
                left = mid
        return left

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    stations1 = [1,2,3,4,5,6,7,8,9,10]
    K1 = 9
    print("Test Case 1:")
    print(f"Stations: {stations1}, K: {K1}")
    print(f"Binary Search Solution: {solution.minmaxGasDist_binary_search(stations1, K1):.6f}")  # Output: 0.500000
    print(f"Math Approach Solution: {solution.minmaxGasDist_math_approach(stations1, K1):.6f}")    # Output: 0.500000
    print(f"Optimized Solution: {solution.minmaxGasDist_optimized(stations1, K1):.6f}")          # Output: 0.500000
    print(f"Final Optimized Solution: {solution.minmaxGasDist_final(stations1, K1):.6f}")       # Output: 0.500000
    print()

    # Test case 2
    stations2 = [1,2,3,4,5,6,7,8,9,10]
    K2 = 1
    print("Test Case 2:")
    print(f"Stations: {stations2}, K: {K2}")
    print(f"Binary Search Solution: {solution.minmaxGasDist_binary_search(stations2, K2):.6f}")  # Output: 1.000000
    print(f"Math Approach Solution: {solution.minmaxGasDist_math_approach(stations2, K2):.6f}")    # Output: 1.000000
    print(f"Optimized Solution: {solution.minmaxGasDist_optimized(stations2, K2):.6f}")          # Output: 1.000000
    print(f"Final Optimized Solution: {solution.minmaxGasDist_final(stations2, K2):.6f}")       # Output: 1.000000
    print()

    # Test case 3
    stations3 = [1,2,3,4,5,6,7,8,9,10]
    K3 = 0
    print("Test Case 3:")
    print(f"Stations: {stations3}, K: {K3}")
    # Since K=0, no new stations can be added; the maximum distance remains the same
    max_gap3 = max(stations3[i] - stations3[i - 1] for i in range(1, len(stations3)))
    print(f"Expected Output: {max_gap3:.6f}")  # Output: 1.000000
    print()

    # Test case 4
    stations4 = [1,5,10]
    K4 = 2
    print("Test Case 4:")
    print(f"Stations: {stations4}, K: {K4}")
    print(f"Binary Search Solution: {solution.minmaxGasDist_binary_search(stations4, K4):.6f}")  # Expected Output: 2.5
    print(f"Math Approach Solution: {solution.minmaxGasDist_math_approach(stations4, K4):.6f}")    # Expected Output: 2.5
    print(f"Optimized Solution: {solution.minmaxGasDist_optimized(stations4, K4):.6f}")          # Expected Output: 2.5
    print(f"Final Optimized Solution: {solution.minmaxGasDist_final(stations4, K4):.6f}")       # Expected Output: 2.5
    print()

    # Test case 5
    stations5 = [1,2,3,4,5,6,7,8,9,10,100]
    K5 = 10
    print("Test Case 5:")
    print(f"Stations: {stations5}, K: {K5}")
    print(f"Binary Search Solution: {solution.minmaxGasDist_binary_search(stations5, K5):.6f}")  # Expected Output: ~9.090909
    print(f"Math Approach Solution: {solution.minmaxGasDist_math_approach(stations5, K5):.6f}")    # Expected Output: ~9.090909
    print(f"Optimized Solution: {solution.minmaxGasDist_optimized(stations5, K5):.6f}")          # Expected Output: ~9.090909
    print(f"Final Optimized Solution: {solution.minmaxGasDist_final(stations5, K5):.6f}")       # Expected Output: ~9.090909
    print()