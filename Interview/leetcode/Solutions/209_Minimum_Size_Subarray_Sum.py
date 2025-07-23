# File: Leetcode/Solutions/Array/209_Minimum_Size_Subarray_Sum.py
"""
Problem Number: 209
Problem Name: Minimum Size Subarray Sum
Difficulty: Medium
Tags: Array, Binary Search, Sliding Window, Prefix Sum
Company (Frequency): A common problem testing sliding window and potentially binary search on prefix sums.
Leetcode Link: <https://leetcode.com/problems/minimum-size-subarray-sum/description/>

DESCRIPTION

Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a subarray whose sum is greater than or equal to `target`. If there is no such subarray, return `0` instead.

---

#### Example 1:

Input:
target = 7, nums = [2,3,1,2,4,3]

Output:
2

Explanation:
The subarray [4,3] has the minimal length under the problem constraint.

---

#### Example 2:

Input:
target = 4, nums = [1,4,4]

Output:
1

Explanation:

---

#### Example 3:

Input:
target = 11, nums = [1,1,1,1,1,1,1,1]

Output:
0

---

#### Constraints:

- 1 <= target <= 10^9
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^4

---

#### Follow up:

If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log(n)).
"""
import bisect
from typing import List

class Solution:
    """
    Thought Process for Minimum Size Subarray Sum:

    The problem asks for the shortest contiguous subarray whose sum is greater than or equal to a given `target`.
    The input array `nums` contains only *positive* integers. This is a crucial constraint.

    Let's explore different approaches:

    1.  **Brute Force:**
        -   **Idea:** Generate all possible subarrays, calculate their sum, and keep track of the minimum length satisfying the condition.
        -   **Algorithm:**
            1. Initialize `min_length = infinity`.
            2. Outer loop `i` from 0 to `n-1` (start of subarray).
            3. Inner loop `j` from `i` to `n-1` (end of subarray).
            4. Calculate `current_sum = sum(nums[k] for k in range(i, j+1))`.
            5. If `current_sum >= target`, update `min_length = min(min_length, j - i + 1)`.
            6. Return `min_length` (or 0 if still infinity).
        -   **Time Complexity (T.C.):** O(N^2) if sums are calculated iteratively (O(N^3) if `sum()` on slices is used repeatedly).
        -   **Space Complexity (S.C.):** O(1).
        -   **Problem:** Too slow for `N = 10^5`. `10^5 * 10^5 = 10^10` operations.

    2.  **Sliding Window (Optimal O(N) Solution):**
        -   **Idea:** This is the most efficient approach for this problem, leveraging the "positive integers" constraint. We maintain a "window" defined by `left` and `right` pointers. We expand the window from the `right` and shrink it from the `left` while maintaining the sum.
        -   **Why it works with positive integers:** When elements are positive, adding an element always increases the sum, and removing an element always decreases it. This monotonic property allows the pointers to move in a coordinated way without needing to backtrack.
        -   **Algorithm:**
            1.  Initialize `min_length = float('inf')` (or `math.inf`). This will store the minimal length found so far.
            2.  Initialize `window_sum = 0`. This stores the sum of elements within the current window `nums[left...right]`.
            3.  Initialize `left = 0`. This pointer marks the beginning of the current window.
            4.  Iterate `right` from 0 to `n-1` (this pointer expands the window):
                a.  Add `nums[right]` to `window_sum`.
                b.  **While `window_sum >= target`:** This means we have found a valid subarray.
                    i.  Update `min_length = min(min_length, right - left + 1)`. `right - left + 1` is the current window length.
                    ii. Try to shrink the window from the left to find a smaller valid subarray. Subtract `nums[left]` from `window_sum`.
                    iii. Increment `left` to move the window's start.
            5.  After the loop, if `min_length` is still `float('inf')`, it means no such subarray was found, so return 0. Otherwise, return `min_length`.
        -   **Time Complexity (T.C.):** O(N). The `right` pointer traverses the array once. The `left` pointer also traverses the array at most once. Each element is added to `window_sum` once and subtracted from `window_sum` once. Thus, operations are proportional to N.
        -   **Space Complexity (S.C.):** O(1). Only a few constant extra variables are used.

    3.  **Prefix Sum + Binary Search (O(N log N) Solution - Follow Up):**
        -   **Idea:** This approach uses prefix sums to quickly calculate subarray sums and then binary search to find the minimum length.
        -   **Prefix Sums:** Create an array `prefix_sums` where `prefix_sums[k]` stores the sum of `nums[0...k-1]`. `prefix_sums[0]` is 0. The sum of a subarray `nums[i...j]` is `prefix_sums[j+1] - prefix_sums[i]`.
        -   **Binary Search:** For each possible starting index `i`, we want to find the smallest `j` such that `prefix_sums[j+1] - prefix_sums[i] >= target`. This can be rewritten as `prefix_sums[j+1] >= target + prefix_sums[i]`. Since `nums` contains positive integers, `prefix_sums` is a monotonically increasing array. We can use binary search on `prefix_sums` to find the smallest `prefix_sums[j+1]` that meets this condition.
        -   **Algorithm:**
            1.  Create `prefix_sums` array of size `n+1`. `prefix_sums[0] = 0`.
            2.  Populate `prefix_sums`: For `k` from 0 to `n-1`, `prefix_sums[k+1] = prefix_sums[k] + nums[k]`.
            3.  Initialize `min_length = float('inf')`.
            4.  Iterate `i` from 0 to `n-1` (representing `prefix_sums[i]`, the sum up to `nums[i-1]`):
                a.  We are looking for a `prefix_sums[j_plus_1]` such that `prefix_sums[j_plus_1] >= target + prefix_sums[i]`.
                b.  Use `bisect_left` (from Python's `bisect` module) to find the insertion point for `target + prefix_sums[i]` in the `prefix_sums` array. We search in the range `[i+1, n]` of `prefix_sums` to ensure `j_plus_1 > i` (i.e., the subarray is non-empty and has distinct start/end).
                c.  `search_value = target + prefix_sums[i]`.
                d.  `idx = bisect.bisect_left(prefix_sums, search_value, lo=i+1)` (Search from `i+1` to ensure subarray has at least one element).
                e.  If `idx < len(prefix_sums)` (meaning a valid `j+1` was found):
                    -   The length of the subarray is `idx - i`.
                    -   Update `min_length = min(min_length, idx - i)`.
            5.  If `min_length` is still `float('inf')`, return 0. Otherwise, return `min_length`.
        -   **Time Complexity (T.C.):** O(N log N). Building prefix sums is O(N). The loop runs N times, and each iteration performs a binary search on the `prefix_sums` array (which has up to N elements), taking O(log N) time.
        -   **Space Complexity (S.C.):** O(N) for the `prefix_sums` array.
    """

    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        Solution using the Sliding Window technique (Optimal O(N)).
        """
        n = len(nums)
        min_length = float('inf')
        window_sum = 0
        left = 0

        for right in range(n):
            window_sum += nums[right]

            # While the window sum is greater than or equal to the target,
            # we have a valid subarray. Try to shrink it from the left.
            while window_sum >= target:
                # Update the minimum length found so far
                min_length = min(min_length, right - left + 1)
                
                # Shrink the window from the left by removing nums[left]
                window_sum -= nums[left]
                left += 1
        
        # If min_length is still infinity, it means no such subarray was found.
        return min_length if min_length != float('inf') else 0

    def minSubArrayLen_ONlogN(self, target: int, nums: List[int]) -> int:
        """
        Solution using Prefix Sums and Binary Search (O(N log N)).
        """
        n = len(nums)
        min_length = float('inf')
        
        # Create a prefix sum array. prefix_sums[k] = sum(nums[0]...nums[k-1])
        # prefix_sums[0] = 0 (sum of empty prefix)
        prefix_sums = [0] * (n + 1)
        for i in range(n):
            prefix_sums[i+1] = prefix_sums[i] + nums[i]
            
        # For each possible starting index i of a subarray (corresponding to prefix_sums[i])
        for i in range(n + 1): # Iterate through all possible start points of prefix_sums
            # We are looking for prefix_sums[j_plus_1] such that:
            # prefix_sums[j_plus_1] - prefix_sums[i] >= target
            # => prefix_sums[j_plus_1] >= target + prefix_sums[i]
            
            # The value we are searching for in prefix_sums
            search_value = target + prefix_sums[i]
            
            # Use binary search (bisect_left) to find the smallest index 'idx'
            # in prefix_sums such that prefix_sums[idx] >= search_value.
            # We search from index i+1 to ensure the subarray is non-empty.
            idx = bisect.bisect_left(prefix_sums, search_value, lo=i+1)
            
            # If a valid index 'idx' is found within the bounds of prefix_sums
            if idx < len(prefix_sums):
                # The length of the subarray is (idx - i)
                # (since prefix_sums[idx] corresponds to sum up to index idx-1,
                # and prefix_sums[i] corresponds to sum up to index i-1)
                min_length = min(min_length, idx - i)
                
        return min_length if min_length != float('inf') else 0

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ({"target": 7, "nums": [2,3,1,2,4,3]}, 2), # Example 1
        ({"target": 4, "nums": [1,4,4]}, 1),       # Example 2
        ({"target": 11, "nums": [1,1,1,1,1,1,1,1]}, 0), # Example 3
        ({"target": 100, "nums": []}, 0),          # Empty array
        ({"target": 15, "nums": [1,2,3,4,5]}, 5),  # [1,2,3,4,5] sum 15, length 5
        ({"target": 15, "nums": [5,1,3,5,10,7,4,9,2,8]}, 2), # [10,7] sum 17, length 2, [7,4,9,2,8] sum 30 length 5 etc.
                                                            # [5,10] = 15, len 2.
                                                            # [7,4,9,2,8] sums to 30.
        ({"target": 20, "nums": [1,2,3,4,5,6,7,8,9,10]}, 3), # [7,8,9] = 24. [6,7,8] = 21. Smallest is [6,7,8] len 3.
        ({"target": 1, "nums": [1]}, 1), # Single element target
        ({"target": 5, "nums": [1,1,1,1,1]}, 5),
        ({"target": 5, "nums": [10]}, 1), # Single element > target
    ]

    print("--- O(N) Sliding Window Solution ---")
    for inputs, expected_output in test_cases:
        target = inputs["target"]
        nums = inputs["nums"]
        
        result = solution.minSubArrayLen(target, list(nums)) # Pass a copy of the list
        
        print(f"Input: target={target}, nums={nums}")
        print(f"Output: {result}")
        print(f"Expected: {expected_output}")
        print(f"Status: {'Pass' if result == expected_output else 'Fail'}")
        print("-" * 30)

    print("\n--- O(N log N) Prefix Sum + Binary Search Solution ---")
    for inputs, expected_output in test_cases:
        target = inputs["target"]
        nums = inputs["nums"]
        
        result_nlogn = solution.minSubArrayLen_ONlogN(target, list(nums)) # Pass a copy of the list
        
        print(f"Input: target={target}, nums={nums}")
        print(f"Output (O(N log N)): {result_nlogn}")
        print(f"Expected: {expected_output}")
        print(f"Status: {'Pass' if result_nlogn == expected_output else 'Fail'}")
        print("-" * 30)