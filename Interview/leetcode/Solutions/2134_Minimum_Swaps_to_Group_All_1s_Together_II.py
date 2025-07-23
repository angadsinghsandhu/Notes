# File: Leetcode/Solutions/Array/2134_Minimum_Swaps_to_Group_All_1s_Together_II.py
"""
Problem Number: 2134
Problem Name: Minimum Swaps to Group All 1's Together II
Difficulty: Medium
Tags: Array, Sliding Window
Company (Frequency): Tests understanding of circular arrays and fixed-size sliding windows.
Leetcode Link: <https://leetcode.com/problems/minimum-swaps-to-group-all-1s-together-ii/description/>

DESCRIPTION

A `swap` is defined as taking two distinct positions in an array and swapping the values in them.
A `circular` array is defined as an array where we consider the first element and the last element to be adjacent.
Given a `binary` circular array `nums`, return the minimum number of swaps required to group all 1's present in the array together at `any` location.

---

#### Example 1:

Input:
nums = [0,1,0,1,1,0,0]

Output:
1

Explanation:
Here are a few of the ways to group all the 1's together:
[0,0,1,1,1,0,0] using 1 swap.
[0,1,1,1,0,0,0] using 1 swap.
[1,1,0,0,0,0,1] using 2 swaps (using the circular property of the array).
There is no way to group all 1's together with 0 swaps.
Thus, the minimum number of swaps required is 1.

---

#### Example 2:

Input:
nums = [0,1,1,1,0,0,1,1,0]

Output:
2

Explanation:
Here are a few of the ways to group all the 1's together:
[1,1,1,0,0,0,0,1,1] using 2 swaps (using the circular property of the array).
[1,1,1,1,1,0,0,0,0] using 2 swaps.
There is no way to group all 1's together with 0 or 1 swaps.
Thus, the minimum number of swaps required is 2.

---

#### Example 3:

Input:
nums = [1,1,0,0,1]

Output:
0

Explanation:
All the 1's are already grouped together due to the circular property of the array.
Thus, the minimum number of swaps required is 0.

---

#### Constraints:

- 1 <= nums.length <= 10^5
- nums[i] is either 0 or 1.
"""
from typing import List

class Solution:
    """
    Thought Process for Minimum Swaps to Group All 1's Together II:

    The problem asks for the minimum swaps to group all 1's in a *circular* binary array.

    Key Insights:

    1.  **Fixed Window Size:** If we want to group all the 1's together, they will occupy a contiguous subarray. The length of this subarray must be exactly equal to the total count of 1's in the entire array. Let's call this `total_ones`.

    2.  **Minimum Swaps within a Window:** Consider a window of size `total_ones`. If this window contains `k` ones, it means it contains `total_ones - k` zeros. To make this window contain *only* ones, we need to swap these `total_ones - k` zeros with `total_ones - k` ones that are *outside* this window. Each such swap effectively brings a '1' into the window and moves a '0' out. Therefore, the number of swaps required for a particular window is `(window_size) - (number_of_ones_in_window)`. Since `window_size` is fixed at `total_ones`, this simplifies to `total_ones - (number_of_ones_in_window)`.

    3.  **Optimization Goal:** To *minimize* the number of swaps (`total_ones - number_of_ones_in_window`), we need to *maximize* the `number_of_ones_in_window`. Our goal is to find a window of size `total_ones` that contains the maximum possible count of 1's.

    4.  **Circular Array:** The array is circular. This means a window can wrap around from the end of the array to the beginning. For example, if `nums = [0,1,0,1,1,0,0]` and `total_ones = 3`, a valid window could be `[1,1,0]` starting at index 3 and wrapping around, or `[1,0,0]` starting at index 5 and wrapping to index 0.

    Approach: Sliding Window with Circularity Handling

    We will use a fixed-size sliding window. The size of the window will be `total_ones`. We need to iterate this window over all possible `n` starting positions in the circular array and find the one that maximizes the count of 1's.

    Algorithm:

    1.  Get the length of the array, `n = len(nums)`.
    2.  Calculate `total_ones = sum(nums)`. This is our fixed window size.
    3.  **Edge Cases:**
        -   If `total_ones` is 0 (no ones in the array), or `total_ones` is `n` (all ones in the array), then all ones are already grouped. Return 0 swaps.
    4.  Initialize `current_ones_in_window = 0`. This will track the count of ones in the current sliding window.
    5.  Initialize `max_ones_in_window = 0`. This will store the maximum number of ones found in any window of size `total_ones`.

    6.  **Initialize the first window:**
        -   Iterate `i` from 0 to `total_ones - 1`.
        -   `current_ones_in_window += nums[i]`.
        -   Set `max_ones_in_window = current_ones_in_window`. This is the count of ones in the initial window.

    7.  **Slide the window:**
        -   Now, we need to slide the window `n - 1` times to cover all other starting positions in the circular array.
        -   For each step, an element leaves the window from the left and a new element enters from the right.
        -   We use the modulo operator (`% n`) to handle the circularity for the element entering the window from the right.
        -   Iterate `i` from 1 to `n - 1` (this `i` represents the starting index of the new window):
            -   The element leaving the window is `nums[i - 1]`. Subtract its value from `current_ones_in_window`.
            -   The element entering the window is `nums[(i + total_ones - 1) % n]`. Add its value to `current_ones_in_window`.
            -   Update `max_ones_in_window = max(max_ones_in_window, current_ones_in_window)`.

    8.  Finally, the minimum number of swaps required is `total_ones - max_ones_in_window`. This is because `max_ones_in_window` is the maximum number of 1's we can *keep* in a window of size `total_ones`. The remaining `total_ones - max_ones_in_window` elements in that optimal window *must* be zeros, which need to be swapped out with ones from outside.

    Complexity Analysis:

    -   **Time Complexity (T.C.):** O(N).
        -   Calculating `total_ones` takes O(N) time.
        -   Initializing the first window takes O(`total_ones`) time.
        -   Sliding the window takes O(N - 1) iterations. Each iteration involves constant time operations (add, subtract, modulo, max).
        -   Overall, the complexity is dominated by iterating through the array a constant number of times, resulting in O(N).
    -   **Space Complexity (S.C.):** O(1).
        -   Only a few constant variables are used to store counts and pointers. No auxiliary data structures proportional to `n` are created.
    """

    def minSwaps(self, nums: List[int]) -> int:
        n = len(nums)

        # 1. Count the total number of 1's. This will be our fixed window size.
        total_ones = sum(nums)

        # 2. Handle edge cases where no swaps are needed:
        #    If there are no ones or all elements are ones, they are already grouped.
        if total_ones == 0 or total_ones == n:
            return 0

        # The size of our sliding window is `total_ones`.
        window_size = total_ones

        # 3. Initialize current_ones_in_window and max_ones_in_window.
        current_ones_in_window = 0
        max_ones_in_window = 0

        # 4. Calculate the number of ones in the initial window (from index 0 to window_size - 1).
        for i in range(window_size):
            current_ones_in_window += nums[i]
        
        # This is our initial maximum
        max_ones_in_window = current_ones_in_window

        # 5. Slide the window across the circular array.
        #    The loop variable `i` represents the potential starting index of the window.
        #    We start `i` from 1 because we've already processed the window starting at 0.
        #    We iterate `n - 1` times to cover all `n` unique starting positions in a circular manner.
        for i in range(1, n):
            # Element leaving the window from the left: nums[i-1]
            current_ones_in_window -= nums[i - 1]
            
            # Element entering the window from the right: nums[(i + window_size - 1) % n]
            # The `% n` handles the circularity, wrapping around to the beginning of the array.
            current_ones_in_window += nums[(i + window_size - 1) % n]
            
            # Update the maximum number of ones found in any window.
            max_ones_in_window = max(max_ones_in_window, current_ones_in_window)

        # 6. The minimum number of swaps is total_ones - max_ones_in_window.
        #    This represents the number of zeros in the optimal window,
        #    which need to be swapped out with ones from outside the window.
        return total_ones - max_ones_in_window

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ({"nums": [0,1,0,1,1,0,0]}, 1), # Example 1
        ({"nums": [0,1,1,1,0,0,1,1,0]}, 2), # Example 2
        ({"nums": [1,1,0,0,1]}, 0), # Example 3
        ({"nums": [1,0,1,0,1]}, 1), # total_ones = 3. window size 3. [1,0,1], [0,1,0], [1,0,1]
                                    # initial [1,0,1] -> ones = 2, swaps = 1
                                    # [0,1,0,1,1] => [1,0,1], [0,1,0], [1,0,1], [0,1,1], [1,1,0]
                                    # [1,0,1] -> 2 ones
                                    # [0,1,1] -> 2 ones
                                    # [1,1,0] -> 2 ones
                                    # max_ones = 2. Swaps = 3 - 2 = 1.
        ({"nums": [1,1,1,1]}, 0), # All ones
        ({"nums": [0,0,0,0]}, 0), # No ones
        ({"nums": [0,1,1,0,1,1,0,1,1,1]}, 1), # total_ones = 8, n = 10. window size 8.
                                                # Need to find 8 contiguous spots with max 1s.
                                                # [1,1,0,1,1,1,1,0] => 6 ones
                                                # [1,1,1,1,1,1,1,0] => 7 ones
                                                # [0,1,1,1,0,1,1,1,1,0]
                                                # [0,1,1,1,0,0,1,1,0]
                                                # Let's verify manually: [0,1,1,0,1,1,0,1,1,1] (8 ones)
                                                # Maximize 1s in a window of size 8:
                                                # [0,1,1,0,1,1,0,1] (5 ones)
                                                # [1,1,0,1,1,0,1,1] (6 ones)
                                                # [1,0,1,1,0,1,1,1] (6 ones)
                                                # [0,1,1,0,1,1,1,0] (6 ones)
                                                # [1,1,0,1,1,1,0,1] (6 ones)
                                                # [1,0,1,1,1,0,1,1] (6 ones)
                                                # [0,1,1,1,0,1,1,1] (6 ones)
                                                # [1,1,1,0,1,1,1,0] (6 ones)
                                                # [1,1,0,1,1,1,0,1] (6 ones)
                                                # [1,0,1,1,1,0,1,1] (6 ones)
                                                # Looks like max_ones is 6. So swaps = 8 - 6 = 2.
                                                # Wait, example answer is 1. My manual trace is possibly wrong or my logic.
                                                # Let's re-verify example 2: [0,1,1,1,0,0,1,1,0]. total_ones = 6. n = 9. window_size = 6.
                                                # [0,1,1,1,0,0] -> 3 ones. swaps = 6-3=3
                                                # [1,1,1,0,0,1] -> 4 ones. swaps = 6-4=2
                                                # [1,1,0,0,1,1] -> 4 ones. swaps = 6-4=2
                                                # [1,0,0,1,1,0] -> 3 ones. swaps = 6-3=3
                                                # [0,0,1,1,0,1] -> 3 ones. swaps = 6-3=3
                                                # [0,1,1,0,1,1] -> 4 ones. swaps = 6-4=2
                                                # Max ones in window is 4. Min swaps is 6 - 4 = 2. This matches example 2.

                                                # For [0,1,1,0,1,1,0,1,1,1] (total 8 ones)
                                                # My code gets 1. Let's trace it.
                                                # nums = [0,1,1,0,1,1,0,1,1,1]
                                                # n = 10, total_ones = 8, window_size = 8
                                                # initial window [0,1,1,0,1,1,0,1] (idx 0-7) => current_ones = 5. max_ones = 5.
                                                # i = 1: remove nums[0]=0, add nums[(1+8-1)%10] = nums[8%10]=nums[8]=1. current_ones = 5 - 0 + 1 = 6. max_ones = 6. Window: [1,1,0,1,1,0,1,1] (idx 1-8)
                                                # i = 2: remove nums[1]=1, add nums[(2+8-1)%10] = nums[9%10]=nums[9]=1. current_ones = 6 - 1 + 1 = 6. max_ones = 6. Window: [1,0,1,1,0,1,1,1] (idx 2-9)
                                                # i = 3: remove nums[2]=1, add nums[(3+8-1)%10] = nums[10%10]=nums[0]=0. current_ones = 6 - 1 + 0 = 5. max_ones = 6. Window: [0,1,1,0,1,1,1,0] (idx 3-0)
                                                # i = 4: remove nums[3]=0, add nums[(4+8-1)%10] = nums[11%10]=nums[1]=1. current_ones = 5 - 0 + 1 = 6. max_ones = 6. Window: [1,1,0,1,1,1,0,1] (idx 4-1)
                                                # i = 5: remove nums[4]=1, add nums[(5+8-1)%10] = nums[12%10]=nums[2]=1. current_ones = 6 - 1 + 1 = 6. max_ones = 6. Window: [1,0,1,1,1,0,1,1] (idx 5-2)
                                                # i = 6: remove nums[5]=1, add nums[(6+8-1)%10] = nums[13%10]=nums[3]=0. current_ones = 6 - 1 + 0 = 5. max_ones = 6. Window: [0,1,1,1,0,1,1,1] (idx 6-3)
                                                # i = 7: remove nums[6]=0, add nums[(7+8-1)%10] = nums[14%10]=nums[4]=1. current_ones = 5 - 0 + 1 = 6. max_ones = 6. Window: [1,1,1,0,1,1,1,0] (idx 7-4)
                                                # i = 8: remove nums[7]=1, add nums[(8+8-1)%10] = nums[15%10]=nums[5]=1. current_ones = 6 - 1 + 1 = 6. max_ones = 6. Window: [1,1,0,1,1,1,0,1] (idx 8-5)
                                                # i = 9: remove nums[8]=1, add nums[(9+8-1)%10] = nums[16%10]=nums[6]=0. current_ones = 6 - 1 + 0 = 5. max_ones = 6. Window: [1,0,1,1,1,0,1,1] (idx 9-6)
                                                # End loop. max_ones = 6. swaps = 8 - 6 = 2.
                                                # My code output is 2. The custom test case `[0,1,1,0,1,1,0,1,1,1]` and expected `1` must be incorrect. It should be 2. Let's fix that test case.

        ({"nums": [0,1,1,0,1,1,0,1,1,1]}, 2), # Corrected expected output to 2.

    ]

    for inputs, expected_output in test_cases:
        nums = inputs["nums"]
        
        result = solution.minSwaps(list(nums)) # Pass a copy of the list
        
        print(f"Input: nums={nums}")
        print(f"Output: {result}")
        print(f"Expected: {expected_output}")
        print(f"Status: {'Pass' if result == expected_output else 'Fail'}")
        print("-" * 30)