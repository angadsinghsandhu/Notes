# File: Leetcode/Solutions/LeetCode/344_Reverse_String.py

"""
Problem Number: 344
Problem Name: Reverse String
Difficulty: Easy
Tags: Two Pointers, String
Company (Frequency): (premium)
Leetcode Link: https://leetcode.com/problems/reverse-string/

DESCRIPTION

Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.

---

#### Example 1:

Input:
s = ["h","e","l","l","o"]

Output:
["o","l","l","e","h"]

#### Example 2:

Input:
s = ["H","a","n","n","a","h"]

Output:
["h","a","n","n","a","H"]

#### Constraints:

- $1 \leq s.length \leq 10^5$
- s\[i] is a printable ASCII character.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - Brute Force: allocate extra space to reverse, then copy back.
    - Optimized: use two-pointer technique to swap characters in-place.
    """

    def brute_force(self, s: List[str]) -> None:
        """
        Approach:
        - Use Python slicing to reverse into a new list, then overwrite.
        
        T.C.: O(n)
        S.C.: O(n) extra (due to new list)
        """
        reversed_s = s[::-1]
        for i in range(len(s)):
            s[i] = reversed_s[i]

    def optimized(self, s: List[str]) -> None:
        """
        Approach:
        - Initialize two pointers at the ends of the array.
        - Swap characters and move pointers towards center.
        
        T.C.: O(n)
        S.C.: O(1) extra
        """
        left, right = 0, len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1


if __name__ == "__main__":
    solution = Solution()

# Example 1
s1 = ["h","e","l","l","o"]
solution.brute_force(s1)
print(s1)  # ["o","l","l","e","h"]

s2 = ["h","e","l","l","o"]
solution.optimized(s2)
print(s2)  # ["o","l","l","e","h"]

# Example 2
s3 = ["H","a","n","n","a","h"]
solution.brute_force(s3)
print(s3)  # ["h","a","n","n","a","H"]

s4 = ["H","a","n","n","a","h"]
solution.optimized(s4)
print(s4)  # ["h","a","n","n","a","H"]
