# File: Leetcode/Solutions/12_Integer_to_Roman.py

"""
Problem Number: 12
Problem Name: Integer to Roman
Difficulty: Medium
Tags: Hash Table, Math, String
Company (Frequency): Amazon (15), Microsoft (10), Google (8)
Leetcode Link: https://leetcode.com/problems/integer-to-roman/description/

DESCRIPTION

Roman numerals are represented by seven different symbols: I, V, X, L, C, D, and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

Roman numerals are formed by appending the conversions of decimal place values from highest to lowest. Converting a decimal place value into a Roman numeral has the following rules:

1. If the value does not start with 4 or 9, select the symbol of the maximal value that can be subtracted from the input, append that symbol to the result, subtract its value, and convert the remainder to a Roman numeral.
2. If the value starts with 4 or 9, use the subtractive form representing one symbol subtracted from the following symbol, for example, 4 is IV (1 less than 5), and 9 is IX (1 less than 10).
3. Only powers of 10 (I, X, C, M) can be appended consecutively at most 3 times to represent multiples of 10. Symbols like V, L, and D cannot be repeated.

Given an integer, convert it to a Roman numeral.

---

#### Example 1:
**Input:**
```plaintext
num = 3749
```

**Output:**
```plaintext
"MMMDCCXLIX"
```

**Explanation:**  
- 3000 = MMM
- 700 = DCC
- 40 = XL
- 9 = IX

#### Constraints:
- `1 <= num <= 3999`
"""

from typing import List

class Solution:
    """
    Thought Process:
    - Roman numerals are constructed by combining symbols in descending order of value.
    - We can use a greedy approach to subtract the largest possible values from the input number and append the corresponding Roman symbols.
    - Special cases like 4 (IV), 9 (IX), 40 (XL), etc., are handled by including them in the list of symbols and values.

    Input:
        num: int - The integer to be converted to a Roman numeral.

    Output:
        str - The Roman numeral representation of the input integer.
    """

    def intToRoman(self, num: int) -> str:
        """
        Approach:
        - Use a list of tuples to store Roman symbols and their corresponding values in descending order.
        - Iterate through the list, subtracting the largest possible value from the input number and appending the corresponding symbol to the result.
        - Repeat until the input number is reduced to 0.

        T.C.: O(1) - The number of iterations is constant (13 symbols).
        S.C.: O(1) - The space used is constant (fixed list of symbols and values).
        """
        # List of Roman symbols and their corresponding values in descending order
        roman_symbols = [
            ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
            ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
            ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1)
        ]
        
        # Initialize an empty list to store the result
        result = []
        
        # Iterate through the symbols and values
        for symbol, value in roman_symbols:
            # Append the symbol while the value can be subtracted from num
            while num >= value:
                result.append(symbol)
                num -= value
        
        # Join the list into a single string and return
        return ''.join(result)


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    num1 = 3749
    print(solution.intToRoman(num1))  # Output: "MMMDCCXLIX"

    # Test case 2
    num2 = 58
    print(solution.intToRoman(num2))  # Output: "LVIII"

    # Test case 3
    num3 = 1994
    print(solution.intToRoman(num3))  # Output: "MCMXCIV"