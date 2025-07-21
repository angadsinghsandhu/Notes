# File: Leetcode/Solutions/Array/916_Word_Subsets.py
"""
Problem Number: 916
Problem Name: Word Subsets
Difficulty: Medium
Tags: Array, Hash Table, String
Company (Frequency): Not explicitly stated, but common for string manipulation and frequency counting.
Leetcode Link: <https://leetcode.com/problems/word-subsets/description/>

DESCRIPTION

You are given two string arrays `words1` and `words2`.
A string `b` is a subset of string `a` if every letter in `b` occurs in `a` including multiplicity.
For example, "wrr" is a subset of "warrior" but is not a subset of "world".
A string `a` from `words1` is universal if for every string `b` in `words2`, `b` is a subset of `a`.
Return an array of all the universal strings in `words1`. You may return the answer in any order.

---

#### Example 1:

Input:
words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["e","o"]

Output:
["facebook","google","leetcode"]

---

#### Example 2:

Input:
words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["lc","eo"]

Output:
["leetcode"]

---

#### Example 3:

Input:
words1 = ["acaac","cccbb","aacbb","caacc","bcbbb"], words2 = ["c","cc","b"]

Output:
["cccbb"]

---

#### Constraints:

- 1 <= words1.length, words2.length <= 10^4
- 1 <= words1[i].length, words2[i].length <= 10
- words1[i] and words2[i] consist only of lowercase English letters.
- All the strings of `words1` are unique.
"""
from typing import List

class Solution:
    """
    Thought Process:

    The core idea for a string `a` from `words1` to be "universal" is that it must contain
    all characters from *every* string `b` in `words2` with sufficient multiplicity.

    This means `a` must satisfy the subset condition for `b1`, `b2`, ..., `bm` (where m is words2.length).
    If `b` is a subset of `a`, then for every character `char`, `count(char, b) <= count(char, a)`.

    Combining this for all `b` in `words2`, string `a` must have `count(char, a) >= max_b_count_for_char`
    for every `char`, where `max_b_count_for_char` is the maximum frequency required for `char` across
    *all* strings in `words2`.

    For example, if `words2 = ["loo", "cool"]`:
    - For 'l': "loo" needs 2 'l's, "cool" needs 1 'l'. So, `max_b_count['l'] = max(2, 1) = 2`.
    - For 'o': "loo" needs 2 'o's, "cool" needs 2 'o's. So, `max_b_count['o'] = max(2, 2) = 2`.
    - For 'c': "loo" needs 0 'c's, "cool" needs 1 'c'. So, `max_b_count['c'] = max(0, 1) = 1`.

    So, any universal string `a` must have at least two 'l's, two 'o's, and one 'c'.

    This observation leads to an efficient two-pass algorithm.

    Algorithm Steps:

    1.  **Build a "Master" Frequency Map for `words2`:**
        - Create an array (or dictionary) `max_b_freq` of size 26 (for 'a' through 'z'), initialized to all zeros.
        - Iterate through each string `b` in `words2`:
            - Calculate the frequency map `b_freq` for the current string `b`.
            - For each character `char` (from 'a' to 'z'):
                - Update `max_b_freq[char]` to be `max(max_b_freq[char], b_freq[char])`. This ensures `max_b_freq` stores the highest requirement for each character across all words in `words2`.

    2.  **Check Each String in `words1` against the Master Map:**
        - Initialize an empty list `result` to store universal strings.
        - Iterate through each string `a` in `words1`:
            - Calculate the frequency map `a_freq` for the current string `a`.
            - Assume `a` is universal (`is_universal = True`).
            - Iterate through each character `char` (from 'a' to 'z'):
                - If `a_freq[char]` is less than `max_b_freq[char]`:
                    - Then `a` cannot satisfy the requirement for this `char`, so it's not universal.
                    - Set `is_universal = False` and break this inner loop (no need to check further characters for `a`).
            - If `is_universal` is still `True` after checking all characters, add `a` to the `result` list.

    3.  **Return `result`.**

    Complexity Analysis:
    Let:
    - N = `len(words1)`
    - M = `len(words2)`
    - L1_max = maximum length of a string in `words1` (max 10)
    - L2_max = maximum length of a string in `words2` (max 10)
    - C = number of unique lowercase English letters (26)

    T.C.:
    - Step 1: Iterate through `M` strings. For each string, we build a frequency map (O(L2_max)) and then update `C` entries in `max_b_freq` (O(C)). So, O(M * (L2_max + C)).
    - Step 2: Iterate through `N` strings. For each string, we build a frequency map (O(L1_max)) and then compare `C` entries (O(C)). So, O(N * (L1_max + C)).
    - Total Time Complexity: O(M * (L2_max + C) + N * (L1_max + C)).
    - Since L1_max, L2_max, and C are small constants (<= 26), this can be approximated as O(M * L2_max + N * L1_max).
    - Given constraints (N, M <= 10^4, lengths <= 10), this is roughly 10^4 * 10 = 10^5 operations, which is efficient enough.

    S.C.:
    - `max_b_freq`: O(C)
    - Temporary frequency maps (`b_freq`, `a_freq`): O(C)
    - `result` list: O(N) in the worst case (if all strings in `words1` are universal).
    - Total Space Complexity: O(C + N), which simplifies to O(N) as C is a constant.
    """

    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        """
        Calculates the frequency map for a given string.
        Returns a list of 26 integers representing counts for 'a' through 'z'.
        """
        def count_chars(word: str) -> List[int]:
            freq = [0] * 26
            for char_code in map(ord, word):
                freq[char_code - ord('a')] += 1
            return freq

        # Step 1: Build the master frequency map for words2
        # max_b_freq[i] will store the maximum count required for the i-th letter
        # across all words in words2.
        max_b_freq = [0] * 26
        for b_word in words2:
            b_freq = count_chars(b_word)
            for i in range(26):
                max_b_freq[i] = max(max_b_freq[i], b_freq[i])

        # Step 2: Check each word in words1 against the master frequency map
        universal_strings = []
        for a_word in words1:
            a_freq = count_chars(a_word)
            is_universal = True
            for i in range(26):
                # If 'a_word' does not have enough of character 'i' to satisfy 'max_b_freq'
                if a_freq[i] < max_b_freq[i]:
                    is_universal = False
                    break # No need to check other characters for this 'a_word'
            
            if is_universal:
                universal_strings.append(a_word)
        
        return universal_strings

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        # Example 1
        ({"words1": ["amazon","apple","facebook","google","leetcode"], "words2": ["e","o"]}, ["facebook","google","leetcode"]),
        # Example 2
        ({"words1": ["amazon","apple","facebook","google","leetcode"], "words2": ["lc","eo"]}, ["leetcode"]),
        # Example 3
        ({"words1": ["acaac","cccbb","aacbb","caacc","bcbbb"], "words2": ["c","cc","b"]}, ["cccbb"]),
        # Custom Test Case: 'a' requires 'a' (1) and 'b' requires 'a' (2)
        ({"words1": ["apple", "banana", "bandana"], "words2": ["a", "aa"]}, ["banana", "bandana"]),
        # Custom Test Case: No universal strings
        ({"words1": ["xyz"], "words2": ["a"]}, []),
        # Custom Test Case: All universal strings
        ({"words1": ["aaaaa", "bbbbb"], "words2": ["a", "b"]}, ["aaaaa", "bbbbb"]),
    ]

    for inputs, expected_output in test_cases:
        words1 = inputs["words1"]
        words2 = inputs["words2"]
        
        # We need to sort the output because the problem states "You may return the answer in any order."
        # Sorting allows for consistent comparison against expected output.
        result = sorted(solution.wordSubsets(words1, words2))
        
        # Sort expected output for comparison
        sorted_expected_output = sorted(expected_output)

        print(f"Input: words1={words1}, words2={words2}")
        print(f"Output: {result}")
        print(f"Expected: {sorted_expected_output}")
        print(f"Status: {'Pass' if result == sorted_expected_output else 'Fail'}")
        print("-" * 30)