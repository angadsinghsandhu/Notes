# File: Leetcode/Solutions/Amazon/4_Median_of_Two_Sorted_Arrays.py

"""
Problem Number: 4
Problem Name: Median of Two Sorted Arrays
Difficulty: Hard
Tags: Array, Binary Search, Divide and Conquer
Company (Frequency): Amazon (95)
Leetcode Link: <https://leetcode.com/problems/median-of-two-sorted-arrays/description/>

DESCRIPTION

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

---

#### Example 1:
**Input:**
```plaintext
nums1 = [1, 3], nums2 = [2]
```

**Output:**
```plaintext
2.00000
```

**Explanation:**  
Merged array = [1, 2, 3] and median is 2.

#### Example 2:
**Input:**
```plaintext
nums1 = [1, 2], nums2 = [3, 4]
```

**Output:**
```plaintext
2.50000
```

**Explanation:**  
Merged array = [1, 2, 3, 4] and median is (2 + 3) / 2 = 2.5.

#### Constraints:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves finding the median of two sorted arrays efficiently.
    - A brute force solution would merge the two arrays and find the median, but it is inefficient (O(m+n)).
    - An optimized solution uses binary search to achieve O(log(min(m, n))) time complexity.

    Input:
        nums1: List[int] - The first sorted array.
        nums2: List[int] - The second sorted array.

    Output:
        float - The median of the two sorted arrays.
    """

    def brute_force_solution(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Approach:
        - Merge the two sorted arrays into one sorted array.
        - Find the median of the merged array.

        T.C.: O(m + n)
        S.C.: O(m + n)
        """
        merged = []
        i, j = 0, 0

        # Merge the two arrays
        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                merged.append(nums1[i])
                i += 1
            else:
                merged.append(nums2[j])
                j += 1

        # Append remaining elements from nums1
        while i < len(nums1):
            merged.append(nums1[i])
            i += 1

        # Append remaining elements from nums2
        while j < len(nums2):
            merged.append(nums2[j])
            j += 1

        # Find the median
        n = len(merged)
        if n % 2 == 1:
            return float(merged[n // 2])
        else:
            return (merged[n // 2 - 1] + merged[n // 2]) / 2.0

    def optimized_solution(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Approach:
        - Use binary search on the smaller array to partition both arrays such that the left half contains the median.
        - Ensure the partition is correct by checking the boundary elements.
        - Calculate the median based on the partition.

        T.C.: O(log(min(m, n)))
        S.C.: O(1)
        """
        # Ensure nums1 is the smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        low, high = 0, m

        while low <= high:
            partition1 = (low + high) // 2  # Partition for nums1
            partition2 = (m + n + 1) // 2 - partition1  # Partition for nums2

            # Handle edge cases for partition1 and partition2
            max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
            min_right1 = float('inf') if partition1 == m else nums1[partition1]

            max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
            min_right2 = float('inf') if partition2 == n else nums2[partition2]

            # Check if the partition is correct
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                # Calculate the median
                if (m + n) % 2 == 1:
                    return float(max(max_left1, max_left2))
                else:
                    return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            elif max_left1 > min_right2:
                high = partition1 - 1
            else:
                low = partition1 + 1

        raise ValueError("Input arrays are not sorted or invalid.")

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.brute_force_solution([1, 3], [2]))  # Output: 2.0
    print(solution.optimized_solution([1, 2], [3, 4]))  # Output: 2.5
    print(solution.optimized_solution([0, 0], [0, 0]))  # Output: 0.0
    print(solution.optimized_solution([], [1]))  # Output: 1.0
    print(solution.optimized_solution([2], []))  # Output: 2.0