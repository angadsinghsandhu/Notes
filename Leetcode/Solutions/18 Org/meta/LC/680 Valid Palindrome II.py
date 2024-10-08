# VALID PALINDROME II

# Problem number: 680
# Difficulty: Easy
# Tags: Two Pointers, String, Greedy
# Link: https://leetcode.com/problems/valid-palindrome-ii/

class Solution:
    """
    The problem is to determine if a string can become a palindrome by deleting at most one character.
    
    We can solve this using a two-pointer approach:
    1. Use two pointers, one starting from the beginning and the other from the end.
    2. If characters at both pointers match, continue checking.
    3. If characters don't match, try skipping one character from either the left or right and check again.
    
    The idea is to use the fact that we are allowed one deletion to achieve a palindrome.
    """

    def validPalindrome(self, s: str) -> bool:
        """
        This function checks if the string can be a palindrome by removing at most one character.
        
        T.C. : O(n) where n is the length of the string
        S.C. : O(1) since we are using a constant amount of extra space
        """
        
        def is_palindrome_range(i: int, j: int) -> bool:
            """
            Helper function to check if the substring s[i:j+1] is a palindrome.
            """
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True
        
        # Initialize two pointers
        left, right = 0, len(s) - 1
        
        # Traverse the string
        while left < right:
            if s[left] != s[right]:
                # Try skipping either the left or right character
                return is_palindrome_range(left + 1, right) or is_palindrome_range(left, right - 1)
            left += 1
            right -= 1
        
        return True  # If no mismatch is found, the string is already a palindrome

# Best Method: Two Pointers approach is the optimal solution.
