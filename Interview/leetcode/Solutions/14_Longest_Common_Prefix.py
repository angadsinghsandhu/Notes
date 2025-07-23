# File: Leetcode/Solutions/14_Longest_Common_Prefix.py

"""
Problem Number: 14
Problem Name: Longest Common Prefix
Difficulty: Easy
Tags: String, Trie
Company (Frequency): Amazon (32), Google (28), Microsoft (20)
Leetcode Link: https://leetcode.com/problems/longest-common-prefix/

DESCRIPTION

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

---

#### Example 1:
**Input:**
```plaintext
strs = ["flower","flow","flight"]
```

**Output:**
```plaintext
"fl"
```

#### Example 2:
**Input:**
```plaintext
strs = ["dog","racecar","car"]
```

**Output:**
```plaintext
""
```

**Explanation:**  
There is no common prefix among the input strings.

#### Constraints:
- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` consists of only lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem requires finding the longest common prefix among all given strings.
    - The brute-force approach compares each character of the first string with the corresponding characters of all other strings.
    - A more optimized approach sorts the list and compares only the first and last string, as they would have the least commonality.

    Input:
        strs: List[str] - A list of strings.

    Output:
        str - The longest common prefix.
    """

    def brute_force_solution(self, strs: List[str]) -> str:
        """
        Approach:
        - Iterate through each character of the first string.
        - Compare it with the corresponding character in every other string.
        - If a mismatch is found, return the common prefix found so far.

        T.C.: O(n * m) - n is the number of strings, and m is the length of the shortest string.
        S.C.: O(1) - Constant space used.
        """
        if not strs:
            return ""

        for i in range(len(strs[0])):
            for s in strs[1:]:
                if i >= len(s) or s[i] != strs[0][i]:
                    return strs[0][:i]
        return strs[0]

    def optimized_solution(self, strs: List[str]) -> str:
        """
        Approach:
        - Sort the strings lexicographically.
        - Compare only the first and last string in the sorted list, as they will have the least commonality.
        - Return the common prefix found in these two strings.

        T.C.: O(n log n + m) - Sorting takes O(n log n), and comparing first/last string takes O(m).
        S.C.: O(1) - No extra space used.
        """
        if not strs:
            return ""

        strs.sort()  # Sort lexicographically
        first, last = strs[0], strs[-1]

        i = 0
        while i < len(first) and i < len(last) and first[i] == last[i]:
            i += 1

        return first[:i]


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    strs1 = ["flower", "flow", "flight"]
    print(solution.brute_force_solution(strs1))  # Output: "fl"
    print(solution.optimized_solution(strs1))    # Output: "fl"

    # Test case 2
    strs2 = ["dog", "racecar", "car"]
    print(solution.brute_force_solution(strs2))  # Output: ""
    print(solution.optimized_solution(strs2))    # Output: ""
