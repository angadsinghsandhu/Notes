# TODO: new

# File: Leetcode/Solutions/354_Russian_Doll_Envelopes.py

"""
Problem Number: 354
Problem Name: Russian Doll Envelopes
Difficulty: Hard
Tags: Array, Binary Search, Dynamic Programming, Sorting
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/russian-doll-envelopes/description/

DESCRIPTION

You are given a 2D array of integers `envelopes` where `envelopes[i] = [wi, hi]` represents the width and the height of an envelope.

One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height.

Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).

Note: You cannot rotate an envelope.

---

#### Example 1:
**Input:**
```plaintext
envelopes = [[5,4],[6,4],[6,7],[2,3]]
```

**Output:**
```plaintext
3
```

**Explanation:**  
The maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).

#### Example 2:
**Input:**
```plaintext
envelopes = [[1,1],[1,1],[1,1]]
```

**Output:**
```plaintext
1
```

**Explanation:**  
Only one envelope can be used since all envelopes have the same dimensions.

#### Constraints:
- `1 <= envelopes.length <= 10^5`
- `envelopes[i].length == 2`
- `1 <= wi, hi <= 10^5`
"""

from bisect import bisect_left
from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding the maximum number of envelopes that can be nested inside each other.
    - A brute-force approach involves checking every pair of envelopes, but this is inefficient.
    - An optimized approach involves sorting the envelopes and then using a variation of the Longest Increasing Subsequence (LIS) algorithm to find the maximum sequence of nested envelopes.

    Input:
        envelopes: List[List[int]] - A list of envelopes where each envelope is represented by its width and height.

    Output:
        int - The maximum number of envelopes that can be nested.
    """

    def brute_force_solution(self, envelopes: List[List[int]]) -> int:
        """
        Approach:
        - Sort the envelopes by width and height.
        - Iterate through every possible pair of envelopes and check if one can fit into the other.
        - Track the maximum number of envelopes that can be nested.

        T.C.: O(n^2) - Checking every pair of envelopes.
        S.C.: O(n) - Space for storing the DP array.
        """
        if not envelopes:
            return 0

        # Sort envelopes by width and height
        envelopes.sort()
        n = len(envelopes)
        dp = [1] * n  # DP array to store the maximum number of nested envelopes up to each index

        for i in range(1, n):
            for j in range(i):
                if envelopes[j][0] < envelopes[i][0] and envelopes[j][1] < envelopes[i][1]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    def optimized_solution(self, envelopes: List[List[int]]) -> int:
        """
        Approach:
        - Sort the envelopes by width in ascending order and by height in descending order.
        - Use a variation of the Longest Increasing Subsequence (LIS) algorithm to find the maximum sequence of nested envelopes.
        - Implement LIS using binary search for efficiency.

        T.C.: O(n log n) - Sorting and binary search.
        S.C.: O(n) - Space for storing the DP array.
        """
        if not envelopes:
            return 0

        # Sort envelopes by width in ascending order and by height in descending order
        envelopes.sort(key=lambda x: (x[0], -x[1]))

        # Initialize the DP array with the height of the first envelope
        dp = [envelopes[0][1]]

        for _, h in envelopes[1:]:
            if h > dp[-1]:
                dp.append(h)
            else:
                # Find the position to replace using binary search
                idx = bisect_left(dp, h)
                dp[idx] = h

        return len(dp)

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    envelopes1 = [[5,4],[6,4],[6,7],[2,3]]
    print(solution.brute_force_solution(envelopes1))  # Output: 3
    print(solution.optimized_solution(envelopes1))    # Output: 3

    # Test case 2
    envelopes2 = [[1,1],[1,1],[1,1]]
    print(solution.brute_force_solution(envelopes2))  # Output: 1
    print(solution.optimized_solution(envelopes2))    # Output: 1
