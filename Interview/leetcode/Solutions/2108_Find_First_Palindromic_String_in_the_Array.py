# File: Leetcode/Solutions/Array/2108_Find_First_Palindromic_String_in_the_Array.py
"""
Problem Number: 2108
Problem Name: Find First Palindromic String in the Array
Difficulty: Easy
Tags: Array, Two Pointers, String
Company (Frequency): Common pattern for basic string manipulation and array iteration.
Leetcode Link: <https://leetcode.com/problems/find-first-palindromic-string-in-the-array/description/>

DESCRIPTION

Given an array of strings `words`, return the first palindromic string in the array. If there is no such string, return an empty string "".
A string is palindromic if it reads the same forward and backward.

---

#### Example 1:

Input:
words = ["abc","car","ada","racecar","cool"]

Output:
"ada"

Explanation:
The first string that is palindromic is "ada".
Note that "racecar" is also palindromic, but it is not the first.

---

#### Example 2:

Input:
words = ["notapalindrome","racecar"]

Output:
"racecar"

Explanation:
The first and only string that is palindromic is "racecar".

---

#### Example 3:

Input:
words = ["def","ghi"]

Output:
""

Explanation:
There are no palindromic strings, so the empty string is returned.

---

#### Constraints:

- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists only of lowercase English letters.
"""
from typing import List

class Solution:
    """
    Thought Process for Find First Palindromic String in the Array:

    The problem asks us to find the first string in a given array `words` that is a palindrome.
    If no palindromic string is found, we should return an empty string.
    A string is palindromic if it reads the same forwards and backward.

    Given the constraints:
    - `words.length` up to 100.
    - `words[i].length` up to 100.

    These constraints are quite small, meaning that even a straightforward approach will be efficient enough.

    Core Subproblem: How to check if a string is a palindrome?
    There are a couple of common ways to check for palindromes:

    1.  **String Reversal Comparison (Pythonic):**
        A string `s` is a palindrome if `s == s[::-1]`. This is concise in Python.
        -   **Time Complexity for check:** O(L), where L is the length of the string, due to string copying for reversal.
        -   **Space Complexity for check:** O(L) for the reversed string copy.

    2.  **Two Pointers:**
        Initialize two pointers, `left` at the beginning of the string and `right` at the end of the string.
        Iterate while `left < right`:
        -   If `s[left]` is not equal to `s[right]`, the string is not a palindrome. Return `False`.
        -   Move `left` one step to the right (`left += 1`).
        -   Move `right` one step to the left (`right -= 1`).
        If the loop completes, it means all corresponding characters matched, so the string is a palindrome. Return `True`.
        -   **Time Complexity for check:** O(L), as each pointer traverses at most half the string.
        -   **Space Complexity for check:** O(1), as no extra data structure proportional to string length is used.

    Overall Approach:

    The problem asks for the *first* palindromic string. This implies we should iterate through the `words` array in the given order and perform the palindrome check on each string. As soon as a palindrome is found, we can return it immediately without checking the rest of the array. If the loop completes without finding any palindrome, it means none exist, so we return an empty string.

    Detailed Algorithm:

    1. Define a helper function, say `_is_palindrome(s: str)`, that takes a string and returns `True` if it's a palindrome, `False` otherwise. (Using the two-pointer method for efficiency and clarity).
    2. Iterate through each `word` in the input `words` list.
    3. Inside the loop, call `_is_palindrome(word)`.
    4. If `_is_palindrome(word)` returns `True`, then this `word` is the first palindromic string. Return `word`.
    5. If the loop finishes (meaning no palindromic string was found), return an empty string `""`.

    Complexity Analysis of the overall solution:

    -   **Time Complexity (T.C.):** O(N * L) in the worst case.
        -   `N` is the number of strings in `words` (`words.length`).
        -   `L` is the maximum length of a string in `words` (`words[i].length`).
        -   In the worst case (e.g., the last string is a palindrome, or no palindrome exists), we iterate through all `N` strings. For each string, we perform a palindrome check which takes O(L) time.
        -   Given `N <= 100` and `L <= 100`, the maximum operations would be roughly `100 * 100 = 10,000`, which is very fast.
    -   **Space Complexity (S.C.):** O(1) (excluding input and output storage).
        -   If the two-pointer method is used for palindrome checking, no additional space proportional to string length is used.
        -   If Python's string slicing `[::-1]` is used, it might create a temporary string copy, leading to O(L) auxiliary space per check, but this temporary space is reused and doesn't accumulate significantly across the function call. For typical competitive programming context, this is often still considered O(1) auxiliary space.
    """

    def _is_palindrome(self, s: str) -> bool:
        """
        Helper function to check if a string is a palindrome using two pointers.
        T.C.: O(L) where L is the length of the string s.
        S.C.: O(1)
        """
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False  # Characters do not match, not a palindrome
            left += 1
            right -= 1
        return True  # All characters matched, it's a palindrome

    def findFirstPalindrome(self, words: List[str]) -> str:
        """
        Main function to find the first palindromic string in the array.
        """
        for word in words:
            if self._is_palindrome(word):
                return word  # Found the first palindrome, return it immediately
        
        return "" # No palindromic string found after checking all words

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        ({"words": ["abc","car","ada","racecar","cool"]}, "ada"), # Example 1
        ({"words": ["notapalindrome","racecar"]}, "racecar"), # Example 2
        ({"words": ["def","ghi"]}, ""), # Example 3
        ({"words": ["a"]}, "a"), # Single character string (is a palindrome)
        ({"words": ["ab", "ba"]}, "ba"), # "ba" is palindrome
        ({"words": ["level", "madam", "rotor"]}, "level"), # Multiple palindromes, return first
        ({"words": ["", "a", "aa"]}, ""), # Empty string is not a palindrome by problem context usually, but technically reads same.
                                            # LeetCode usually assumes non-empty strings or provides explicit rules.
                                            # Current constraints say 1 <= words[i].length, so no empty strings as input.
        ({"words": ["race", "car", "level"]}, "level")
    ]

    for inputs, expected_output in test_cases:
        words = inputs["words"]
        
        result = solution.findFirstPalindrome(list(words)) # Pass a copy of the list
        
        print(f"Input: words={words}")
        print(f"Output: '{result}'")
        print(f"Expected: '{expected_output}'")
        print(f"Status: {'Pass' if result == expected_output else 'Fail'}")
        print("-" * 30)