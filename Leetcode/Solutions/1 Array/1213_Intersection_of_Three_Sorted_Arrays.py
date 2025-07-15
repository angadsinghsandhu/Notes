# File: Leetcode/Solutions/Facebook/1213_Intersection_of_Three_Sorted_Arrays.py

"""
Problem Number: 1213
Problem Name: Intersection of Three Sorted Arrays
Difficulty: Easy
Tags: Array, Three Pointers (Implied by nature of sorted arrays)
Company (Frequency): Facebook, TripAdvisor
Leetcode Link: Not explicitly provided, but typically a premium question.

DESCRIPTION

Given three integer arrays `arr1`, `arr2`, and `arr3` sorted in strictly increasing order,
return a sorted array of only the integers that appeared in all three arrays.

---

#### Example 1:

Input:
arr1 = [1,2,3,4,5], arr2 = [1,2,5,7,9], arr3 = [1,3,4,5,8]

Output:
[1,5]

Explanation:
Only 1 and 5 appeared in the three arrays.

---

#### Constraints:

- 1 <= arr1.length, arr2.length, arr3.length <= 1000
- 1 <= arr1[i], arr2[i], arr3[i] <= 2000
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem asks us to find the common elements present in three strictly increasing sorted arrays.
    - Since all three arrays are sorted, a multi-pointer approach is highly efficient.
    - We can use three pointers, one for each array, and advance them based on comparisons.
    - If the elements at all three pointers are equal, it's a common element, so we add it to our result and advance all three pointers.
    - If the elements are not equal, we advance the pointer pointing to the smallest element. This is because a smaller element cannot possibly be in the other arrays if their current elements are larger (due to sorted nature).

    Input:
        arr1: List[int] - The first sorted integer array.
        arr2: List[int] - The second sorted integer array.
        arr3: List[int] - The third sorted integer array.

    Output:
        List[int] - A sorted array of integers appearing in all three input arrays.
    """

    def arraysIntersection(self, arr1: List[int], arr2: List[int], arr3: List[int]) -> List[int]:
        """
        Approach: Three Pointers
        - Initialize three pointers: `p1` for `arr1`, `p2` for `arr2`, and `p3` for `arr3`, all starting at index 0.
        - Initialize an empty list `result` to store the common elements.
        - Iterate while all three pointers are within the bounds of their respective arrays:
            - Get the current elements: `val1 = arr1[p1]`, `val2 = arr2[p2]`, `val3 = arr3[p3]`.
            - If `val1 == val2 == val3`:
                - This is a common element. Append `val1` to `result`.
                - Increment all three pointers: `p1 += 1`, `p2 += 1`, `p3 += 1`.
            - Else (if the values are not all equal):
                - Find the minimum among `val1`, `val2`, `val3`.
                - Increment only the pointer(s) corresponding to the minimum value(s). This ensures we try to move past the smallest element, seeking a potential match.
                - For example, if `val1` is the smallest, increment `p1`. If `val2` is the smallest, increment `p2`, and so on.
        - Return `result`.

        T.C.: O(n1 + n2 + n3) where n1, n2, n3 are lengths of arr1, arr2, arr3 respectively. In the worst case, each pointer traverses its entire array once.
        S.C.: O(min(n1, n2, n3)) in the worst case if all elements are common, but practically O(k) where k is the number of common elements.
        """
        p1, p2, p3 = 0, 0, 0
        result = []

        n1, n2, n3 = len(arr1), len(arr2), len(arr3)

        while p1 < n1 and p2 < n2 and p3 < n3:
            val1 = arr1[p1]
            val2 = arr2[p2]
            val3 = arr3[p3]

            if val1 == val2 and val2 == val3:
                # Found a common element
                result.append(val1)
                p1 += 1
                p2 += 1
                p3 += 1
            else:
                # Advance the pointer pointing to the smallest element
                min_val = min(val1, val2, val3)
                if val1 == min_val:
                    p1 += 1
                if val2 == min_val:
                    p2 += 1
                if val3 == min_val:
                    p3 += 1
        return result


# Run and print sample test cases

if __name__ == "__main__":
    solution = Solution()

    # Test Case 1
    arr1_1 = [1,2,3,4,5]
    arr2_1 = [1,2,5,7,9]
    arr3_1 = [1,3,4,5,8]
    expected1 = [1,5]

    result1 = solution.arraysIntersection(list(arr1_1), list(arr2_1), list(arr3_1))
    print(f"Input: arr1={arr1_1}, arr2={arr2_1}, arr3={arr3_1} -> Output: {result1} (Expected: {expected1})")
    print("-" * 20)

    # Additional Test Case: No common elements
    arr1_2 = [1,2,3]
    arr2_2 = [4,5,6]
    arr3_2 = [7,8,9]
    expected2 = []

    result2 = solution.arraysIntersection(list(arr1_2), list(arr2_2), list(arr3_2))
    print(f"Input: arr1={arr1_2}, arr2={arr2_2}, arr3={arr3_2} -> Output: {result2} (Expected: {expected2})")
    print("-" * 20)

    # Additional Test Case: Some common elements, but not all (e.g., in two but not three)
    arr1_3 = [1,2,3,10,11]
    arr2_3 = [2,3,4,10,12]
    arr3_3 = [3,4,5,10,13]
    expected3 = [3,10] # 2 is in arr1, arr2 but not arr3. 4 is in arr2, arr3 but not arr1.

    result3 = solution.arraysIntersection(list(arr1_3), list(arr2_3), list(arr3_3))
    print(f"Input: arr1={arr1_3}, arr2={arr2_3}, arr3={arr3_3} -> Output: {result3} (Expected: {expected3})")
    print("-" * 20)

    # Additional Test Case: Empty arrays (though constraints say length >= 1)
    # The current solution handles this gracefully as `p1 < n1` etc. will immediately be false.
    arr1_4 = [1]
    arr2_4 = [1]
    arr3_4 = [1]
    expected4 = [1]

    result4 = solution.arraysIntersection(list(arr1_4), list(arr2_4), list(arr3_4))
    print(f"Input: arr1={arr1_4}, arr2={arr2_4}, arr3={arr3_4} -> Output: {result4} (Expected: {expected4})")
    print("-" * 20)