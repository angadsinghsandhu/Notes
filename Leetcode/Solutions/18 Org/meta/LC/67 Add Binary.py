# ADD BINARY

# Problem number: 67
# Difficulty: Easy
# Tags: String, Math, Bit Manipulation
# Link: https://leetcode.com/problems/add-binary/

class Solution:
    """
    The problem requires adding two binary strings and returning their sum as a binary string.
    The solution involves simulating the binary addition bit by bit, similar to how 
    addition is done manually.

    We can iterate from the end of both strings, adding each pair of digits with a carry.
    Once we reach the beginning of the shorter string, we continue with the remaining 
    digits of the longer string and the carry.

    Time Complexity: O(max(n, m)), where n and m are the lengths of the binary strings a and b
    Space Complexity: O(max(n, m)), since the result string can be as long as the longer input string plus one more character for the carry.
    """
    
    def addBinary(self, a: str, b: str) -> str:
        """
        This function adds two binary strings and returns the sum as a binary string.
        
        T.C. : O(max(n, m)), where n and m are the lengths of the binary strings a and b
        S.C. : O(max(n, m)) to store the resulting binary string
        """
        result = []
        carry = 0
        i, j = len(a) - 1, len(b) - 1
        
        # Loop over both strings starting from the end
        while i >= 0 or j >= 0 or carry:
            # Get the current digits or 0 if we are past the beginning of one string
            digit_a = int(a[i]) if i >= 0 else 0
            digit_b = int(b[j]) if j >= 0 else 0
            
            # Compute the sum of both digits and the carry
            total = digit_a + digit_b + carry
            result.append(str(total % 2))  # Append the binary result (either 0 or 1)
            carry = total // 2  # Update the carry (either 0 or 1)
            
            # Move to the previous digits
            i -= 1
            j -= 1
        
        # The result is currently reversed, so we need to reverse it back
        return ''.join(reversed(result))

# Best Method: This method is the most optimal due to the simple linear iteration over the input strings.
