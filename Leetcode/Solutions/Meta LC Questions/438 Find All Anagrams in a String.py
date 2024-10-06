# FIND ALL ANAGRAMS IN A STRING

# Problem number: 438
# Difficulty: Medium
# Tags: Sliding Window, Hash Table
# Link: https://leetcode.com/problems/find-all-anagrams-in-a-string/

from typing import List

class Solution:
    """
    This problem requires finding all the start indices of p's anagrams in s.
    The approach uses a sliding window technique combined with character frequency 
    counting. We compare the frequency of characters in the current window of `s` with 
    the frequency of characters in `p` to identify anagrams.
    
    We will use the sliding window approach, as it provides an optimal solution in terms 
    of time complexity. 

    Method implemented:
    1. Sliding Window Approach
    """

    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        Sliding Window approach to find all anagram start indices.

        T.C. : O(n), where n is the length of string `s`
        S.C. : O(1), since the frequency array size remains constant (26 letters in the alphabet)
        """
        # Resultant list to store start indices
        result = []
        
        # Edge case: if p is longer than s, there can be no anagrams
        if len(p) > len(s):
            return result
        
        # Frequency arrays for p and for the sliding window in s
        p_count = [0] * 26
        s_count = [0] * 26
        
        # Populate the frequency array for p and for the first window in s
        for i in range(len(p)):
            p_count[ord(p[i]) - ord('a')] += 1
            s_count[ord(s[i]) - ord('a')] += 1
        
        # Sliding window: compare the arrays and slide one character at a time
        for i in range(len(p), len(s)):
            if p_count == s_count:
                result.append(i - len(p))
            
            # Slide the window: include s[i], exclude s[i - len(p)]
            s_count[ord(s[i]) - ord('a')] += 1
            s_count[ord(s[i - len(p)]) - ord('a')] -= 1
        
        # Check the last window
        if p_count == s_count:
            result.append(len(s) - len(p))
        
        return result

# Best Method: The sliding window technique is optimal in both time and space complexity
# as it efficiently handles the character comparisons with constant space for frequency counts.

# Sample Testing
solution = Solution()
print(solution.findAnagrams("cbaebabacd", "abc"))  # Output: [0, 6]
print(solution.findAnagrams("abab", "ab"))  # Output: [0, 1, 2]
