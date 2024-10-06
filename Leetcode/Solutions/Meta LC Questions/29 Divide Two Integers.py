# DIVIDE TWO INTEGERS

# Problem number: 29
# Difficulty: Medium
# Tags: Math, Bit Manipulation
# Link: https://leetcode.com/problems/divide-two-integers/

class Solution:
    """
    This problem requires dividing two integers without using multiplication, division, or modulus operators.
    The goal is to return the quotient, truncated towards zero, while handling edge cases like overflow.

    The solution involves bit manipulation (shifting) to repeatedly subtract the divisor from the dividend 
    until we cannot subtract anymore. We also account for signs and ensure the quotient is within the 
    32-bit signed integer range.
    """

    def divide(self, dividend: int, divisor: int) -> int:
        """
        Bit manipulation approach to perform division without multiplication, division, or modulus.
        
        T.C. : O(log(n)) where n is the dividend, due to repeatedly halving the problem size
        S.C. : O(1) since no extra space is used other than variables
        """
        # Constants for 32-bit integer limits
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31
        
        # Edge case for overflow
        if dividend == MIN_INT and divisor == -1:
            return MAX_INT
        
        # Determine the sign of the result
        negative = (dividend < 0) != (divisor < 0)
        
        # Work with positive values for simplicity
        dividend, divisor = abs(dividend), abs(divisor)
        quotient = 0
        
        # Shift the divisor until it's larger than the dividend
        while dividend >= divisor:
            temp, multiple = divisor, 1
            while dividend >= (temp << 1):
                temp <<= 1
                multiple <<= 1
            
            # Subtract the largest shifted divisor and add to quotient
            dividend -= temp
            quotient += multiple
        
        # Apply the sign to the quotient
        quotient = -quotient if negative else quotient
        
        # Ensure the quotient is within the 32-bit signed integer range
        return max(MIN_INT, min(MAX_INT, quotient))

# Best Method: This bit manipulation approach is optimal for this problem, achieving logarithmic time complexity.
