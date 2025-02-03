# File: Leetcode/Solutions/8_String_to_Integer_atoi.py

"""
Problem Number: 8
Problem Name: String to Integer (atoi)
Difficulty: Medium
Tags: String
Company (Frequency): Various (Not specified)
Leetcode Link: https://leetcode.com/problems/string-to-integer-atoi/description/

DESCRIPTION

Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer (similar to C/C++'s `atoi` function).

The algorithm for `myAtoi(string s)` is as follows:

1. Read in and ignore any leading whitespace.
2. Check if the next character (if not already at the end of the string) is '-' or '+'. Read this character in if it is either. This determines if the final result is negative or positive respectively. Assume the result is positive if neither is present.
3. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.
4. Convert these digits into an integer (i.e., "123" -> 123, "0032" -> 32). If no digits were read, then the integer is 0. Change the sign as necessary (from step 2).
5. If the integer is out of the 32-bit signed integer range [-2^31, 2^31 - 1], then clamp the integer so that it remains in the range. Specifically, integers less than -2^31 should be clamped to -2^31, and integers greater than 2^31 - 1 should be clamped to 2^31 - 1.
6. Return the integer as the final result.

---

#### Example 1:
**Input:**
```plaintext
s = "42"
```

**Output:**
```plaintext
42
```

**Explanation:**  
The underlined characters are what is read in, and the caret is the current reader position.
Step 1: "42" (no characters read because there is no leading whitespace)
         ^
Step 2: "42" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "42" ("42" is read in)
           ^
The parsed integer is 42.
Since 42 is in the range [-2^31, 2^31 - 1], the final result is 42.

#### Example 2:
**Input:**
```plaintext
s = "   -42"
```

**Output:**
```plaintext
-42
```

**Explanation:**  
Step 1: "   -42" (leading whitespace is read and ignored)
            ^
Step 2: "   -42" ('-' is read, so the result should be negative)
             ^
Step 3: "   -42" ("42" is read in)
               ^
The parsed integer is -42.
Since -42 is in the range [-2^31, 2^31 - 1], the final result is -42.

#### Constraints:
- `0 <= s.length <= 200`
- `s` consists of English letters (lower-case and upper-case), digits (0-9), ' ', '+', '-', and '.'.
"""

class Solution:
    """
    Thought Process:
    - The problem involves converting a string to a 32-bit signed integer following specific rules.
    - A brute-force approach involves manually parsing the string step by step, but this can be error-prone.
    - An optimized approach uses a single pass to handle whitespace, sign, and digit conversion while checking for overflow.

    Input:
        s: str - The input string to be converted to an integer.

    Output:
        int - The 32-bit signed integer representation of the string.
    """

    def optimized_solution(self, s: str) -> int:
        """
        Approach:
        - Use a single pass to handle whitespace, sign, and digit conversion.
        - Use integer operations to avoid overflow checks during conversion.

        T.C.: O(n) - Single pass through the string.
        S.C.: O(1) - Constant space used.
        """
        if not s:
            return 0

        n = len(s)
        i = 0

        # Step 1: Skip leading whitespace
        while i < n and s[i] == ' ':
            i += 1

        # Step 2: Handle sign
        sign = 1
        if i < n and (s[i] == '+' or s[i] == '-'):
            sign = -1 if s[i] == '-' else 1
            i += 1

        # Step 3: Convert digits to integer
        result = 0
        max_safe_int = (2**31 - 1) // 10  # Precompute to avoid overflow
        while i < n and s[i].isdigit():
            digit = int(s[i])
            # Step 5: Check for overflow
            if result > max_safe_int or (result == max_safe_int and digit > 7):
                return 2**31 - 1 if sign == 1 else -2**31
            result = result * 10 + digit
            i += 1

        # Step 6: Apply sign and return result
        return sign * result

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    s1 = "42"
    print(solution.brute_force_solution(s1))  # Output: 42
    print(solution.optimized_solution(s1))    # Output: 42

    # Test case 2
    s2 = "   -42"
    print(solution.brute_force_solution(s2))  # Output: -42
    print(solution.optimized_solution(s2))    # Output: -42

    # Test case 3
    s3 = "4193 with words"
    print(solution.brute_force_solution(s3))  # Output: 4193
    print(solution.optimized_solution(s3))    # Output: 4193

    # Test case 4
    s4 = "words and 987"
    print(solution.brute_force_solution(s4))  # Output: 0
    print(solution.optimized_solution(s4))    # Output: 0

    # Test case 5
    s5 = "-91283472332"
    print(solution.brute_force_solution(s5))  # Output: -2147483648
    print(solution.optimized_solution(s5))    # Output: -2147483648
