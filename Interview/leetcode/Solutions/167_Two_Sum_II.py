# TODO

### **File:** `Leetcode/Solutions/167_Two_Sum_II_Input_Array_Is_Sorted.py`

"""
Problem Number: 167
Problem Name: Two Sum II - Input Array Is Sorted
Difficulty: Medium
Tags: Array, Two Pointers, Binary Search, Neetcode 150
Company (Frequency): Amazon, Facebook, Google, Microsoft
Leetcode Link: <https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/>

DESCRIPTION

Given a **1-indexed** array of integers `numbers` that is **already sorted** in non-decreasing order, find two numbers such that they add up to a specific `target`.

Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return the indices of the two numbers, `[index1, index2]`, as an integer array of length 2.

The tests are generated such that **there is exactly one solution**, and you **may not use the same element twice**.

Your solution must use only **constant extra space**.

---

#### Example 1:
**Input:**
```plaintext
numbers = [2,7,11,15], target = 9
```
**Output:**
```plaintext
[1,2]
```
**Explanation:**  
The sum of `2` and `7` is `9`. Therefore, `index1 = 1`, `index2 = 2`. We return `[1,2]`.

#### Example 2:
**Input:**
```plaintext
numbers = [2,3,4], target = 6
```
**Output:**
```plaintext
[1,3]
```
**Explanation:**  
The sum of `2` and `4` is `6`. Therefore, `index1 = 1`, `index2 = 3`. We return `[1,3]`.

#### Example 3:
**Input:**
```plaintext
numbers = [-1,0], target = -1
```
**Output:**
```plaintext
[1,2]
```
**Explanation:**  
The sum of `-1` and `0` is `-1`. Therefore, `index1 = 1`, `index2 = 2`. We return `[1,2]`.

#### Constraints:
- `2 <= numbers.length <= 3 * 10^4`
- `-1000 <= numbers[i] <= 1000`
- `numbers` is sorted in **non-decreasing order**.
- `-1000 <= target <= 1000`
- The tests are generated such that there is **exactly one solution**.
"""

class Solution:
    """
    Thought Process:
    - The array is sorted, allowing us to efficiently find the two numbers using the **two-pointer** approach.
    - Initialize two pointers:
        - `left` at the beginning of the array.
        - `right` at the end of the array.
    - Iterate while `left < right`:
        - If the sum of `numbers[left] + numbers[right]` equals the target, return the indices.
        - If the sum is smaller than the target, move `left` to the right to increase the sum.
        - If the sum is greater than the target, move `right` to the left to decrease the sum.
    - This method guarantees an `O(n)` solution while using **O(1) extra space**.

    Input:
        numbers: List[int] - The sorted array of integers.
        target: int - The required sum.

    Output:
        List[int] - The indices (1-based) of the two numbers that sum up to `target`.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        """
        Approach:
        - Use the **Two-Pointer** technique to find the sum efficiently.
        - Move the pointers towards each other based on the sum comparison.

        T.C.: O(n) - At most one full pass through the array.
        S.C.: O(1) - Only two integer variables used.
        """
        left, right = 0, len(numbers) - 1  # Initialize two pointers
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                return [left + 1, right + 1]  # Return 1-based indices
            
            if current_sum < target:
                left += 1  # Increase sum by moving left pointer
            else:
                right -= 1  # Decrease sum by moving right pointer

        return []  # This line will never be reached since a solution is guaranteed

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.twoSum([2,7,11,15], 9))  # Output: [1,2]
    print(solution.twoSum([2,3,4], 6))      # Output: [1,3]
    print(solution.twoSum([-1,0], -1))      # Output: [1,2]