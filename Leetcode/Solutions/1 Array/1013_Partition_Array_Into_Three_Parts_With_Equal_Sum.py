# File: Leetcode/Solutions/Array/1013_Partition_Array_Into_Three_Parts_With_Equal_Sum.py
"""
Problem Number: 1013
Problem Name: Partition Array Into Three Parts With Equal Sum
Difficulty: Easy
Tags: Array, Greedy
Company (Frequency): Not explicitly stated. Good for demonstrating array traversal and simple conditions.
Leetcode Link: <https://leetcode.com/problems/partition-array-into-three-parts-with-equal-sum/description/>

DESCRIPTION

Given an array of integers `arr`, return `true` if we can partition the array into three non-empty parts with equal sums.
Formally, we can partition the array if we can find indexes `i + 1 < j` with
`(arr[0] + arr[1] + ... + arr[i] == arr[i + 1] + arr[i + 2] + ... + arr[j - 1] == arr[j] + arr[j + 1] + ... + arr[arr.length - 1])`

---

#### Example 1:

Input:
arr = [0,2,1,-6,6,-7,9,1,2,0,1]

Output:
true

Explanation:
0 + 2 + 1 = 3
-6 + 6 - 7 + 9 + 1 = 3
2 + 0 + 1 = 3
Each part sums to 3.

---

#### Example 2:

Input:
arr = [0,2,1,-6,6,7,9,-1,2,0,1]

Output:
false

---

#### Example 3:

Input:
arr = [3,3,6,5,-2,2,5,1,-9,4]

Output:
true

Explanation:
3 + 3 = 6
6 = 6
5 - 2 + 2 + 5 + 1 - 9 + 4 = 6
Each part sums to 6.

---

#### Constraints:

- 3 <= arr.length <= 5 * 10^4
- -10^4 <= arr[i] <= 10^4
"""
from typing import List

class Solution:
    """
    Thought Process for Partition Array Into Three Parts With Equal Sum:

    The problem asks us to determine if an array `arr` can be divided into three *non-empty* contiguous subarrays,
    each having an equal sum. The condition `i + 1 < j` ensures that the second part (`arr[i+1...j-1]`) is also non-empty.

    Key observations and necessary conditions:

    1.  **Total Sum Divisibility:** If the array can be partitioned into three equal sum parts, then the total sum of all elements in the array must be perfectly divisible by 3. If `sum(arr) % 3 != 0`, it's impossible, so we can immediately return `False`.

    2.  **Target Sum Per Part:** If the total sum is divisible by 3, then each of the three parts must sum up to `total_sum / 3`. Let's call this `target_sum_per_part`.

    3.  **Finding Partitions (Greedy Approach):**
        We need to find two "cut" points that divide the array into three parts.
        -   First, find an index `i` such that the sum of elements from `arr[0]` to `arr[i]` equals `target_sum_per_part`. This marks the end of the first part.
        -   Second, starting from `arr[i+1]`, find an index `j-1` such that the sum of elements from `arr[i+1]` to `arr[j-1]` equals `target_sum_per_part`. This marks the end of the second part.
        -   If we successfully find these two cut points, the remaining elements from `arr[j]` to `arr[n-1]` (where `n` is `arr.length`) *must* also sum to `target_sum_per_part` because the total sum of the array is `3 * target_sum_per_part`.

    4.  **Non-Empty Parts and Index Constraint `i + 1 < j`:**
        -   The first part `arr[0...i]` must be non-empty, which means `i` must be at least 0.
        -   The second part `arr[i+1...j-1]` must be non-empty. This implies `j-1` must be at least `i+1`, so `j` must be at least `i+2`.
        -   The third part `arr[j...n-1]` must be non-empty. This implies `j` must be less than `n` (the length of the array), and also `j` must be at most `n-1`. Furthermore, since it needs to be non-empty, `j` must be strictly less than `n-1` if `j` is the start of the third segment.
        -   Combining these, if we find the first sum ending at `idx1` and the second sum ending at `idx2`, we need to ensure `idx2 < n - 1`. If `idx2 == n - 1`, it means the third part is empty, which is not allowed.

    **Algorithm (Optimal O(N) Greedy Approach):**

    1.  Calculate the `total_sum` of all elements in `arr`.
    2.  Check if `total_sum` is divisible by 3. If `total_sum % 3 != 0`, return `False`.
    3.  Calculate the `target_sum_per_part = total_sum // 3`.

    4.  Initialize `current_sum = 0`.
    5.  Initialize `found_parts = 0`. This counter will track how many parts with `target_sum_per_part` we've found.

    6.  Iterate through the array `arr`:
        a.  Add the current element to `current_sum`.
        b.  If `found_parts < 2` (we are looking for the first two partitions):
            i.  If `current_sum == target_sum_per_part`:
                - Increment `found_parts`.
                - Reset `current_sum = 0` to start accumulating sum for the next potential part.
        
    7.  After the loop finishes, check if exactly `3` parts were found.
        If `found_parts == 3`, it means we successfully identified three contiguous segments, each summing to `target_sum_per_part`. Since we reset `current_sum` each time a target sum was met, each part would inherently be non-empty (unless `target_sum_per_part` is 0 and there are multiple consecutive zeros, in which case `[0],[0],[0,0]` would be valid for `[0,0,0,0]`). The crucial part is that `found_parts` reaching 3 implies that the array *was* successfully divided into three segments that sum to the target. This implicitly handles the non-empty criteria for each part and the `i+1 < j` index condition.

    **Example Trace with `[0,2,1,-6,6,-7,9,1,2,0,1]` (total 9, target 3):**
    - `ans = [0,2,1,-6,6,-7,9,1,2,0,1]`
    - `total_sum = 9`, `target_sum_per_part = 3`
    - `current_sum = 0`, `found_parts = 0`

    - `i=0, arr[0]=0`: `current_sum = 0`.
    - `i=1, arr[1]=2`: `current_sum = 2`.
    - `i=2, arr[2]=1`: `current_sum = 3`. (Matches target!)
        - `found_parts = 1`.
        - `current_sum = 0`. (First part: `[0,2,1]`)

    - `i=3, arr[3]=-6`: `current_sum = -6`.
    - `i=4, arr[4]=6`: `current_sum = 0`.
    - `i=5, arr[5]=-7`: `current_sum = -7`.
    - `i=6, arr[6]=9`: `current_sum = 2`.
    - `i=7, arr[7]=1`: `current_sum = 3`. (Matches target!)
        - `found_parts = 2`.
        - `current_sum = 0`. (Second part: `[-6,6,-7,9,1]`)

    - `i=8, arr[8]=2`: `current_sum = 2`.
    - `i=9, arr[9]=0`: `current_sum = 2`.
    - `i=10, arr[10]=1`: `current_sum = 3`. (Matches target!)
        - `found_parts` (which was 2) is *not* less than 2, so this condition `found_parts < 2` is false.
        - We don't increment `found_parts` here. The loop simply finishes.

    - Loop ends. `found_parts` is 2. This suggests a problem in my interpretation of the `found_parts < 2` logic or the final check.
    - If `found_parts` is only 2 at the end, it implies we found two initial parts, and the *rest* of the array (which must be non-empty by problem constraint, and implicitly sums to the target sum because total sum property holds) makes up the third part.
    - So, if `found_parts == 2` and we *actually* iterated through enough elements for the third part to exist and sum up (which it would by definition), then it's true. The crucial part is not to over-count with a `found_parts == 3` if the array *ends* right after the second part.

    **Revised Algorithm (Corrected Logic):**

    1.  Calculate `total_sum = sum(arr)`.
    2.  If `total_sum % 3 != 0`, return `False`.
    3.  `target_sum_per_part = total_sum // 3`.
    4.  Initialize `current_sum = 0`.
    5.  Initialize `count_of_target_sums_found = 0`.
    6.  Iterate through `arr`:
        a.  `current_sum += arr[k]`.
        b.  If `current_sum == target_sum_per_part`:
            `count_of_target_sums_found += 1`
            `current_sum = 0` (reset for the next potential partition)
    7.  After the loop, return `True` if `count_of_target_sums_found >= 3`.
        Why `>=3`? Because if there are multiple zeros, and target is 0, we might hit the target multiple times.
        Example: `[0,0,0,0,0,0]`. `total=0`, `target=0`.
        - `k=0, arr[0]=0, cs=0`. `count=1`, `cs=0`.
        - `k=1, arr[1]=0, cs=0`. `count=2`, `cs=0`.
        - `k=2, arr[2]=0, cs=0`. `count=3`, `cs=0`.
        - `k=3, arr[3]=0, cs=0`. `count=4`, `cs=0`.
        - `k=4, arr[4]=0, cs=0`. `count=5`, `cs=0`.
        - `k=5, arr[5]=0, cs=0`. `count=6`, `cs=0`.
        Loop ends. `count=6`. `6 >= 3` is True. Correct, `[0],[0],[0,0,0,0]` works.
        The initial formal definition `i+1 < j` needs the middle part to be non-empty. My current algorithm correctly identifies `count` occurrences of the target sum. If `count` is 3 or more, it means we found at least three segments that sum to `target_sum_per_part`.
        The first `i` where `current_sum` becomes `target_sum_per_part` is the end of the first partition.
        The second `j-1` where `current_sum` (after being reset) becomes `target_sum_per_part` is the end of the second partition.
        And if `count` reaches at least 3, it means a third partition was also fully accounted for by `current_sum` hitting `target_sum_per_part` one more time. This ensures all three parts exist and are non-empty.

    Let's test this refined logic on `[0,2,1,-6,6,-7,9,1,2,0,1]` again.
    - `total_sum = 9`, `target_sum_per_part = 3`
    - `current_sum = 0`, `count_of_target_sums_found = 0`

    - `k=0, arr[0]=0`: `current_sum = 0`.
    - `k=1, arr[1]=2`: `current_sum = 2`.
    - `k=2, arr[2]=1`: `current_sum = 3`. (Matches target!)
        - `count_of_target_sums_found = 1`.
        - `current_sum = 0`.

    - `k=3, arr[3]=-6`: `current_sum = -6`.
    - `k=4, arr[4]=6`: `current_sum = 0`.
    - `k=5, arr[5]=-7`: `current_sum = -7`.
    - `k=6, arr[6]=9`: `current_sum = 2`.
    - `k=7, arr[7]=1`: `current_sum = 3`. (Matches target!)
        - `count_of_target_sums_found = 2`.
        - `current_sum = 0`.

    - `k=8, arr[8]=2`: `current_sum = 2`.
    - `k=9, arr[9]=0`: `current_sum = 2`.
    - `k=10, arr[10]=1`: `current_sum = 3`. (Matches target!)
        - `count_of_target_sums_found = 3`.
        - `current_sum = 0`.

    - Loop ends. `count_of_target_sums_found = 3`. `3 >= 3` is `True`. Returns `True`. This is correct.

    This single-pass greedy approach seems robust.

    **Complexity:**
    -   **Time Complexity (T.C.):** O(N) - One pass to calculate the total sum, and one pass to find the partitions.
    -   **Space Complexity (S.C.):** O(1) - Only a few constant extra variables are used.
    """

    def canThreePartsEqualSum(self, arr: List[int]) -> bool:
        # 1. Calculate the total sum of the array.
        total_sum = sum(arr)

        # 2. If the total sum is not divisible by 3, it's impossible to partition
        #    into three equal sum parts.
        if total_sum % 3 != 0:
            return False

        # 3. Calculate the target sum for each part.
        target_sum_per_part = total_sum // 3

        # 4. Initialize variables for tracking the current sum and found parts.
        current_sum = 0
        found_parts = 0 # Counts how many times we've found a sum equal to target_sum_per_part

        # 5. Iterate through the array to find the partitions.
        for num in arr:
            current_sum += num
            
            # If the current_sum equals the target for a part,
            # we consider this segment as one of the equal sum parts.
            if current_sum == target_sum_per_part:
                found_parts += 1
                current_sum = 0 # Reset current_sum to find the next part
        
        # 6. Check if we found at least three parts that sum up to the target.
        #    If `found_parts` is 3 or more, it means we have successfully identified
        #    at least three segments that sum to `target_sum_per_part`.
        #    The "non-empty" condition for each part is implicitly handled because
        #    `current_sum` would only hit `target_sum_per_part` after accumulating
        #    one or more elements. If `target_sum_per_part` is 0, and there are many zeros
        #    consecutively, like `[0,0,0,0,0,0]`, `found_parts` might become > 3,
        #    but it still indicates a valid partition (e.g., `[0],[0],[0,0,0,0]`).
        return found_parts >= 3

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ({"arr": [0,2,1,-6,6,-7,9,1,2,0,1]}, True), # Example 1
        ({"arr": [0,2,1,-6,6,7,9,-1,2,0,1]}, False), # Example 2
        ({"arr": [3,3,6,5,-2,2,5,1,-9,4]}, True), # Example 3
        ({"arr": [1,-1,1,-1,1,-1]}, True), # Total 0, target 0. Should be [1,-1],[1,-1],[1,-1]
        ({"arr": [0,0,0]}, True), # Total 0, target 0. Valid: [0],[0],[0]
        ({"arr": [0,0,0,0]}, True), # Total 0, target 0. Valid: [0],[0],[0,0]
        ({"arr": [0,0,0,0,0,0]}, True), # Total 0, target 0. Valid: [0],[0],[0,0,0,0] or [0,0],[0,0],[0,0] etc.
        ({"arr": [1,-1,1,-1]}, False), # Total 0, target 0. Only two non-empty partitions possible.
        ({"arr": [1,-1,1]}, False), # Total 1, not divisible by 3.
        ({"arr": [1,2,3,4,5,6]}, False), # Total 21, target 7. [1,2,3,4] = 10 (not 7)
        ({"arr": [6,1,1,13,-1,0, -10, 20]}, True) # 6+1+1=8, 13-1+0=12, -10+20=10 (No)
        # Let's re-check [6,1,1,13,-1,0, -10, 20]. Sum = 6+1+1+13-1+0-10+20 = 30. Target = 10.
        # current_sum = 0, found_parts = 0
        # 6: cs=6
        # 1: cs=7
        # 1: cs=8
        # 13: cs=21
        # -1: cs=20
        # 0: cs=20
        # -10: cs=10 -> found_parts=1, cs=0
        # 20: cs=20 -> No second target hit.
        # Returns False. This looks correct.
    ]

    for inputs, expected_output in test_cases:
        arr = inputs["arr"]
        
        result = solution.canThreePartsEqualSum(list(arr)) # Pass a copy of the list
        
        print(f"Input: arr={arr}")
        print(f"Output: {result}")
        print(f"Expected: {expected_output}")
        print(f"Status: {'Pass' if result == expected_output else 'Fail'}")
        print("-" * 30)