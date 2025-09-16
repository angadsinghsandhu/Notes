# File: Leetcode/Solutions/20_Valid_Parentheses.py

"""
Problem Number: 20
Problem Name: Valid Parentheses
Difficulty: Easy
Tags: String, Stack, Neetcode 150
Company (Frequency): Amazon, Facebook, Google, Microsoft, Bloomberg
Leetcode Link: <https://leetcode.com/problems/valid-parentheses/description/>

DESCRIPTION

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

---

#### Example 1:
**Input:**
```plaintext
s = "()"
```

**Output:**
```plaintext
true
```

#### Example 2:
**Input:**
```plaintext
s = "()[]{}"
```

**Output:**
```plaintext
true
```

#### Example 3:
**Input:**
```plaintext
s = "(]"
```

**Output:**
```plaintext
false
```

#### Example 4:
**Input:**
```plaintext
s = "([])"
```

**Output:**
```plaintext
true
```

#### Constraints:
- 1 <= s.length <= 10^4
- `s` consists of parentheses only `'()[]{}'`.
"""

class Solution:
    """
    Thought Process:
    - The problem involves validating the correctness of nested parentheses.
    - A stack-based approach is ideal for matching opening and closing brackets in the correct order.
    - Iterate through the string, push opening brackets onto the stack, and pop from the stack when encountering closing brackets.

    Input:
        s: str - The input string containing parentheses.

    Output:
        bool - True if the string is valid, False otherwise.
    """

    def isValid(self, s: str) -> bool:
        """
        Approach:
        - Use a stack to keep track of opening brackets.
        - Iterate through the string:
            - If the character is an opening bracket, push it onto the stack.
            - If the character is a closing bracket, check if it matches the top of the stack.
        - The string is valid if the stack is empty at the end.

        T.C.: O(n)
        S.C.: O(n)
        """
        stack = []
        bracket_map = {')': '(', '}': '{', ']': '['}

        for char in s:
            if char in bracket_map.values():  # Opening bracket
                stack.append(char)
            elif char in bracket_map.keys():  # Closing bracket
                if not stack or stack[-1] != bracket_map[char]:
                    return False
                stack.pop()
            else:
                return False  # Invalid character

        return not stack  # Stack should be empty for valid parentheses

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.isValid("()"))  # Output: True
    print(solution.isValid("()[]{}"))  # Output: True
    print(solution.isValid("(]"))  # Output: False
    print(solution.isValid("([])"))  # Output: True
    print(solution.isValid("([)]"))  # Output: False