# VALID PALINDROME

# Problem number: 125
# Difficulty: Easy
# Tags: String, Two Pointers
# Link: https://leetcode.com/problems/valid-palindrome/

class Solution:
    """
    This problem requires checking whether a given string is a valid palindrome.
    A valid palindrome ignores cases, spaces, and non-alphanumeric characters.

    We will implement two methods:
    1. Two-Pointer Approach (Optimal)
    2. String Cleaning and Reversing (Simpler but less optimal)
    """

    def isPalindrome_TwoPointers(self, s: str) -> bool:
        """
        Two-Pointer approach to check for a valid palindrome.
        
        T.C. : O(n) where n is the length of the string
        S.C. : O(1) since we only use two pointers for in-place checks
        """
        left, right = 0, len(s) - 1
        
        while left < right:
            # Move left pointer until alphanumeric is found
            while left < right and not s[left].isalnum():
                left += 1
            # Move right pointer until alphanumeric is found
            while left < right and not s[right].isalnum():
                right -= 1
            
            # Check if the characters are equal (ignoring case)
            if s[left].lower() != s[right].lower():
                return False
            
            left += 1
            right -= 1
        
        return True

    def isPalindrome_StringCleaning(self, s: str) -> bool:
        """
        Simpler method: Clean the string by removing non-alphanumeric characters 
        and comparing it with its reverse.
        
        T.C. : O(n) where n is the length of the string (due to cleaning and reversing)
        S.C. : O(n) due to extra space used for the cleaned string and its reverse
        """
        cleaned_str = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned_str == cleaned_str[::-1]

# Best Method: Two-Pointer Approach is preferred for its in-place and space-efficient nature.

# Sample Inputs for Testing
s1 = "A man, a plan, a canal: Panama"  # Expected output: True
s2 = "race a car"  # Expected output: False
s3 = " "  # Expected output: True

# Testing Two-Pointer Method
print(Solution().isPalindrome_TwoPointers(s1))  # True
print(Solution().isPalindrome_TwoPointers(s2))  # False
print(Solution().isPalindrome_TwoPointers(s3))  # True

# Testing String Cleaning Method
print(Solution().isPalindrome_StringCleaning(s1))  # True
print(Solution().isPalindrome_StringCleaning(s2))  # False
print(Solution().isPalindrome_StringCleaning(s3))  # True
