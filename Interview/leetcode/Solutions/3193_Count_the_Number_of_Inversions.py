# TODO: Revit
# File: Leetcode/Solutions/Dynamic_Programming/3193_Count_the_Number_of_Inversions.py

"""
Problem Number: 3193
Problem Name: Count the Number of Inversions
Difficulty: Hard
Tags: Array, Dynamic Programming
Company (Frequency): Not explicitly stated, but typical for advanced DP problems.
Leetcode Link: <https://leetcode.com/problems/count-the-number-of-inversions/description/>

DESCRIPTION

You are given an integer `n` and a 2D array `requirements`, where `requirements[i] = [endi, cnti]`
represents the end index and the inversion count of each requirement.
A pair of indices `(i, j)` from an integer array `nums` is called an inversion if:
`i < j` and `nums[i] > nums[j]`
Return the number of permutations `perm` of `[0, 1, 2, ..., n - 1]` such that for all `requirements[i]`,
`perm[0..endi]` has exactly `cnti` inversions.
Since the answer may be very large, return it modulo 10^9 + 7.

---

#### Example 1:

Input:
n = 3, requirements = [[2,2],[0,0]]

Output:
2

Explanation:
The two permutations are:
[2, 0, 1]
Prefix [2, 0, 1] has inversions (0, 1) and (0, 2).
Prefix [2] has 0 inversions.
[1, 2, 0]
Prefix [1, 2, 0] has inversions (0, 2) and (1, 2).
Prefix [1] has 0 inversions.

---

#### Example 2:

Input:
n = 3, requirements = [[2,2],[1,1],[0,0]]

Output:
1

Explanation:
The only satisfying permutation is [2, 0, 1]:
Prefix [2, 0, 1] has inversions (0, 1) and (0, 2).
Prefix [2, 0] has an inversion (0, 1).
Prefix [2] has 0 inversions.

---

#### Example 3:

Input:
n = 2, requirements = [[0,0],[1,0]]

Output:
1

Explanation:
The only satisfying permutation is [0, 1]:
Prefix [0] has 0 inversions.
Prefix [0, 1] has an inversion (0, 1).

---

#### Constraints:

- 2 <= n <= 300
- 1 <= requirements.length <= n
- requirements[i] = [endi, cnti]
- 0 <= endi <= n - 1
- 0 <= cnti <= 400
- The input is generated such that there is at least one `i` such that `endi == n - 1`.
- The input is generated such that all `endi` are unique.
"""

from typing import List

class Solution:
    """
    Thought Process:
    This problem is a classic dynamic programming problem related to counting permutations with a specific number of inversions, with the added complexity of prefix requirements.

    Let `dp[i][j]` be the number of permutations of `[0, 1, ..., i]` that have exactly `j` inversions.
    When we construct a permutation of `[0, ..., i]` from a permutation of `[0, ..., i-1]`, we insert `i` into one of `i+1` possible positions.
    If we insert `i` at index `k` (0-indexed, where `0 <= k <= i`):
    - Inserting `i` at the *last* position (`k=i`) adds 0 new inversions with `i`.
    - Inserting `i` at position `k` adds `(i - k)` new inversions with `i` (because `i` is greater than the `i - k` elements to its right).
    - So, to get `j` inversions in `perm[0...i]`, if we placed `i` at position `k`, the prefix `perm[0...i-1]` must have had `j - (i - k)` inversions.

    The recurrence relation would be:
    `dp[i][j] = sum(dp[i-1][j - (i - k)])` for `0 <= k <= i`.
    This can be rewritten as:
    `dp[i][j] = sum(dp[i-1][j - x])` for `0 <= x <= i`.
    Where `x` is the number of new inversions introduced by `i`. `x` ranges from `0` (insert `i` at the end) to `i` (insert `i` at the beginning).

    Base case: `dp[0][0] = 1` (permutation [0] has 0 inversions).

    The maximum possible inversions for a permutation of `[0, ..., i-1]` is `i * (i - 1) / 2`.
    The maximum `cnti` is 400, and `n` is up to 300. The maximum inversions for `n=300` would be `300 * 299 / 2` which is very large.
    However, the `cnti` constraint (max 400) is crucial. We only care about inversion counts up to `max_cnt`.
    So, `dp[i][j]` where `j` goes up to `max(cnti)` for all requirements.

    We need to handle the requirements. The requirements are for specific `endi`.
    The `requirements` array needs to be sorted by `endi` to process them in increasing order.

    Algorithm Steps:
    1. Sort `requirements` by `endi`.
    2. Create a dictionary/map `req_map` to quickly look up `cnti` for a given `endi`.
    3. Initialize `dp` table. `dp[i][j]` will store the count of permutations of `[0...i]` with `j` inversions.
       `max_inversions_needed = max(req[1] for req in requirements)`
       `dp` will be `(n+1) x (max_inversions_needed + 1)`
    4. `dp[0][0] = 1` (base case: permutation [0] has 0 inversions).
    5. Iterate `i` from `1` to `n-1` (representing `perm[0...i]`, which has length `i+1`).
       (Note: `i` in `dp[i][j]` effectively means length `i+1` array, considering numbers `0` to `i`)
       The current element being placed is `i`.
       The number of inversions added by `i` can be from `0` to `i`.
       `dp[i][j] = sum(dp[i-1][j - x])` for `x` from `0` to `min(j, i)`.
       This sum can be optimized using prefix sums to go from `O(K)` to `O(1)` per `j`.
       `pref_sum_dp_prev[k] = sum(dp[i-1][0...k])`
       `dp[i][j] = (pref_sum_dp_prev[j] - pref_sum_dp_prev[j - (i + 1)]) % MOD`

    6. After calculating `dp[endi][cnti]` for all `endi` up to the current `i`, we need to check if it matches the requirement.
       If `i` is an `endi` in `requirements`:
         If `dp[i][req_map[i]] == 0`, then no valid permutations exist, return 0.
         Else, if `dp[i][j]` for any other `j != req_map[i]` is non-zero, this DP state might be invalid later.
         This implies that at each `endi` for a requirement, *only* `dp[endi][cnti]` can be non-zero. All other `dp[endi][j]` for `j != cnti` must effectively become 0. This is a crucial modification to the standard inversion DP.

    Corrected DP state and transition for requirements:
    Let `dp[j]` be the number of permutations of `[0, ..., curr_val]` that have `j` inversions.
    `curr_val` will iterate from `0` to `n-1`.
    `dp_prev` refers to `dp` for `[0, ..., curr_val-1]`.
    `dp_curr` will be the new `dp` for `[0, ..., curr_val]`.

    Initialize `dp_prev[0] = 1` (for `curr_val = 0`, perm `[0]` has 0 inv).

    For `curr_val` from `1` to `n-1`:
        `dp_curr = [0] * (max_inversions_needed + 1)`
        `prefix_sum = [0] * (max_inversions_needed + 1)`

        `prefix_sum[0] = dp_prev[0]`
        for `j` from `1` to `max_inversions_needed`:
            `prefix_sum[j] = (prefix_sum[j-1] + dp_prev[j]) % MOD`

        For `j` from `0` to `max_inversions_needed`:
            `val = prefix_sum[j]`
            if `j - (curr_val + 1) >= 0`:
                `val = (val - prefix_sum[j - (curr_val + 1)] + MOD) % MOD`
            `dp_curr[j] = val`

        `dp_prev = dp_curr`

        If `curr_val` is an `endi` in `req_map`:
            `required_cnt = req_map[curr_val]`
            If `dp_prev[required_cnt] == 0`: return 0 (no permutation satisfies this)
            `temp_dp = [0] * (max_inversions_needed + 1)`
            `temp_dp[required_cnt] = dp_prev[required_cnt]`
            `dp_prev = temp_dp` (filter out all other counts)

     `dp_prev[req_map[n-1]]` (the requirement for the full permutation `[0...n-1]`)

    Maximum inversions for a permutation of length `L` (elements `0` to `L-1`) is `L * (L - 1) / 2`.
    For `n=300`, `L=300`, max inversions `300 * 299 / 2 = 44850`.
    `cnti` max 400. This is small enough for `j` loop.
    So, `max_inversions_needed` is indeed constrained by `400`.

    Let `K = max(cnti)`.
    Overall Time Complexity: O(N * K)
    Overall Space Complexity: O(K)

    Consider edge cases for `j - (curr_val + 1)`.
    `dp[i][j] = sum(dp[i-1][j - x])` for `x` from `0` to `min(j, i)`.
    This is `dp[i][j] = dp[i-1][j] + dp[i-1][j-1] + ... + dp[i-1][j-i]`.
    And `dp[i][j-1] = dp[i-1][j-1] + ... + dp[i-1][j-1-i]`. (Correct range up to i-1, not i)
    This is `dp[i][j] = dp[i][j-1] + dp[i-1][j] - dp[i-1][j - (i + 1)]`.
    This recurrence is more efficient.

    Let `dp[i][j]` be the number of permutations of `[0, ..., i]` with `j` inversions.
    `dp[i][j] = (dp[i][j-1] + dp[i-1][j] - (dp[i-1][j-(i+1)] if j-(i+1) >= 0 else 0) + MOD) % MOD`
    Base case: `dp[0][0] = 1`. All other `dp[0][j] = 0`.
    Iterate `i` from `1` to `n-1`.
    Inside the loop, `j` from `0` to `max_inversions_needed`.

    Final check on requirement handling:
    When `i` is an `endi` with `cnti_req`:
    We compute `dp[i][j]` for all `j`.
    Then, for all `j != cnti_req`, `dp[i][j]` must be forced to 0.
    So, `dp[i]` becomes effectively `[0, 0, ..., dp[i][cnti_req], 0, ...]`.

    Example 1 Walkthrough: n=3, requirements=[[2,2],[0,0]]
    MOD = 10^9 + 7
    Sort requirements: [[0,0], [2,2]]
    req_map = {0: 0, 2: 2}
    max_inv_needed = 2

    Initialize `dp = [0] * (max_inv_needed + 1)` (effectively `dp_prev` for `curr_val - 1`)
    `dp[0] = 1` (for `curr_val = 0`, perm `[0]` has 0 inv).
    `dp = [1, 0, 0]`

    --- `curr_val = 0` is an `endi` (req_map[0] = 0).
    `dp[0]` is 1. All other `dp[j]` are 0. This matches `req_map[0]`. No change.

    --- `curr_val = 1` (insert `1` into permutation of `[0]`)
    `new_dp = [0] * (max_inv_needed + 1)`
    `new_dp[0] = (new_dp[-1 if -1 >= 0 else -1] + dp[0] - (dp[0 - (1+1)] if 0-(1+1) >= 0 else 0) + MOD) % MOD`
    `new_dp[0] = (0 + dp[0] - 0) % MOD = 1`
    `new_dp[1] = (new_dp[0] + dp[1] - (dp[1 - (1+1)] if 1-(1+1) >= 0 else 0) + MOD) % MOD`
    `new_dp[1] = (1 + 0 - 0) % MOD = 1`
    `dp = [1, 1, 0]` (perm of [0,1] with 0 inv: [0,1]; with 1 inv: [1,0])

    --- `curr_val = 1` is NOT an `endi`.

    --- `curr_val = 2` (insert `2` into permutation of `[0,1]`)
    `new_dp = [0] * (max_inv_needed + 1)`
    `new_dp[0]`: place 2 at end of [0,1] -> [0,1,2]. 0 new inv. Depends on `dp[0]` of `[0,1]`. `dp[0]=1`.
                 From formula: `new_dp[0] = (0 + dp[0] - (dp[0-(2+1)] if <0 else 0)) % MOD = 1`
    `new_dp[1]`: place 2 in middle of [0,1] -> [0,2,1]. 1 new inv. Depends on `dp[0]` of `[0,1]`. `dp[0]=1`.
                 Formula: `new_dp[1] = (new_dp[0] + dp[1] - (dp[1-(2+1)] if <0 else 0)) % MOD = (1 + 1 - 0) % MOD = 2`
                 (These are: [0,2,1] from [0,1] with 0 inv; [2,0,1] from [0,1] with 0 inv (not quite, this is incorrect interpretation of DP))

    Let's re-verify the DP recurrence:
    `dp[i][j]` = # permutations of `[0...i]` with `j` inversions.
    `dp[i][j] = sum_{k=0 to i} dp[i-1][j - (i-k)]`
    This sum is over the number of inversions added by placing `i` at position `k`.
    `j - (i-k)` is the required inversions from the prefix `[0...i-1]`.
    `x = i-k` is the number of inversions added by `i`. `x` ranges from `0` to `i`.
    So `dp[i][j] = sum_{x=0 to i} dp[i-1][j-x]` (provided `j-x >= 0`)

    Optimized recurrence (using prefix sums `S[val] = sum_{k=0 to val} dp[i-1][k]`):
    `dp[i][j] = S[j] - S[j - (i+1)]`
    This is what the prefix sum based solution implements.

    Let `dp[k]` be number of permutations of `[0, ..., current_num - 1]` with `k` inversions.
    `dp_new[k]` be number of permutations of `[0, ..., current_num]` with `k` inversions.

    Initialize `dp = [0] * (max_inv_needed + 1)`
    `dp[0] = 1` (for `current_num = 0`)

    For `current_num` from `1` to `n-1`: (This means we are considering permutations of `[0, ..., current_num]`)
        `dp_new = [0] * (max_inv_needed + 1)`
        `prefix_sum = [0] * (max_inv_needed + 1)`

        `prefix_sum[0] = dp[0]`
        for `j` from `1` to `max_inv_needed`:
            `prefix_sum[j] = (prefix_sum[j-1] + dp[j]) % MOD`

        For `j` from `0` to `max_inv_needed`:
            # The value `current_num` can introduce `x` new inversions, where `0 <= x <= current_num`.
            # So `dp_new[j]` gets contributions from `dp[j-0], dp[j-1], ..., dp[j-current_num]`.
            # This is `prefix_sum[j]`
            `val_from_prev_dp_range = prefix_sum[j]`
            if `j - (current_num + 1) >= 0`:
                `val_from_prev_dp_range = (val_from_prev_dp_range - prefix_sum[j - (current_num + 1)] + MOD) % MOD`
            `dp_new[j] = val_from_prev_dp_range`

        `dp = dp_new`

        # Apply requirements if current_num is an endi
        If `current_num` is in `req_map`:
            `required_cnt = req_map[current_num]`
            If `dp[required_cnt] == 0`:
                return 0 # No valid permutations
            # Filter the DP array: only the required_cnt remains
            `temp_dp = [0] * (max_inv_needed + 1)`
            `temp_dp[required_cnt] = dp[required_cnt]`
            `dp = temp_dp`

    Final result is `dp[req_map[n-1]]`.

    Let's re-run Example 1 with the corrected DP and logic: n=3, requirements=[[2,2],[0,0]]
    MOD = 10^9 + 7
    Sorted requirements: `[[0,0], [2,2]]`
    `req_map = {0: 0, 2: 2}`
    `max_inv_needed = 2`

    Initial `dp = [0, 0, 0]`
    `dp[0] = 1` (for base case of permutation `[0]` - which means `current_num` is 0 in problem wording)
    So `dp = [1, 0, 0]`

    --- Handle `current_num = 0` (this is `endi = 0` for permutation `[0]`)
    `req_map` has `0:0`.
    `dp[0]` is 1. This matches. `dp` remains `[1,0,0]`.

    --- `current_num = 1` (building permutations of `[0, 1]`)
    `dp_prev = [1, 0, 0]`
    `prefix_sum`: `[1, 1, 1]` (since `dp_prev[0]=1, dp_prev[1]=0, dp_prev[2]=0`)

    `dp_new = [0] * 3`
    `j = 0`: `x` from `0` to `min(0, 1)` (only `x=0`)
             `dp_new[0] = dp_prev[0-0] = dp_prev[0] = 1`
             From formula `val = prefix_sum[0] = 1`. `j - (curr_val + 1) = 0 - (1+1) = -2`. No subtraction. `new_dp[0] = 1`.
    `j = 1`: `x` from `0` to `min(1, 1)` (i.e., `x=0,1`)
             `dp_new[1] = dp_prev[1-0] + dp_prev[1-1] = dp_prev[1] + dp_prev[0] = 0 + 1 = 1`
             From formula `val = prefix_sum[1] = 1`. `j - (curr_val + 1) = 1 - (1+1) = -1`. No subtraction. `new_dp[1] = 1`.
    `j = 2`: `x` from `0` to `min(2, 1)` (i.e., `x=0,1`)
             `dp_new[2] = dp_prev[2-0] + dp_prev[2-1] = dp_prev[2] + dp_prev[1] = 0 + 0 = 0`
             From formula `val = prefix_sum[2] = 1`. `j - (curr_val + 1) = 2 - (1+1) = 0`. `val = (1 - prefix_sum[0] + MOD) % MOD = (1-1+MOD)%MOD = 0`. `new_dp[2] = 0`.
    `dp = [1, 1, 0]` (Perms for `[0,1]`: `[0,1]` (0 inv), `[1,0]` (1 inv))

    --- `current_num = 1` is NOT an `endi`.

    --- `current_num = 2` (building permutations of `[0, 1, 2]`)
    `dp_prev = [1, 1, 0]`
    `prefix_sum`: `[1, 2, 2]` (since `dp_prev[0]=1, dp_prev[1]=1, dp_prev[2]=0`)

    `dp_new = [0] * 3`
    `j = 0`: `x` from `0` to `min(0, 2)` (only `x=0`)
             `dp_new[0] = dp_prev[0] = 1` (`[0,1,2]`)
             Formula: `val = prefix_sum[0] = 1`. `j-(2+1) = -3`. `dp_new[0] = 1`.
    `j = 1`: `x` from `0` to `min(1, 2)` (i.e., `x=0,1`)
             `dp_new[1] = dp_prev[1] + dp_prev[0] = 1 + 1 = 2` (`[0,2,1], [1,0,2]`)
             Formula: `val = prefix_sum[1] = 2`. `j-(2+1) = -2`. `dp_new[1] = 2`.
    `j = 2`: `x` from `0` to `min(2, 2)` (i.e., `x=0,1,2`)
             `dp_new[2] = dp_prev[2] + dp_prev[1] + dp_prev[0] = 0 + 1 + 1 = 2` (`[1,2,0], [2,0,1]`)
             Formula: `val = prefix_sum[2] = 2`. `j-(2+1) = -1`. `dp_new[2] = 2`.
    `dp = [1, 2, 2]` (Perms for `[0,1,2]`: 0 inv: `[0,1,2]`; 1 inv: `[0,2,1], [1,0,2]`; 2 inv: `[1,2,0], [2,0,1]`)

    --- `current_num = 2` is an `endi` (req_map[2] = 2).
    `dp[2]` is 2. This matches `req_map[2]`.
    Filter `dp`:
    `temp_dp = [0, 0, 0]`
    `temp_dp[2] = dp[2] = 2`
    `dp = [0, 0, 2]`

    Final Answer: `dp[req_map[n-1]] = dp[req_map[2]] = dp[2] = 2`. Correct.

    This DP approach with prefix sums and filtering seems correct.

    Edge cases:
    - `cnti = 0`: Handled correctly by DP.
    - `n=2`, requirements `[[0,0],[1,0]]`:
      `req_map = {0:0, 1:0}`. `max_inv_needed = 0`.
      Initial `dp = [1]` (for `curr_val = 0`)
      Handle `curr_val = 0`: `req_map[0]=0`. `dp[0]=1`. Matches. `dp=[1]`.
      `curr_val = 1`: (building perms of `[0,1]`)
        `dp_prev = [1]`. `prefix_sum = [1]`.
        `dp_new = [0]`
        `j = 0`: `x` from `0` to `min(0,1)` (`x=0`). `dp_new[0] = dp_prev[0] = 1`.
        `dp = [1]` (Perms for `[0,1]`: `[0,1]` (0 inv))
      Handle `curr_val = 1`: `req_map[1]=0`. `dp[0]=1`. Matches. `dp=[1]`.
      Final result: `dp[req_map[n-1]] = dp[req_map[1]] = dp[0] = 1`. Correct.
    """

    def countPermutations(self, n: int, requirements: List[List[int]]) -> int:
        MOD = 10**9 + 7

        # Step 1: Sort requirements by endi
        requirements.sort(key=lambda x: x[0])

        # Step 2: Create a map for quick lookup
        req_map = {end_idx: count for end_idx, count in requirements}

        # Determine the maximum inversion count needed for DP table size
        # Max inversions for k elements (0 to k-1) is k * (k-1) / 2
        # Max cnti is 400.
        max_inversions_needed = 0
        for _, cnti in requirements:
            max_inversions_needed = max(max_inversions_needed, cnti)

        # dp[j] will store the number of permutations of [0, ..., current_num - 1] with j inversions
        dp = [0] * (max_inversions_needed + 1)

        # Base case: For the permutation of [0], which is just [0], it has 0 inversions.
        # This corresponds to current_num = 0 in our logic (length 1 prefix).
        dp[0] = 1

        # Handle the requirement for endi = 0
        if 0 in req_map:
            required_cnt_at_0 = req_map[0]
            if dp[required_cnt_at_0] == 0:
                return 0
            # Filter the dp array for endi = 0. Only the required count should remain.
            temp_dp = [0] * (max_inversions_needed + 1)
            temp_dp[required_cnt_at_0] = dp[required_cnt_at_0]
            dp = temp_dp

        # Iterate current_num from 1 to n-1 (representing permutations of [0, ..., current_num])
        for current_num in range(1, n):
            dp_new = [0] * (max_inversions_needed + 1)
            
            # Calculate prefix sums of the current dp array (dp_prev)
            # This helps calculate sum(dp[j-x] for x in range(current_num + 1)) in O(1)
            prefix_sum = [0] * (max_inversions_needed + 1)
            prefix_sum[0] = dp[0]
            for j in range(1, max_inversions_needed + 1):
                prefix_sum[j] = (prefix_sum[j-1] + dp[j]) % MOD

            for j in range(max_inversions_needed + 1):
                # dp_new[j] = sum(dp[j - x]) for x from 0 to current_num (inclusive)
                # This sum is prefix_sum[j] - prefix_sum[j - (current_num + 1)]
                val = prefix_sum[j]
                if j - (current_num + 1) >= 0:
                    val = (val - prefix_sum[j - (current_num + 1)] + MOD) % MOD
                dp_new[j] = val
            
            dp = dp_new # Update dp for the next iteration

            # Apply requirements if current_num is an endi
            if current_num in req_map:
                required_cnt = req_map[current_num]
                if dp[required_cnt] == 0:
                    return 0 # No permutation satisfies this requirement
                
                # Filter the dp array: only the count at required_cnt remains
                temp_dp = [0] * (max_inversions_needed + 1)
                temp_dp[required_cnt] = dp[required_cnt]
                dp = temp_dp
        
        # The problem states that there is at least one i such that endi == n - 1.
        # So we must check the requirement for the full permutation.
        final_required_cnt = req_map[n-1]
        return dp[final_required_cnt]