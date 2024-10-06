# VERIFYING AN ALIEN DICTIONARY

# Problem number: 953
# Difficulty: Easy
# Tags: String, Hash Table
# Link: https://leetcode.com/problems/verifying-an-alien-dictionary/

from typing import List

class Solution:
    """
    This problem involves checking if a list of words is sorted lexicographically
    according to a custom alphabet order (provided in the 'order' string).
    
    We need to map the characters from the custom 'order' to their corresponding
    indices (0 to 25). Then, for each pair of consecutive words in the list, we
    will compare their characters one by one to ensure they are in the correct order.
    
    If at any point we find a character that violates the order, we return False.
    Otherwise, if all word pairs are valid, we return True.
    
    The approach involves:
    1. Creating a map of character order.
    2. Iterating through the words to verify their order.
    """

    def isAlienSorted(self, words: List[str], order: str) -> bool:
        """
        Checks if the words list is sorted based on the alien dictionary order.

        T.C. : O(n * m) where n is the number of words and m is the average length of the words
        S.C. : O(1) for constant extra space usage (excluding input space)
        """
        # Create a dictionary to map each character to its position in the custom alphabet
        order_map = {char: idx for idx, char in enumerate(order)}
        
        # Compare each pair of consecutive words
        for i in range(len(words) - 1):
            if not self.is_sorted(words[i], words[i + 1], order_map):
                return False
        
        return True

    def is_sorted(self, word1: str, word2: str, order_map: dict) -> bool:
        """
        Helper function to compare two words based on the alien dictionary order.
        """
        for c1, c2 in zip(word1, word2):
            # Compare the characters according to the custom order
            if order_map[c1] < order_map[c2]:
                return True
            elif order_map[c1] > order_map[c2]:
                return False
        
        # If all characters are equal, the shorter word should come first
        return len(word1) <= len(word2)

# Best Method: This approach compares each pair of consecutive words efficiently 
# by leveraging a custom order mapping for character comparisons.

# Sample Inputs for Testing
words = ["hello","leetcode"]
order = "hlabcdefgijkmnopqrstuvwxyz"

# Testing the solution
solution = Solution()
print(solution.isAlienSorted(words, order))  # Should output True
