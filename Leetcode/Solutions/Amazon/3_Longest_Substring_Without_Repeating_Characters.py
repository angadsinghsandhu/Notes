# File: Leetcode/Solutions/Amazon/3_Longest_Substring_Without_Repeating_Characters.py

"""
Problem Number: 3
Problem Name: Longest Substring Without Repeating Characters
Difficulty: Medium
Tags: String, Sliding Window, Hash Table
Company (Frequency): Amazon (123)
Leetcode Link: <https://leetcode.com/problems/longest-substring-without-repeating-characters/description/>

DESCRIPTION

Given a string `s`, find the length of the longest substring without repeating characters.

---

#### Example 1:
**Input:**
```plaintext
s = "abcabcbb"
```

**Output:**
```plaintext
3
```

**Explanation:**  
The answer is "abc", with the length of 3.

#### Example 2:
**Input:**
```plaintext
s = "bbbbb"
```

**Output:**
```plaintext
1
```

**Explanation:**  
The answer is "b", with the length of 1.

#### Example 3:
**Input:**
```plaintext
s = "pwwkew"
```

**Output:**
```plaintext
3
```

**Explanation:**  
The answer is "wke", with the length of 3.  
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

#### Constraints:
- 0 <= s.length <= 5 * 10^4
- `s` consists of English letters, digits, symbols, and spaces.
"""

class Solution:
    """
    Thought Process:
    - The problem involves finding the longest substring without repeating characters.
    - A brute force solution would check all possible substrings, but it is inefficient (O(n^2)).
    - An optimized solution uses the sliding window technique with a hash table to track characters and their indices.

    Input:
        s: str - The input string.

    Output:
        int - The length of the longest substring without repeating characters.
    """

    def brute_force_solution(self, s: str) -> int:
        """
        Approach:
        - Check all possible substrings and determine if they contain unique characters.
        - Keep track of the maximum length found.

        T.C.: O(n^2)
        S.C.: O(min(n, m)) where m is the size of the character set.
        """
        max_length = 0
        for i in range(len(s)):
            seen = set()
            current_length = 0
            for j in range(i, len(s)):
                if s[j] in seen:
                    break
                seen.add(s[j])
                current_length += 1
            max_length = max(max_length, current_length)
        return max_length

    def sliding_window_solution(self, s: str) -> int:
        """
        Approach:
        - Use a sliding window to represent the current substring.
        - Use a hash table to store the last index of each character.
        - Move the start of the window forward if a repeating character is found.

        T.C.: O(n)
        S.C.: O(min(n, m)) where m is the size of the character set.
        """
        char_to_index = {}  # Stores the last index of each character
        max_length = 0
        start = 0  # Start of the sliding window

        for end in range(len(s)):
            if s[end] in char_to_index:
                # Move the start of the window to the right of the last occurrence of s[end]
                start = max(start, char_to_index[s[end]] + 1)
            # Update the last index of the current character
            char_to_index[s[end]] = end
            # Update the maximum length
            max_length = max(max_length, end - start + 1)

        return max_length

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.brute_force_solution("abcabcbb"))  # Output: 3
    print(solution.sliding_window_solution("bbbbb"))  # Output: 1
    print(solution.sliding_window_solution("pwwkew"))  # Output: 3