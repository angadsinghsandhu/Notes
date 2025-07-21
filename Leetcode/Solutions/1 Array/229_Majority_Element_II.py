# File: Leetcode/Solutions/Array/229_Majority_Element_II.py
"""
Problem Number: 229
Problem Name: Majority Element II
Difficulty: Medium
Tags: Array, Hash Table, Sorting, Counting
Company (Frequency): Not explicitly stated, but frequently asked in interviews due to Boyer-Moore adaptation.
Leetcode Link: <https://leetcode.com/problems/majority-element-ii/description/>

DESCRIPTION

Given an integer array of size `n`, find all elements that appear more than `⌊ n/3 ⌋` times.

---

#### Example 1:

Input:
nums = [3,2,3]

Output:
[3]

---

#### Example 2:

Input:
nums = [1]

Output:
[1]

---

#### Example 3:

Input:
nums = [1,2]

Output:
[1,2]

---

#### Constraints:

- 1 <= nums.length <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9

---

#### Follow up:

Could you solve the problem in linear time and in O(1) space?
"""
from typing import List
import collections

class Solution:
    """
    Thought Process:

    The problem asks us to find all elements that appear more than `⌊ n / 3 ⌋` times in an array of size `n`.
    Unlike "Majority Element I" (where elements appeared more than `⌊ n / 2 ⌋` times and there was only one such element),
    here we can have at most two such majority elements.
    Why at most two?
    If there were three distinct elements (x, y, z) each appearing more than `n/3` times:
    count(x) > n/3
    count(y) > n/3
    count(z) > n/3
    Then, count(x) + count(y) + count(z) > n/3 + n/3 + n/3 = n.
    But the total number of elements is exactly `n`. This is a contradiction.
    Therefore, there can be at most two elements that appear more than `⌊ n / 3 ⌋` times.

    This crucial observation guides the optimal O(1) space solution.

    Several approaches can be used:

    1.  **Hash Map / Dictionary:**
        - This is the most straightforward approach.
        - **Approach:**
            1. Use `collections.Counter` or a manual dictionary to store the frequency of each element in `nums`.
            2. Iterate through the items (element, count) in the frequency map.
            3. If an element's count is greater than `n // 3`, add it to a result list.
            4. Return the result list.
        - **T.C.:** O(N) - One pass to build the frequency map. Then, iterating through at most N unique elements.
        - **S.C.:** O(N) - In the worst case, all elements are unique, requiring space for N key-value pairs in the hash map. This does not meet the O(1) space follow-up.

    2.  **Sorting:**
        - **Approach:**
            1. Sort the array `nums`.
            2. Iterate through the sorted array, counting consecutive occurrences of each number.
            3. If a number's count exceeds `n // 3`, add it to the result list.
            4. Handle edge cases for the last element.
        - **T.C.:** O(N log N) - Dominated by the sorting step.
        - **S.C.:** O(1) - If sorting is done in-place (like Python's `list.sort()`). This meets the space requirement but not the linear time requirement.

    3.  **Modified Boyer-Moore Voting Algorithm (Optimal for Follow-up):**
        - This algorithm is a generalization of the Boyer-Moore algorithm for finding elements appearing `> n/k` times. For `k=3`, we need to find elements appearing `> n/3` times, so we use `k-1 = 2` candidates.
        - **Approach:**
            1.  **First Pass (Candidate Selection):**
                - Initialize two candidates (`candidate1`, `candidate2`) and their counts (`count1`, `count2`) to 0.
                - Iterate through each `num` in `nums`:
                    - If `num` matches `candidate1`, increment `count1`.
                    - Else if `num` matches `candidate2`, increment `count2`.
                    - Else if `count1` is 0, set `candidate1 = num` and `count1 = 1`.
                    - Else if `count2` is 0, set `candidate2 = num` and `count2 = 1`.
                    - Else (if `num` is different from both candidates AND both `count1` and `count2` are non-zero), decrement both `count1` and `count2`. This "cancels out" `num` with one instance of each candidate.
            2.  **Second Pass (Verification):**
                - The candidates from the first pass are *potential* majority elements. They are not guaranteed to be actual majority elements (e.g., `[1,2,3,4,5,6]` would give candidates but no actual majority).
                - Reset `count1 = 0`, `count2 = 0`.
                - Iterate through `nums` again:
                    - If `num` is equal to `candidate1`, increment `count1`.
                    - If `num` is equal to `candidate2` AND `candidate1 != candidate2` (to avoid double-counting if candidates ended up being the same), increment `count2`.
            3.  **Result Construction:**
                - Initialize an empty list `result`.
                - If `count1 > n // 3`, add `candidate1` to `result`.
                - If `candidate2` is not `None` (meaning it was assigned) and `count2 > n // 3` AND `candidate1 != candidate2` (important to prevent duplicates if for some reason both candidates ended up being the same value, though the logic generally keeps them distinct if possible), add `candidate2` to `result`.
                - A simpler way to handle `candidate1 != candidate2` is to put potential candidates into a `set` first, then verify, then convert to list. Or just append `candidate1` if it meets criteria, then append `candidate2` *only if it's different from candidate1* and meets criteria.

        - **T.C.:** O(N) - Two passes over the array.
        - **S.C.:** O(1) - Only a few constant extra variables are used.
    """

    def majorityElement_hash_map(self, nums: List[int]) -> List[int]:
        """
        Approach 1: Using a Hash Map (Dictionary) to count frequencies.

        T.C.: O(N)
        S.C.: O(N)
        """
        n = len(nums)
        threshold = n // 3
        counts = collections.Counter(nums)
        result = []

        for num, count in counts.items():
            if count > threshold:
                result.append(num)
        return result

    def majorityElement_boyer_moore(self, nums: List[int]) -> List[int]:
        """
        Approach 2: Modified Boyer-Moore Voting Algorithm.
        This algorithm leverages the fact that there can be at most two majority elements
        (those appearing more than n/3 times).

        T.C.: O(N)
        S.C.: O(1)
        """
        if not nums:
            return []

        candidate1, candidate2 = None, None
        count1, count2 = 0, 0
        n = len(nums)
        threshold = n // 3

        # First pass: Find potential candidates
        for num in nums:
            if num == candidate1:
                count1 += 1
            elif num == candidate2:
                count2 += 1
            elif count1 == 0:
                candidate1 = num
                count1 = 1
            elif count2 == 0:
                candidate2 = num
                count2 = 1
            else:
                # If current num is different from both candidates, and both counts are > 0,
                # decrement both counts. This cancels them out.
                count1 -= 1
                count2 -= 1
        
        # Second pass: Verify the counts of the potential candidates
        count1, count2 = 0, 0 # Reset counts for verification
        for num in nums:
            if num == candidate1:
                count1 += 1
            # Important: Ensure candidate2 is not the same as candidate1 before incrementing
            # This handles cases where candidate1 and candidate2 might end up being the same value
            # due to the decrementing logic, although the logic for selecting candidates tries to keep them distinct.
            # Using 'is not None' is defensive, as candidate2 might not have been assigned if array is small.
            elif candidate2 is not None and num == candidate2: 
                count2 += 1
        
        result = []
        # Check if candidate1 is a true majority element
        if count1 > threshold:
            result.append(candidate1)
        
        # Check if candidate2 is a true majority element AND is distinct from candidate1
        if candidate2 is not None and count2 > threshold and candidate1 != candidate2:
            result.append(candidate2)
            
        return result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ([3,2,3], [3]),
        ([1], [1]),
        ([1,2], [1,2]),
        ([1,1,1,3,3,2,2,2], [1,2]),
        ([1,2,3,4,5], []), # n=5, threshold=1.66 -> need count > 1 (i.e. >= 2). No element appears >= 2 times.
        ([1,1,2,3,4], [1]), # n=5, threshold=1.66 -> need count > 1. 1 appears 2 times.
        ([2,2,1,3,1,1,3,1], [1]), # n=8, threshold=2.66 -> need count > 2 (i.e. >=3). 1 appears 5 times.
        ([8,8,7,7,7], [7,8]), # n=5, threshold=1.66 -> need count > 1. 7 appears 3, 8 appears 2.
        ([0,0,0], [0]),
        ([1,2,3], []), # n=3, threshold=1. Need count > 1. No element appears > 1.
    ]

    print("--- Testing majorityElement_hash_map ---")
    for nums, expected in test_cases:
        result = solution.majorityElement_hash_map(list(nums))
        # Sort result for consistent comparison, as order doesn't matter
        result.sort() 
        expected.sort()
        print(f"Input: {nums}, Output: {result}, Expected: {expected} -> {'Pass' if result == expected else 'Fail'}")
    print("-" * 40)

    print("\n--- Testing majorityElement_boyer_moore ---")
    for nums, expected in test_cases:
        result = solution.majorityElement_boyer_moore(list(nums))
        # Sort result for consistent comparison
        result.sort()
        expected.sort()
        print(f"Input: {nums}, Output: {result}, Expected: {expected} -> {'Pass' if result == expected else 'Fail'}")
    print("-" * 40)