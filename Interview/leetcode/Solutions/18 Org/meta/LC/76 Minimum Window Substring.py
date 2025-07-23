# MINIMUM WINDOW SUBSTRING

# Problem number: 76
# Difficulty: Hard
# Tags: Sliding Window, Hash Map, String
# Link: https://leetcode.com/problems/minimum-window-substring/

from collections import Counter

class Solution:
    """
    The goal is to find the minimum window in string `s` which contains all the characters 
    in string `t` (including duplicates).
    
    We can solve this using the Sliding Window approach. By expanding and contracting the 
    window dynamically, we can keep track of the count of characters from `t` in `s`. The 
    idea is to maintain a valid window that contains all the characters in `t`, then try to 
    minimize its size.

    Approach:
    - Maintain two pointers (left and right) for the window.
    - Use a hash map (Counter) to count characters in `t`.
    - Expand the window by moving the right pointer until the window contains all characters 
      from `t`.
    - Once a valid window is found, move the left pointer to reduce the window size while 
      maintaining validity.

    Time Complexity: O(m + n), where m is the length of `s` and n is the length of `t`. 
    We visit each character in `s` at most twice.
    
    Space Complexity: O(n), where n is the number of unique characters in `t`.
    """

    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""
        
        # Step 1: Count all characters in t
        t_count = Counter(t)
        required = len(t_count)
        
        # Step 2: Initialize window pointers and variables for tracking the minimum window
        left, right = 0, 0
        window_counts = {}
        formed = 0  # To keep track of how many unique characters in t are satisfied in the current window
        min_length = float("inf")
        min_window = (0, 0)  # Stores the start and end of the minimum window
        
        while right < len(s):
            # Add current character to the window
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1
            
            # If the current character in window matches the count in t, increment `formed`
            if char in t_count and window_counts[char] == t_count[char]:
                formed += 1
            
            # Try to contract the window from the left if all characters are found
            while left <= right and formed == required:
                char = s[left]
                
                # Update the minimum window
                if right - left + 1 < min_length:
                    min_length = right - left + 1
                    min_window = (left, right)
                
                # Remove the leftmost character from the window
                window_counts[char] -= 1
                if char in t_count and window_counts[char] < t_count[char]:
                    formed -= 1
                
                left += 1
            
            # Expand the window to the right
            right += 1
        
        # Step 3: Return the minimum window substring
        return "" if min_length == float("inf") else s[min_window[0]:min_window[1] + 1]

# Best Method: Sliding Window Approach is the optimal solution for this problem.
