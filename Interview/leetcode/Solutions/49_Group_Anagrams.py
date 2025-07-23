# File: Leetcode/Solutions/Amazon/49_Group_Anagrams.py

"""
Problem Number: 49
Problem Name: Group Anagrams
Difficulty: Medium
Tags: String, Hash Table, Sorting
Company (Frequency): Amazon (82)
Leetcode Link: <https://leetcode.com/problems/group-anagrams/description/>

DESCRIPTION

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

---

#### Example 1:
**Input:**
```plaintext
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
```

**Output:**
```plaintext
[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
```

**Explanation:**  
- There is no string in `strs` that can be rearranged to form "bat".
- The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
- The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.

#### Example 2:
**Input:**
```plaintext
strs = [""]
```

**Output:**
```plaintext
[[""]]
```

#### Example 3:
**Input:**
```plaintext
strs = ["a"]
```

**Output:**
```plaintext
[["a"]]
```

#### Constraints:
- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.
"""

from typing import List
from collections import defaultdict

class Solution:
    """
    Thought Process:
    - The problem involves grouping strings that are anagrams of each other.
    - An anagram is a word or phrase formed by rearranging the letters of a different word or phrase.
    - A common approach is to use a hash table (dictionary) to group strings with the same sorted representation.

    Input:
        strs: List[str] - The input array of strings.

    Output:
        List[List[str]] - A list of grouped anagrams.
    """

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Approach:
        - Use a dictionary to group strings that are anagrams of each other.
        - The key for each group is the sorted version of the string.
        - Iterate through the input list, sort each string, and add it to the corresponding group in the dictionary.

        T.C.: O(n * k log k), where n is the number of strings and k is the maximum length of a string.
        S.C.: O(n * k)
        """
        anagram_groups = defaultdict(list)

        for s in strs:
            # Sort the string to use as a key
            sorted_str = "".join(sorted(s))
            # Add the original string to the corresponding group
            anagram_groups[sorted_str].append(s)

        # Return the grouped anagrams as a list of lists
        return list(anagram_groups.values())

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]

    print(solution.groupAnagrams([""]))
    # Output: [[""]]

    print(solution.groupAnagrams(["a"]))
    # Output: [["a"]]